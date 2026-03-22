import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { sessionsAPI } from '../services/api';
import AudioPlayer from '../components/AudioPlayer';
import TranscriptView from '../components/TranscriptView';
import DiagramViewer from '../components/DiagramViewer';
import QuizSection from '../components/QuizSection';
import FlashcardDeck from '../components/FlashcardDeck';
import DoubtChat from '../components/DoubtChat';
import toast from 'react-hot-toast';
import {
  HiOutlineChatBubbleLeftRight,
  HiOutlineDocumentText,
  HiOutlinePhoto,
  HiOutlineClipboardDocumentList,
  HiOutlineRectangleStack,
  HiOutlineQuestionMarkCircle,
  HiOutlineChatBubbleOvalLeft,
  HiOutlineArrowLeft,
} from 'react-icons/hi2';
import './PodcastPlayer.css';

const TABS = [
  { id: 'transcript', icon: <HiOutlineChatBubbleLeftRight />, label: 'Transcript' },
  { id: 'summary', icon: <HiOutlineDocumentText />, label: 'Summary' },
  { id: 'cheatsheet', icon: <HiOutlineClipboardDocumentList />, label: 'Cheat Sheet' },
  { id: 'diagrams', icon: <HiOutlinePhoto />, label: 'Diagrams' },
  { id: 'flashcards', icon: <HiOutlineRectangleStack />, label: 'Flashcards' },
  { id: 'quiz', icon: <HiOutlineQuestionMarkCircle />, label: 'Quiz' },
  { id: 'doubt', icon: <HiOutlineChatBubbleOvalLeft />, label: 'Ask Doubt' },
];

export default function PodcastPlayer() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [session, setSession] = useState(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('transcript');

  useEffect(() => {
    loadSession();
  }, [id]);

  const loadSession = async () => {
    try {
      const res = await sessionsAPI.get(id);
      setSession(res.data);
    } catch (err) {
      toast.error('Failed to load session');
      navigate('/');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="page-container" style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '60vh' }}>
        <div className="spinner" />
      </div>
    );
  }

  if (!session) return null;

  const modeLabels = { kids: '🎈 Kids', student: '📚 Student', exam: '🎯 Exam' };

  return (
    <div className="player-page">
      {/* Header */}
      <div className="player-header">
        <button className="btn btn-ghost" onClick={() => navigate('/')}>
          <HiOutlineArrowLeft /> Back
        </button>
        <div className="player-title-area">
          <h1>{session.title}</h1>
          <span className={`badge badge-${session.mode}`}>{modeLabels[session.mode] || session.mode}</span>
        </div>
      </div>

      {/* Audio Player */}
      <AudioPlayer audioUrl={session.audio_url} />

      {/* Tab Navigation */}
      <div className="player-tabs">
        {TABS.map((tab) => (
          <button
            key={tab.id}
            className={`player-tab ${activeTab === tab.id ? 'active' : ''}`}
            onClick={() => setActiveTab(tab.id)}
          >
            {tab.icon}
            <span>{tab.label}</span>
          </button>
        ))}
      </div>

      {/* Tab Content */}
      <div className="player-content glass-card">
        {activeTab === 'transcript' && (
          <TranscriptView conversation={session.conversation} />
        )}

        {activeTab === 'summary' && (
          <div className="markdown-content">
            <h3>📋 Summary</h3>
            <div className="text-content">{session.summary || 'No summary available'}</div>
          </div>
        )}

        {activeTab === 'cheatsheet' && (
          <div className="markdown-content">
            <h3>⚡ Cheat Sheet</h3>
            <div className="text-content">{session.cheat_sheet || 'No cheat sheet available'}</div>
          </div>
        )}

        {activeTab === 'diagrams' && (
          <DiagramViewer diagrams={session.diagrams} />
        )}

        {activeTab === 'flashcards' && (
          <FlashcardDeck flashcards={session.flashcards} />
        )}

        {activeTab === 'quiz' && (
          <QuizSection quiz={session.quiz} />
        )}

        {activeTab === 'doubt' && (
          <DoubtChat sessionId={id} />
        )}
      </div>
    </div>
  );
}
