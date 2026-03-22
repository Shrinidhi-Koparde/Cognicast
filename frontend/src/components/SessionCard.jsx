import { useNavigate } from 'react-router-dom';
import { HiOutlineClock, HiOutlinePlay } from 'react-icons/hi2';
import './SessionCard.css';

export default function SessionCard({ session }) {
  const navigate = useNavigate();

  const modeLabels = { kids: '🎈 Kids', student: '📚 Student', exam: '🎯 Exam' };
  const modeClass = `badge badge-${session.mode}`;
  const statusClass = `badge badge-${session.status}`;

  const formatDate = (dateStr) => {
    try {
      const d = new Date(dateStr);
      return d.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
    } catch { return dateStr; }
  };

  return (
    <div
      className="session-card glass-card"
      onClick={() => session.status === 'completed' && navigate(`/session/${session.id}`)}
      role="button"
      tabIndex={0}
    >
      <div className="session-card-header">
        <span className={modeClass}>{modeLabels[session.mode] || session.mode}</span>
        <span className={statusClass}>{session.status}</span>
      </div>
      <h3 className="session-card-title">{session.title}</h3>
      <div className="session-card-footer">
        <span className="session-date">
          <HiOutlineClock /> {formatDate(session.created_at)}
        </span>
        {session.status === 'completed' && (
          <div className="session-play-btn">
            <HiOutlinePlay /> Listen
          </div>
        )}
      </div>
    </div>
  );
}
