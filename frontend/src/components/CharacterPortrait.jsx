import { useState } from "react";

function slugify(name) {
  return name.toLowerCase().replace(/\s+/g, "-");
}

export default function CharacterPortrait({ name }) {
  const [failed, setFailed] = useState(false);
  const src = `/portraits/${slugify(name)}.jpg`;

  if (failed) {
    const initial = name.trim().charAt(0).toUpperCase();
    return (
      <div className="portrait-fallback" aria-hidden="true">
        {initial}
      </div>
    );
  }

  return (
    <img
      className="portrait-image"
      src={src}
      alt={`${name} portrait`}
      onError={() => setFailed(true)}
    />
  );
}
