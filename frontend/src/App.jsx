import { useState } from "react";
import CharacterPicker from "./components/CharacterPicker";
import GameStagePicker from "./components/GameStagePicker";
import RecommendationResults from "./components/RecommendationResults";
import { fetchRecommendation } from "./api/recommendApi";
import "./App.css";

export default function App() {
  const [selected, setSelected] = useState([]);
  const [playstyleHint, setPlaystyleHint] = useState("");
  const [gameStage, setGameStage] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  async function handleGenerate() {
    setLoading(true);
    setError(null);
    setResult(null);
    try {
      const data = await fetchRecommendation(selected, playstyleHint, gameStage);
      setResult(data);
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="app-shell">
      <header className="app-header">
        <span className="eyebrow">Midgar's Materia</span>
        <h1>Marley's FF7 Build Generator</h1>
        <p className="subtitle">
          Select 3 characters and I will generate optimal selection of materia
          and equipment for you to use on your journey.
        </p>
      </header>

      <CharacterPicker
        selected={selected}
        onChange={setSelected}
        playstyleHint={playstyleHint}
        onPlaystyleChange={setPlaystyleHint}
      />

      <GameStagePicker selectedStage={gameStage} onChange={setGameStage} />

      <div className="generate-row">
        <button
          className="generate-button"
          disabled={selected.length !== 3 || loading}
          onClick={handleGenerate}
        >
          {loading ? "Lifestream is loading..." : "Generate Build"}
        </button>
        {error && <p className="status-text status-error">{error}</p>}
      </div>

      <RecommendationResults result={result} />
    </div>
  );
}
