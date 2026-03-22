import './TranscriptView.css';

export default function TranscriptView({ conversation }) {
  if (!conversation || conversation.length === 0) {
    return <p className="empty-text">No transcript available</p>;
  }

  return (
    <div className="transcript-view">
      {conversation.map((turn, i) => (
        <div
          key={i}
          className={`transcript-bubble ${turn.speaker}`}
          style={{ animationDelay: `${i * 0.05}s` }}
        >
          <div className="bubble-avatar">
            {turn.speaker === 'student' ? '🎓' : '🧑‍🏫'}
          </div>
          <div className="bubble-content">
            <span className="bubble-speaker">
              {turn.speaker === 'student' ? 'Student' : 'Mentor'}
            </span>
            <p>{turn.text}</p>
          </div>
        </div>
      ))}
    </div>
  );
}
