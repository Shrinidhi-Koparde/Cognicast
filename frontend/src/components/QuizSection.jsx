import { useState } from 'react';
import { HiOutlineCheck, HiOutlineXMark } from 'react-icons/hi2';
import './QuizSection.css';

export default function QuizSection({ quiz }) {
  const [answers, setAnswers] = useState({});
  const [showResults, setShowResults] = useState(false);

  if (!quiz || quiz.length === 0) {
    return <p className="empty-text">No quiz generated</p>;
  }

  const handleSelect = (qIndex, oIndex) => {
    if (showResults) return;
    setAnswers({ ...answers, [qIndex]: oIndex });
  };

  const score = Object.keys(answers).reduce((acc, qIdx) => {
    return acc + (answers[qIdx] === quiz[Number(qIdx)].correct_index ? 1 : 0);
  }, 0);

  return (
    <div className="quiz-section">
      <div className="quiz-header">
        <h3>📝 Knowledge Check</h3>
        {showResults && (
          <div className="quiz-score">
            Score: <strong>{score} / {quiz.length}</strong>
          </div>
        )}
      </div>

      <div className="quiz-questions">
        {quiz.map((q, qIdx) => (
          <div key={qIdx} className="quiz-question glass-card">
            <p className="question-text">
              <span className="q-number">Q{qIdx + 1}.</span> {q.question}
            </p>
            <div className="question-options">
              {q.options.map((opt, oIdx) => {
                const selected = answers[qIdx] === oIdx;
                const isCorrect = q.correct_index === oIdx;
                let cls = 'option-btn';
                if (showResults && selected && isCorrect) cls += ' correct';
                else if (showResults && selected && !isCorrect) cls += ' wrong';
                else if (showResults && isCorrect) cls += ' correct-hint';
                else if (selected) cls += ' selected';

                return (
                  <button
                    key={oIdx}
                    className={cls}
                    onClick={() => handleSelect(qIdx, oIdx)}
                  >
                    <span className="option-text">{opt}</span>
                    {showResults && selected && isCorrect && <HiOutlineCheck className="option-icon correct-icon" />}
                    {showResults && selected && !isCorrect && <HiOutlineXMark className="option-icon wrong-icon" />}
                  </button>
                );
              })}
            </div>
            {showResults && q.explanation && (
              <p className="question-explanation">💡 {q.explanation}</p>
            )}
          </div>
        ))}
      </div>

      <button
        className="btn btn-primary quiz-submit"
        onClick={() => setShowResults(true)}
        disabled={Object.keys(answers).length < quiz.length || showResults}
      >
        {showResults ? `Score: ${score}/${quiz.length}` : 'Check Answers'}
      </button>

      {showResults && (
        <button
          className="btn btn-secondary"
          style={{ marginTop: '12px', width: '100%' }}
          onClick={() => { setAnswers({}); setShowResults(false); }}
        >
          Retry Quiz
        </button>
      )}
    </div>
  );
}
