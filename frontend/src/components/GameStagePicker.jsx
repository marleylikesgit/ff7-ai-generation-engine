import { useEffect, useState } from "react";
import { fetchGameStages } from "../api/recommendApi";

export default function GameStagePicker({ selectedStage, onChange }) {
  const [stages, setStages] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchGameStages()
      .then((data) => {
        setStages(data);
        if (!selectedStage && data.length > 0) {
          onChange(data[data.length - 1].id); 
        }
      })
      .finally(() => setLoading(false));
  }, []);

  if (loading) return null;

  return (
    <div className="stage-picker">
      <span className="playstyle-label" style={{ marginBottom: 8, display: "block" }}>
        How far are you in the story?
      </span>
      <div className="stage-options">
        {stages.map((stage) => (
          <button
            key={stage.id}
            className={`stage-button ${selectedStage === stage.id ? "is-selected" : ""}`}
            onClick={() => onChange(stage.id)}
            type="button"
          >
            <span className="stage-label">{stage.label}</span>
            <span className="stage-description">{stage.description}</span>
          </button>
        ))}
      </div>
    </div>
  );
}
