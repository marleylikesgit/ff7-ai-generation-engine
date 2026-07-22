const TYPE_COLORS = {
  magic: "var(--materia-magic)",
  support: "var(--materia-support)",
  command: "var(--materia-command)",
  independent: "var(--materia-independent)",
  summon: "var(--materia-summon)",
};

export default function MateriaCard({ name, type }) {
  const color = TYPE_COLORS[type?.toLowerCase()] || "var(--materia-independent)";
  return (
    <span className="materia-orb" style={{ "--orb-color": color }}>
      <span className="materia-orb-dot" />
      {name}
    </span>
  );
}
