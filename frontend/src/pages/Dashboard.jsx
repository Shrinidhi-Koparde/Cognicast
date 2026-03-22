import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { sessionsAPI } from '../services/api';
import SessionCard from '../components/SessionCard';
import toast from 'react-hot-toast';
import { HiOutlinePlus, HiOutlineSparkles } from 'react-icons/hi2';
import './Dashboard.css';

export default function Dashboard() {
  const [sessions, setSessions] = useState([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    loadSessions();
  }, []);

  const loadSessions = async () => {
    try {
      const res = await sessionsAPI.list();
      setSessions(res.data.sessions || []);
    } catch (err) {
      toast.error('Failed to load sessions');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="page-container">
      <div className="dashboard-header">
        <div className="page-header">
          <h1>Your Learning Sessions</h1>
          <p>Pick up where you left off or start something new</p>
        </div>
        <button className="btn btn-primary" onClick={() => navigate('/upload')}>
          <HiOutlinePlus /> New Session
        </button>
      </div>

      {loading ? (
        <div className="dashboard-loading">
          <div className="spinner" />
          <p>Loading your sessions...</p>
        </div>
      ) : sessions.length === 0 ? (
        <div className="dashboard-empty animate-fade-in">
          <div className="empty-icon">
            <HiOutlineSparkles />
          </div>
          <h2>No sessions yet</h2>
          <p>Upload your first PDF and transform it into an AI-powered podcast!</p>
          <button className="btn btn-primary" onClick={() => navigate('/upload')}>
            <HiOutlinePlus /> Create Your First Session
          </button>
        </div>
      ) : (
        <div className="sessions-grid">
          {sessions.map((session, i) => (
            <SessionCard key={session.id} session={session} />
          ))}
        </div>
      )}
    </div>
  );
}
