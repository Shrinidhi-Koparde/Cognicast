import './DiagramViewer.css';

export default function DiagramViewer({ diagrams }) {
  if (!diagrams || diagrams.length === 0) {
    return <p className="empty-text">No diagrams extracted from this PDF</p>;
  }

  return (
    <div className="diagram-viewer">
      <div className="diagram-grid">
        {diagrams.map((b64, i) => (
          <div key={i} className="diagram-item glass-card">
            <img
              src={`data:image/png;base64,${b64}`}
              alt={`Diagram ${i + 1}`}
              loading="lazy"
            />
            <span className="diagram-label">Figure {i + 1}</span>
          </div>
        ))}
      </div>
    </div>
  );
}
