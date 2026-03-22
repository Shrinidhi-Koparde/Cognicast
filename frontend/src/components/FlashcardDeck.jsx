import { useState } from 'react';
import './FlashcardDeck.css';

export default function FlashcardDeck({ flashcards }) {
  const [current, setCurrent] = useState(0);
  const [flipped, setFlipped] = useState(false);

  if (!flashcards || flashcards.length === 0) {
    return <p className="empty-text">No flashcards generated</p>;
  }

  const card = flashcards[current];

  const next = () => {
    setFlipped(false);
    setTimeout(() => setCurrent((prev) => (prev + 1) % flashcards.length), 150);
  };

  const prev = () => {
    setFlipped(false);
    setTimeout(() => setCurrent((prev) => (prev - 1 + flashcards.length) % flashcards.length), 150);
  };

  return (
    <div className="flashcard-deck">
      <div className="flashcard-counter">
        Card {current + 1} of {flashcards.length}
      </div>

      <div
        className={`flashcard ${flipped ? 'flipped' : ''}`}
        onClick={() => setFlipped(!flipped)}
      >
        <div className="flashcard-inner">
          <div className="flashcard-front">
            <span className="flashcard-label">Question</span>
            <p>{card.front}</p>
          </div>
          <div className="flashcard-back">
            <span className="flashcard-label">Answer</span>
            <p>{card.back}</p>
          </div>
        </div>
      </div>

      <p className="flashcard-hint">Click to flip</p>

      <div className="flashcard-nav">
        <button className="btn btn-secondary" onClick={prev}>← Previous</button>
        <button className="btn btn-secondary" onClick={next}>Next →</button>
      </div>
    </div>
  );
}
