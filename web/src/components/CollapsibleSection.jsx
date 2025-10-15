// components/CollapsibleSection.tsx
import React, { useState } from "react";

export default function CollapsibleSection({
  title = "How the Belief Map Works",
  children,
}) {
  const [open, setOpen] = useState(false);

  return (
    <section className="container">
      <div
        className={`collapsible ${open ? "open" : ""}`}
        onClick={() => setOpen(o => !o)}
        role="button"
        aria-expanded={open}
      >
        <div className="collapsible-header">
          <h3>{title}</h3>
          <span className="chevron" aria-hidden>▾</span>
        </div>
        <div className="collapsible-body">
          {children}
        </div>
      </div>
    </section>
  );
}
