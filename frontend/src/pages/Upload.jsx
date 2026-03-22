import { useState, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { uploadAPI } from '../services/api';
import toast from 'react-hot-toast';
import {
  HiOutlineDocumentArrowUp,
  HiOutlineSparkles,
  HiOutlineAcademicCap,
  HiOutlineTrophy,
} from 'react-icons/hi2';
import './Upload.css';

const MODES = [
  {
    id: 'kids',
    label: 'Kids Mode',
    icon: <HiOutlineSparkles />,
    emoji: '🎈',
    desc: 'Simple, story-like explanations',
    color: '#f472b6',
  },
  {
    id: 'student',
    label: 'Student Mode',
    icon: <HiOutlineAcademicCap />,
    emoji: '📚',
    desc: 'Balanced and thorough',
    color: '#818cf8',
  },
  {
    id: 'exam',
    label: 'Exam Mode',
    icon: <HiOutlineTrophy />,
    emoji: '🎯',
    desc: 'Concise, key points only',
    color: '#fbbf24',
  },
];

const PROCESSING_STEPS = [
  '📄 Extracting text & diagrams from PDF...',
  '🤖 Generating conversational script...',
  '📝 Creating summary & cheat sheet...',
  '🃏 Building flashcards...',
  '❓ Generating quiz questions...',
  '🎙️ Producing podcast audio...',
  '✅ Wrapping up...',
];

export default function Upload() {
  const [file, setFile] = useState(null);
  const [mode, setMode] = useState('student');
  const [uploading, setUploading] = useState(false);
  const [step, setStep] = useState(0);
  const [dragActive, setDragActive] = useState(false);
  const fileInputRef = useRef(null);
  const navigate = useNavigate();

  const handleDrop = (e) => {
    e.preventDefault();
    setDragActive(false);
    const f = e.dataTransfer.files[0];
    if (f && f.type === 'application/pdf') {
      setFile(f);
    } else {
      toast.error('Please upload a PDF file');
    }
  };

  const handleFileSelect = (e) => {
    const f = e.target.files[0];
    if (f) setFile(f);
  };

  const handleUpload = async () => {
    if (!file) return toast.error('Please select a PDF');
    setUploading(true);
    setStep(0);

    // Simulate step progression
    const interval = setInterval(() => {
      setStep((prev) => Math.min(prev + 1, PROCESSING_STEPS.length - 1));
    }, 4000);

    try {
      const res = await uploadAPI.uploadPdf(file, mode);
      clearInterval(interval);
      toast.success('Session created successfully!');
      navigate(`/session/${res.data.session_id}`);
    } catch (err) {
      clearInterval(interval);
      toast.error(err.response?.data?.detail || 'Upload failed');
      setUploading(false);
    }
  };

  return (
    <div className="page-container">
      <div className="page-header" style={{ textAlign: 'center' }}>
        <h1>Create New Session</h1>
        <p>Upload a PDF and choose your learning style</p>
      </div>

      {!uploading ? (
        <div className="upload-content animate-fade-in">
          {/* Drop Zone */}
          <div
            className={`drop-zone glass-card ${dragActive ? 'drag-active' : ''} ${file ? 'has-file' : ''}`}
            onDragOver={(e) => { e.preventDefault(); setDragActive(true); }}
            onDragLeave={() => setDragActive(false)}
            onDrop={handleDrop}
            onClick={() => fileInputRef.current?.click()}
          >
            <input
              ref={fileInputRef}
              type="file"
              accept=".pdf"
              onChange={handleFileSelect}
              hidden
            />
            <div className="drop-icon">
              <HiOutlineDocumentArrowUp />
            </div>
            {file ? (
              <div className="file-info">
                <p className="file-name">{file.name}</p>
                <p className="file-size">{(file.size / 1024 / 1024).toFixed(2)} MB</p>
              </div>
            ) : (
              <>
                <p className="drop-text">Drag & drop your PDF here</p>
                <p className="drop-hint">or click to browse</p>
              </>
            )}
          </div>

          {/* Mode Selector */}
          <div className="mode-selector">
            <h3>Choose Learning Mode</h3>
            <div className="mode-cards">
              {MODES.map((m) => (
                <div
                  key={m.id}
                  className={`mode-card glass-card ${mode === m.id ? 'selected' : ''}`}
                  onClick={() => setMode(m.id)}
                  style={{ '--mode-color': m.color }}
                >
                  <span className="mode-emoji">{m.emoji}</span>
                  <h4>{m.label}</h4>
                  <p>{m.desc}</p>
                </div>
              ))}
            </div>
          </div>

          {/* Submit */}
          <button
            className="btn btn-primary upload-btn"
            onClick={handleUpload}
            disabled={!file}
          >
            <HiOutlineSparkles /> Generate Podcast
          </button>
        </div>
      ) : (
        /* Processing Animation */
        <div className="processing-view animate-fade-in">
          <div className="processing-spinner-wrap">
            <div className="processing-spinner" />
            <div className="processing-icon">🎙️</div>
          </div>
          <h2>Creating Your Podcast</h2>
          <p className="processing-desc">This may take 1-3 minutes depending on the PDF size</p>
          <div className="processing-steps">
            {PROCESSING_STEPS.map((s, i) => (
              <div
                key={i}
                className={`processing-step ${i < step ? 'done' : i === step ? 'active' : ''}`}
              >
                {s}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
