from flask import Flask, render_template, request, jsonify, session
from models import ChatHistory
from llm_service import LLMService
import uuid

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this-in-production'  # Change this in production

# Initialize LLM service
llm_service = LLMService()

# Store chat histories per session
chat_sessions = {}

@app.route('/')
def index():
    """Render the main chat interface"""
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    """Handle chat messages"""
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({'error': 'Empty message'}), 400
        
        # Get or create session ID
        session_id = session.get('session_id')
        if not session_id:
            session_id = str(uuid.uuid4())
            session['session_id'] = session_id
            chat_sessions[session_id] = ChatHistory()
        
        # Get chat history for this session
        chat_history = chat_sessions.get(session_id, ChatHistory())
        
        # Get response from LLM
        assistant_response = llm_service.get_chat_response(chat_history, user_message)
        
        # Update session storage
        chat_sessions[session_id] = chat_history
        
        return jsonify({
            'user_message': user_message,
            'assistant_response': assistant_response,
            'success': True
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/clear', methods=['POST'])
def clear_chat():
    """Clear the chat history"""
    try:
        session_id = session.get('session_id')
        if session_id and session_id in chat_sessions:
            chat_sessions[session_id].clear()
        
        return jsonify({'success': True, 'message': 'Chat history cleared'})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/history', methods=['GET'])
def get_history():
    """Get chat history for current session"""
    try:
        session_id = session.get('session_id')
        if session_id and session_id in chat_sessions:
            chat_history = chat_sessions[session_id]
            messages = [
                {
                    'role': msg.role,
                    'content': msg.content,
                    'timestamp': msg.timestamp.isoformat()
                }
                for msg in chat_history.messages
            ]
            return jsonify({'messages': messages, 'success': True})
        else:
            return jsonify({'messages': [], 'success': True})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
