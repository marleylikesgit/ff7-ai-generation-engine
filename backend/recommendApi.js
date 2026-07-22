const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || "http://localhost:8000";

export async function fetchCharacters() {
  const res = await fetch(`${API_BASE_URL}/characters`);
  if (!res.ok) throw new Error("Failed to load characters");
  return res.json();
}

export async function fetchGameStages() {
  const res = await fetch(`${API_BASE_URL}/game-stages`);
  if (!res.ok) throw new Error("Failed to load game stages");
  return res.json();
}

export async function fetchRecommendation(characterNames, playstyleHint, gameStage) {
  const res = await fetch(`${API_BASE_URL}/recommend`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      character_names: characterNames,
      playstyle_hint: playstyleHint || null,
      game_stage: gameStage || "late",
    }),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || "Failed to generate recommendation");
  }
  return res.json();
}
