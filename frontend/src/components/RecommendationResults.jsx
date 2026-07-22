import MateriaCard from "./MateriaCard";
import EquipmentCard from "./EquipmentCard";

export default function RecommendationResults({ result }) {
  if (!result) return null;

  return (
    <div className="results">
      <div className="team-summary">
        <span className="eyebrow">Reasoning</span>
        <p>{result.team_summary}</p>
      </div>

      <div className="loadout-grid">
        {result.loadouts.map((loadout) => (
          <div className="loadout-card" key={loadout.character}>
            <h3>{loadout.character}</h3>

            <div className="equipment-block">
              <EquipmentCard label="Weapon" value={loadout.weapon} />
              <EquipmentCard label="Armor" value={loadout.armor} />
              <EquipmentCard label="Accessory" value={loadout.accessory} />
            </div>

            <div className="materia-block">
              {loadout.materia.map((m) => (
                <MateriaCard key={m} name={m} type="independent" />
              ))}
            </div>

            <p className="rationale">{loadout.rationale}</p>
          </div>
        ))}
      </div>

      {result.retrieved_notes?.length > 0 && (
        <div className="sources">
          <span className="eyebrow">Extra Notes</span>
          <ul>
            {result.retrieved_notes.map((title) => (
              <li key={title}>{title}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
