import { useEffect, useState } from "react";
import { fetchCharacters } from "../api/recommendApi";
import CharacterPortrait from "./CharacterPortrait";

export default function CharacterPicker({ selected, onChange, playstyleHint, onPlaystyleChange }) {
  const [characters, setCharacters] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchCharacters()
      .then(setCharacters)
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, []);

  function toggle(name) {
    if (selected.includes(name)) {
      onChange(selected.filter((n) => n !== name));
    } else if (selected.length < 3) {
      onChange([...selected, name]);
    }
  }

  if (loading) return <p className="status-text">Loading party...</p>;
  if (error) return <p className="status-text status-error">{error}</p>;

  return (
    <div className="picker">
      <div className="picker-header">
        <h2>Choose your party</h2>
        <span className="picker-count">{selected.length} / 3 selected</span>
      </div>

      <div className="character-grid">
        {characters.map((c) => {
          const isSelected = selected.includes(c.name);
          const disabled = !isSelected && selected.length >= 3;
          return (
            <button
              key={c.id}
              className={`character-tile ${isSelected ? "is-selected" : ""}`}
              disabled={disabled}
              onClick={() => toggle(c.name)}
              title={c.strengths}
            >
              <CharacterPortrait name={c.name} />
              <span className="character-name">{c.name}</span>
              <span className="character-role">{c.role_archetype}</span>
            </button>
          );
        })}
      </div>

      <label className="playstyle-label">
        Playstyle preference (optional)
        <input
          type="text"
          placeholder="e.g. heavy elemental magic, large dps, long range build"
          value={playstyleHint}
          onChange={(e) => onPlaystyleChange(e.target.value)}
        />
      </label>
    </div>
  );
}
