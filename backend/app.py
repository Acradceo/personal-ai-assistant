from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
from langchain.llms import Ollama
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from datetime import datetime
import logging
import secrets

load_dotenv()

app = Flask(__name__)

# Configure CORS securely
allowed_origins_env = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,http://localhost:5000,http://127.0.0.1:3000,http://127.0.0.1:5000")
allowed_origins = [origin.strip() for origin in allowed_origins_env.split(",")]
CORS(app, origins=allowed_origins)

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# API Key for sensitive operations
API_KEY = os.getenv("API_KEY", None)

# Initialize Ollama LLM
try:
    llm = Ollama(
        model="mistral",
        callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]),
        temperature=0.7,
    )
    logger.info("✓ Ollama LLM initialized successfully")
except Exception as e:
    logger.error(f"✗ Failed to initialize Ollama: {e}")
    llm = None

# Data structures - optimized for O(1) lookups
conversation_history = []
tasks = {}  # Changed from list to dict for O(1) lookups
notes = {}  # Changed from list to dict for O(1) lookups
next_task_id = 1
next_note_id = 1

# ============ Authentication ============

def require_api_key(f):
    """Decorator to require API key for sensitive operations"""
    def decorated(*args, **kwargs):
        if API_KEY is None:
            logger.warning("API_KEY not configured for protected endpoint")
            return jsonify({"error": "API_KEY not configured on server"}), 500
        
        auth_header = request.headers.get("Authorization", "")
        api_key_header = request.headers.get("X-API-Key", "")
        
        # Try both Bearer token and direct API key
        token = None
        if auth_header.startswith("Bearer "):
            token = auth_header[7:]
        elif api_key_header:
            token = api_key_header
        
        if not token or not secrets.compare_digest(token, API_KEY):
            logger.warning(f"Unauthorized access attempt to {request.path}")
            return jsonify({"error": "Unauthorized"}), 401
        
        return f(*args, **kwargs)
    
    decorated.__name__ = f.__name__
    return decorated

# ============ Health & Status ============

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "ollama_available": llm is not None
    }), 200

# ============ Chat Endpoint ============

@app.route('/api/chat', methods=['POST'])
@require_api_key
def chat():
    """Main chat endpoint"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid JSON"}), 400
        
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({"error": "Empty message"}), 400
        
        if llm is None:
            return jsonify({
                "error": "Ollama LLM not available. Make sure Ollama is running.",
                "help": "Start Ollama: ollama run mistral"
            }), 503
        
        # Add to conversation history
        conversation_history.append({
            "role": "user",
            "content": user_message,
            "timestamp": datetime.now().isoformat()
        })
        
        # Get response from LLM
        response = llm.predict(user_message)
        
        # Add response to history
        conversation_history.append({
            "role": "assistant",
            "content": response,
            "timestamp": datetime.now().isoformat()
        })
        
        return jsonify({
            "response": response,
            "timestamp": datetime.now().isoformat(),
            "conversation_length": len(conversation_history)
        }), 200
        
    except Exception as e:
        logger.error(f"Chat error: {e}")
        return jsonify({"error": str(e)}), 500

# ============ Tasks Endpoints ============

@app.route('/api/tasks', methods=['GET', 'POST'])
def manage_tasks():
    """Manage tasks - GET returns all tasks, POST creates new task"""
    try:
        if request.method == 'POST':
            data = request.get_json()
            if not data or 'title' not in data:
                return jsonify({"error": "Missing required field: title"}), 400
            
            global next_task_id
            task_id = next_task_id
            next_task_id += 1
            
            task = {
                "id": task_id,
                "title": data.get('title'),
                "description": data.get('description', ''),
                "status": "pending",
                "created_at": datetime.now().isoformat()
            }
            tasks[task_id] = task
            return jsonify(task), 201
        
        # GET: return all tasks as list
        return jsonify({"tasks": list(tasks.values())}), 200
        
    except Exception as e:
        logger.error(f"Task error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/tasks/<int:task_id>', methods=['GET', 'PUT', 'DELETE'])
def task_detail(task_id):
    """Get, update, or delete a specific task"""
    try:
        if task_id not in tasks:
            return jsonify({"error": "Task not found"}), 404
        
        if request.method == 'GET':
            return jsonify(tasks[task_id]), 200
        
        if request.method == 'PUT':
            data = request.get_json()
            if not data:
                return jsonify({"error": "Invalid JSON"}), 400
            
            task = tasks[task_id]
            
            # Whitelist allowed fields to prevent mass assignment
            allowed_fields = {'title', 'description', 'status'}
            for field in allowed_fields:
                if field in data:
                    task[field] = data[field]
            
            return jsonify(task), 200
        
        if request.method == 'DELETE':
            deleted_task = tasks.pop(task_id)
            return jsonify({"message": "Task deleted", "task": deleted_task}), 200
            
    except Exception as e:
        logger.error(f"Task detail error: {e}")
        return jsonify({"error": str(e)}), 500

# ============ Notes Endpoints ============

@app.route('/api/notes', methods=['GET', 'POST'])
def manage_notes():
    """Manage notes - GET returns all notes, POST creates new note"""
    try:
        if request.method == 'POST':
            data = request.get_json()
            if not data or 'title' not in data:
                return jsonify({"error": "Missing required field: title"}), 400
            
            global next_note_id
            note_id = next_note_id
            next_note_id += 1
            
            note = {
                "id": note_id,
                "title": data.get('title'),
                "content": data.get('content', ''),
                "created_at": datetime.now().isoformat(),
                "tags": data.get('tags', [])
            }
            notes[note_id] = note
            return jsonify(note), 201
        
        # GET: return all notes as list
        return jsonify({"notes": list(notes.values())}), 200
        
    except Exception as e:
        logger.error(f"Notes error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/notes/<int:note_id>', methods=['GET', 'PUT', 'DELETE'])
def note_detail(note_id):
    """Get, update, or delete a specific note"""
    try:
        if note_id not in notes:
            return jsonify({"error": "Note not found"}), 404
        
        if request.method == 'GET':
            return jsonify(notes[note_id]), 200
        
        if request.method == 'PUT':
            data = request.get_json()
            if not data:
                return jsonify({"error": "Invalid JSON"}), 400
            
            note = notes[note_id]
            
            # Whitelist allowed fields to prevent mass assignment
            allowed_fields = {'title', 'content', 'tags'}
            for field in allowed_fields:
                if field in data:
                    note[field] = data[field]
            
            return jsonify(note), 200
        
        if request.method == 'DELETE':
            deleted_note = notes.pop(note_id)
            return jsonify({"message": "Note deleted", "note": deleted_note}), 200
            
    except Exception as e:
        logger.error(f"Note detail error: {e}")
        return jsonify({"error": str(e)}), 500

# ============ History Endpoints ============

@app.route('/api/history', methods=['GET'])
def get_history():
    """Get conversation history"""
    try:
        limit = request.args.get('limit', default=50, type=int)
        if limit < 1 or limit > 1000:
            limit = 50
        
        return jsonify({
            "history": conversation_history[-limit:],
            "total": len(conversation_history)
        }), 200
    except Exception as e:
        logger.error(f"History error: {e}")
        return jsonify({"error": str(e)}), 500

# ============ Admin Endpoints ============

@app.route('/api/clear', methods=['POST'])
@require_api_key
def clear_data():
    """Clear all data (requires API key)"""
    try:
        global conversation_history, tasks, notes, next_task_id, next_note_id
        conversation_history = []
        tasks = {}
        notes = {}
        next_task_id = 1
        next_note_id = 1
        
        logger.warning("All data cleared by authenticated request")
        return jsonify({"message": "All data cleared"}), 200
    except Exception as e:
        logger.error(f"Clear error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get statistics about stored data"""
    try:
        return jsonify({
            "tasks_count": len(tasks),
            "notes_count": len(notes),
            "history_length": len(conversation_history),
            "next_task_id": next_task_id,
            "next_note_id": next_note_id,
            "timestamp": datetime.now().isoformat()
        }), 200
    except Exception as e:
        logger.error(f"Stats error: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug_mode = os.getenv('DEBUG', 'False').lower() == 'true'
    app.run(host='0.0.0.0', port=port, debug=debug_mode)
