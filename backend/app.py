from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
from langchain.llms import Ollama
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
import json
from datetime import datetime
import logging

load_dotenv()

app = Flask(__name__)
CORS(app)

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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

# Store conversation history
conversation_history = []
tasks = []
notes = []

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "ollama_available": llm is not None
    }), 200

@app.route('/api/chat', methods=['POST'])
def chat():
    """Main chat endpoint"""
    try:
        data = request.get_json()
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

@app.route('/api/tasks', methods=['GET', 'POST'])
def manage_tasks():
    """Manage tasks"""
    try:
        if request.method == 'POST':
            data = request.get_json()
            task = {
                "id": len(tasks) + 1,
                "title": data.get('title'),
                "description": data.get('description', ''),
                "status": "pending",
                "created_at": datetime.now().isoformat()
            }
            tasks.append(task)
            return jsonify(task), 201
        
        return jsonify({"tasks": tasks}), 200
        
    except Exception as e:
        logger.error(f"Task error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/tasks/<int:task_id>', methods=['PUT', 'DELETE'])
def update_task(task_id):
    """Update or delete a task"""
    try:
        task = next((t for t in tasks if t['id'] == task_id), None)
        
        if not task:
            return jsonify({"error": "Task not found"}), 404
        
        if request.method == 'PUT':
            data = request.get_json()
            allowed_fields = ['title', 'description', 'status']
            for field in allowed_fields:
                if field in data:
                    task[field] = data[field]
            return jsonify(task), 200
        
        if request.method == 'DELETE':
            tasks.remove(task)
            return jsonify({"message": "Task deleted"}), 200
            
    except Exception as e:
        logger.error(f"Update task error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/notes', methods=['GET', 'POST'])
def manage_notes():
    """Manage notes"""
    try:
        if request.method == 'POST':
            data = request.get_json()
            note = {
                "id": len(notes) + 1,
                "title": data.get('title'),
                "content": data.get('content', ''),
                "created_at": datetime.now().isoformat(),
                "tags": data.get('tags', [])
            }
            notes.append(note)
            return jsonify(note), 201
        
        return jsonify({"notes": notes}), 200
        
    except Exception as e:
        logger.error(f"Notes error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/notes/<int:note_id>', methods=['PUT', 'DELETE'])
def update_note(note_id):
    """Update or delete a note"""
    try:
        note = next((n for n in notes if n['id'] == note_id), None)
        
        if not note:
            return jsonify({"error": "Note not found"}), 404
        
        if request.method == 'PUT':
            data = request.get_json()
            allowed_fields = ['title', 'content', 'tags']
            for field in allowed_fields:
                if field in data:
                    note[field] = data[field]
            return jsonify(note), 200
        
        if request.method == 'DELETE':
            notes.remove(note)
            return jsonify({"message": "Note deleted"}), 200
            
    except Exception as e:
        logger.error(f"Update note error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/history', methods=['GET'])
def get_history():
    """Get conversation history"""
    try:
        limit = request.args.get('limit', default=50, type=int)
        return jsonify({
            "history": conversation_history[-limit:],
            "total": len(conversation_history)
        }), 200
    except Exception as e:
        logger.error(f"History error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/clear', methods=['POST'])
def clear_data():
    """Clear all data"""
    try:
        global conversation_history, tasks, notes
        conversation_history = []
        tasks = []
        notes = []
        return jsonify({"message": "All data cleared"}), 200
    except Exception as e:
        logger.error(f"Clear error: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)