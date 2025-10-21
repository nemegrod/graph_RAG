from flask import Flask, render_template, request, redirect, url_for
import asyncio
import logging
from src.agents.jaguar_agent.jaguar_agent_af import get_jaguar_agent

# Suppress Werkzeug request logs
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app = Flask(__name__)

# Single-user POC: Global storage for one conversation thread and history
app.config['AGENT'] = None
app.config['THREAD'] = None
app.config['CHAT_HISTORY'] = []
app.config['ERROR'] = None


def get_agent():
    """Get or create the jaguar agent (singleton)"""
    if app.config['AGENT'] is None:
        app.config['AGENT'] = get_jaguar_agent()
    return app.config['AGENT']


def get_thread():
    """Get or create the conversation thread (singleton)"""
    if app.config['THREAD'] is None:
        agent = get_agent()
        app.config['THREAD'] = agent.get_new_thread()
    return app.config['THREAD']


@app.route('/')
def index():
    """Render the main chat interface"""
    error = app.config.get('ERROR')
    app.config['ERROR'] = None  # Clear error after displaying
    return render_template(
        'index.html', 
        chat_history=app.config['CHAT_HISTORY'],
        error=error
    )

@app.route('/chat', methods=['POST'])
def chat():
    """Handle chat messages"""
    try:
        # Get user message from form
        user_message = request.form.get('message', '').strip()
        
        if not user_message:
            return redirect(url_for('index'))
        
        # Get agent and thread (created on first use)
        agent = get_agent()
        thread = get_thread()
        
        # Run agent with the conversation thread
        response = asyncio.run(agent.run(user_message, thread=thread, store=True))
        
        # Extract assistant response
        assistant_response = response.text
        
        # Store messages in global chat history for UI display
        app.config['CHAT_HISTORY'].append({
            'role': 'user',
            'content': user_message
        })
        app.config['CHAT_HISTORY'].append({
            'role': 'assistant',
            'content': assistant_response
        })
        
        return redirect(url_for('index'))
        
    except Exception as e:
        app.config['ERROR'] = str(e)
        return redirect(url_for('index'))

@app.route('/clear', methods=['POST'])
def clear_chat():
    """Clear the chat history and start a new conversation"""
    try:
        # Get agent
        agent = get_agent()
        
        # Create new thread (replaces existing one)
        app.config['THREAD'] = agent.get_new_thread()
        
        # Clear chat history
        app.config['CHAT_HISTORY'] = []
        
        return redirect(url_for('index'))
        
    except Exception as e:
        app.config['ERROR'] = str(e)
        return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
