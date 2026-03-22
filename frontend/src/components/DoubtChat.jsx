import { useState } from 'react';
import { questionsAPI } from '../services/api';
import toast from 'react-hot-toast';
import { HiOutlinePaperAirplane } from 'react-icons/hi2';
import './DoubtChat.css';

export default function DoubtChat({ sessionId }) {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSend = async () => {
    if (!input.trim() || loading) return;
    const question = input.trim();
    setInput('');
    setMessages((prev) => [...prev, { role: 'user', text: question }]);
    setLoading(true);

    try {
      const res = await questionsAPI.ask(sessionId, question);
      setMessages((prev) => [...prev, { role: 'ai', text: res.data.answer }]);
    } catch (err) {
      toast.error('Failed to get answer');
      setMessages((prev) => [...prev, { role: 'ai', text: 'Sorry, I couldn\'t process your question. Please try again.' }]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="doubt-chat">
      <div className="doubt-header">
        <h4>💬 Ask a Doubt</h4>
        <p>Ask anything about the material</p>
      </div>

      <div className="doubt-messages">
        {messages.length === 0 && (
          <div className="doubt-empty">
            <p>Ask a question about the content and get AI-powered explanations!</p>
          </div>
        )}
        {messages.map((msg, i) => (
          <div key={i} className={`doubt-msg ${msg.role}`}>
            <div className="doubt-msg-avatar">
              {msg.role === 'user' ? '🎓' : '🤖'}
            </div>
            <div className="doubt-msg-content">
              <p>{msg.text}</p>
            </div>
          </div>
        ))}
        {loading && (
          <div className="doubt-msg ai">
            <div className="doubt-msg-avatar">🤖</div>
            <div className="doubt-msg-content">
              <div className="typing-indicator">
                <span /><span /><span />
              </div>
            </div>
          </div>
        )}
      </div>

      <div className="doubt-input-bar">
        <input
          type="text"
          className="input-field"
          placeholder="Type your question..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          disabled={loading}
        />
        <button
          className="btn btn-primary doubt-send"
          onClick={handleSend}
          disabled={!input.trim() || loading}
        >
          <HiOutlinePaperAirplane />
        </button>
      </div>
    </div>
  );
}
