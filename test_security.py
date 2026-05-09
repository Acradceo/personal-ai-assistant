import unittest
import json
from backend.app import app, tasks, notes

class SecurityTests(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

        # Clear existing data and create some defaults
        tasks.clear()
        notes.clear()

        self.app.post('/api/tasks', json={'title': 'Test Task', 'description': 'desc'})
        self.app.post('/api/notes', json={'title': 'Test Note', 'content': 'content'})

    def test_task_mass_assignment(self):
        # Initial state check
        resp = self.app.get('/api/tasks')
        data = json.loads(resp.data)
        self.assertEqual(len(data['tasks']), 1)
        original_task = data['tasks'][0]
        self.assertEqual(original_task['id'], 1)
        original_created_at = original_task['created_at']

        # Attempt mass assignment
        update_data = {
            'title': 'Updated Title',
            'id': 999,
            'created_at': '2000-01-01T00:00:00',
            'admin': True
        }
        resp = self.app.put(f"/api/tasks/{original_task['id']}", json=update_data)
        self.assertEqual(resp.status_code, 200)

        # Check result
        resp = self.app.get('/api/tasks')
        data = json.loads(resp.data)
        updated_task = data['tasks'][0]

        # Allowed field updated
        self.assertEqual(updated_task['title'], 'Updated Title')

        # Disallowed fields NOT updated
        self.assertEqual(updated_task['id'], 1)
        self.assertEqual(updated_task['created_at'], original_created_at)
        self.assertNotIn('admin', updated_task)

    def test_note_mass_assignment(self):
        # Initial state check
        resp = self.app.get('/api/notes')
        data = json.loads(resp.data)
        self.assertEqual(len(data['notes']), 1)
        original_note = data['notes'][0]
        self.assertEqual(original_note['id'], 1)
        original_created_at = original_note['created_at']

        # Attempt mass assignment
        update_data = {
            'title': 'Updated Note Title',
            'id': 999,
            'created_at': '2000-01-01T00:00:00',
            'is_admin': True
        }
        resp = self.app.put(f"/api/notes/{original_note['id']}", json=update_data)
        self.assertEqual(resp.status_code, 200)

        # Check result
        resp = self.app.get('/api/notes')
        data = json.loads(resp.data)
        updated_note = data['notes'][0]

        # Allowed field updated
        self.assertEqual(updated_note['title'], 'Updated Note Title')

        # Disallowed fields NOT updated
        self.assertEqual(updated_note['id'], 1)
        self.assertEqual(updated_note['created_at'], original_created_at)
        self.assertNotIn('is_admin', updated_note)

if __name__ == '__main__':
    unittest.main()
