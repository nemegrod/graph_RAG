from flask import Flask, render_template, request, jsonify, session
import uuid
import asyncio
from src.agents.jaguar_agent.jaguar_agent_af import get_jaguar_agent

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this-in-production'  # Change this in production

# Initialize Agent Framework agent
agent = None  # Will be initialized lazily

# Store thread IDs per session (Agent Framework manages conversation history internally)
session_threads = {}

@app.route('/')
def index():
    """Render the main chat interface"""
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    """Handle chat messages"""
    global agent
    
    try:
        # Lazy initialization of agent
        if agent is None:
            agent = get_jaguar_agent()
        
        data = request.get_json()
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({'error': 'Empty message'}), 400
        
        # Get or create session ID and thread ID
        session_id = session.get('session_id')
        if not session_id:
            session_id = str(uuid.uuid4())
            session['session_id'] = session_id
            # Each session gets a unique thread ID for Agent Framework
            session_threads[session_id] = f"thread_{session_id}"
        
        thread_id = session_threads.get(session_id, f"thread_{session_id}")
        
        # Run agent asynchronously - Agent Framework manages history per thread
        assistant_response = asyncio.run(agent.run(user_message, thread_id=thread_id))
        
        return jsonify({
            'user_message': user_message,
            'assistant_response': assistant_response,
            'success': True
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/clear', methods=['POST'])
def clear_chat():
    """Clear the chat history by creating a new thread"""
    try:
        session_id = session.get('session_id')
        if session_id:
            # Create a new thread ID to start fresh conversation
            # Agent Framework maintains history per thread, so new thread = fresh start
            new_thread_id = f"thread_{uuid.uuid4()}"
            session_threads[session_id] = new_thread_id
            return jsonify({'success': True, 'message': 'Chat history cleared'})
        
        return jsonify({'success': True, 'message': 'No active session'})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/history', methods=['GET'])
def get_history():
    """Get chat history for current session"""
    try:
        session_id = session.get('session_id')
        thread_id = session_threads.get(session_id) if session_id else None
        
        if thread_id:
            # Agent Framework manages history internally per thread
            # For now, return thread info - history is maintained by the agent
            return jsonify({
                'messages': [],
                'success': True,
                'note': 'History is managed by Agent Framework per thread',
                'thread_id': thread_id
            })
        else:
            return jsonify({'messages': [], 'success': True})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
