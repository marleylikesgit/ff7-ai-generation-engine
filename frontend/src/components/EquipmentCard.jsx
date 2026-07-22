export default function EquipmentCard({ label, value }) {
  return (
    <div className="equipment-row">
      <span className="equipment-label">{label}</span>
      <span className="equipment-value">{value || "—"}</span>
    </div>
  );
}
