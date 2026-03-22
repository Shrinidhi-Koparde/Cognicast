import { useRef, useState, useEffect } from 'react';
import { HiOutlinePlay, HiOutlinePause, HiOutlineForward, HiOutlineBackward } from 'react-icons/hi2';
import './AudioPlayer.css';

export default function AudioPlayer({ audioUrl }) {
  const audioRef = useRef(null);
  const [playing, setPlaying] = useState(false);
  const [currentTime, setCurrentTime] = useState(0);
  const [duration, setDuration] = useState(0);

  useEffect(() => {
    const audio = audioRef.current;
    if (!audio) return;
    const onTime = () => setCurrentTime(audio.currentTime);
    const onMeta = () => setDuration(audio.duration);
    const onEnd = () => setPlaying(false);
    audio.addEventListener('timeupdate', onTime);
    audio.addEventListener('loadedmetadata', onMeta);
    audio.addEventListener('ended', onEnd);
    return () => {
      audio.removeEventListener('timeupdate', onTime);
      audio.removeEventListener('loadedmetadata', onMeta);
      audio.removeEventListener('ended', onEnd);
    };
  }, [audioUrl]);

  const toggle = () => {
    if (!audioRef.current) return;
    if (playing) {
      audioRef.current.pause();
    } else {
      audioRef.current.play();
    }
    setPlaying(!playing);
  };

  const skip = (sec) => {
    if (audioRef.current) {
      audioRef.current.currentTime = Math.max(0, Math.min(duration, audioRef.current.currentTime + sec));
    }
  };

  const seek = (e) => {
    const rect = e.currentTarget.getBoundingClientRect();
    const pct = (e.clientX - rect.left) / rect.width;
    if (audioRef.current) {
      audioRef.current.currentTime = pct * duration;
    }
  };

  const fmt = (s) => {
    if (!s || isNaN(s)) return '0:00';
    const m = Math.floor(s / 60);
    const sec = Math.floor(s % 60);
    return `${m}:${sec.toString().padStart(2, '0')}`;
  };

  const apiBase = import.meta.env.VITE_API_URL || 'http://localhost:8000';

  return (
    <div className="audio-player glass-card">
      <audio ref={audioRef} src={audioUrl ? `${apiBase}${audioUrl}` : ''} preload="metadata" />

      <div className="player-controls">
        <button className="player-btn" onClick={() => skip(-10)} title="Back 10s">
          <HiOutlineBackward />
        </button>
        <button className="player-btn play-btn" onClick={toggle}>
          {playing ? <HiOutlinePause /> : <HiOutlinePlay />}
        </button>
        <button className="player-btn" onClick={() => skip(10)} title="Forward 10s">
          <HiOutlineForward />
        </button>
      </div>

      <div className="player-track" onClick={seek}>
        <div className="track-bar">
          <div
            className="track-progress"
            style={{ width: duration ? `${(currentTime / duration) * 100}%` : '0%' }}
          />
        </div>
        <div className="track-times">
          <span>{fmt(currentTime)}</span>
          <span>{fmt(duration)}</span>
        </div>
      </div>
    </div>
  );
}
