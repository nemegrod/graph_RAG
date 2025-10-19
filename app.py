from flask import Flask, render_template, request, jsonify, session, g
import uuid
import asyncio
from src.agents.jaguar_agent.jaguar_agent_af import get_jaguar_agent

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this-in-production'  # Change this in production

# Store thread IDs per session (Agent Framework manages conversation history internally)
app.config['SESSION_THREADS'] = {}


def get_agent():
    """Get or create the jaguar agent (singleton pattern using Flask app context)"""
    if 'agent' not in app.config:
        app.config['agent'] = get_jaguar_agent()
    return app.config['agent']

@app.route('/')
def index():
    """Render the main chat interface"""
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    """Handle chat messages"""
    try:
        # Get the agent instance
        agent = get_agent()
        
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
            app.config['SESSION_THREADS'][session_id] = f"thread_{session_id}"
        
        thread_id = app.config['SESSION_THREADS'].get(session_id, f"thread_{session_id}")
        
        # Run agent asynchronously - Agent Framework manages history per thread
        response = asyncio.run(agent.run(user_message, thread_id=thread_id))
        
        # Extract the text content from the AgentRunResponse object
        last_message = response.messages[-1] if response.messages else None
        if last_message:
            # Try different possible attributes
            assistant_response = (
                getattr(last_message, 'text', None) or
                getattr(last_message, 'content', None) or
                str(last_message)
            )
        else:
            assistant_response = ""
        
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
            app.config['SESSION_THREADS'][session_id] = new_thread_id
            return jsonify({'success': True, 'message': 'Chat history cleared'})
        
        return jsonify({'success': True, 'message': 'No active session'})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/history', methods=['GET'])
def get_history():
    """Get chat history for current session"""
    try:
        session_id = session.get('session_id')
        thread_id = app.config['SESSION_THREADS'].get(session_id) if session_id else None
        
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
