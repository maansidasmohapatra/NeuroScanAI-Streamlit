// Horizontal bar chart of the four softmax output scores (no chart library needed).
export default function ScoreChart({ scores, topClass }) {
  return (
    <div className="chart" role="img" aria-label="Model output scores for the four classes">
      {scores.map((s) => {
        const pct = s.score * 100;
        const isTop = s.class === topClass;
        return (
          <div className="bar-row" key={s.class}>
            <div className="bar-label">{s.display_name}</div>
            <div className="bar-track">
              <div className={`bar-fill ${isTop ? "top" : ""}`} style={{ width: `${Math.max(pct, 0.5)}%` }} />
            </div>
            <div className={`bar-value ${isTop ? "top" : ""}`}>{pct.toFixed(1)}%</div>
          </div>
        );
      })}
    </div>
  );
}
