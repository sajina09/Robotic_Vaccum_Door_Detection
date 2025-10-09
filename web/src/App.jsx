import React, { useEffect, useState } from 'react';

const Nav = ({ theme, onToggle }) => (
  <nav className="nav">
    <a href="#home" className="brand">BayesBot Navigator</a>
    <div className="links">
      <a href="#project">Project</a>
      <a href="#methods">Methods</a>
      <a href="#demo">Demo</a>
      <a href="#team">Team</a>
      <button className="toggle" onClick={onToggle}>
        {theme === 'blue' ? 'Girl' : 'Guy'} Mode
      </button>
    </div>
  </nav>
);

const Hero = () => (
  <header className="hero" id="home">
    <div className="hero-inner">
      <div className="hero-text">
        <h1 className="hero-title">BayesBot Navigator — The Self-Learning Indoor Robot</h1>
        <p className="hero-desc">
          Minimal single-page React site inspired by your reference layout. Smooth-scroll nav,
          responsive blocks, and a one-click theme toggle (blue ↔ pink).
        </p>
        <a href="#project" className="cta">Explore the Project</a>
      </div>
      <div className="hero-art" aria-hidden="true">
        <div className="ball"></div>
        <div className="lamp"></div>
        <div className="chair"></div>
      </div>
    </div>
  </header>
);

const Project = () => (
  <section id="project" className="container">
    <div className="grid two">
      <div className="card">
        <h3>Goal</h3>
        <p>
          BayesBot learns a probabilistic map of rooms and hallways and updates its belief
          over location using sensor fusion (IR, bumpers) and a Bayesian filter.
        </p>
        <div className="actions">
          <a className="btn" href="#methods">See Methods</a>
          <a className="link" href="#demo">Watch Demo</a>
        </div>
      </div>
      <div className="image-card" role="img" aria-label="Chair-like placeholder"></div>
    </div>
  </section>
);

const Methods = () => (
  <section id="methods" className="container">
    <div className="grid two">
      <div className="image-card plant" role="img" aria-label="Plant-like placeholder"></div>
      <div className="card">
        <h3>Methods</h3>
        <ul className="bullets">
          <li>Bayesian filtering over discrete locations</li>
          <li>Sensor fusion: IR proximity + bumper booleans</li>
          <li>Online learning of transition/emission probabilities</li>
          <li>PID tuned motion with collision recovery</li>
        </ul>
        <div className="actions">
          <a className="btn" href="#demo">See Demo</a>
          <span className="dot"></span>
          <span className="muted">Self-updating belief grid</span>
        </div>
      </div>
    </div>
  </section>
);

const Demo = () => (
  <section id="demo" className="container">
    <div className="feature-band">
      <h3 className="band-title">Real-Time Belief Updates</h3>
      <p className="band-sub">
        As BayesBot moves, it refines its posterior over the indoor map — from uncertainty
        to confident localization.
      </p>
      <a href="#team" className="cta ghost">Meet the Team</a>
    </div>
  </section>
);


const TEAM = [
  { name: 'Asmaa Alqurashi',  description: 'Mapping & localization',  emoji: '🗺️' },
  { name: 'Jackson Contreras', description: 'Sensor fusion & data',    emoji: '📡' },
  { name: 'Mirajul Islam',     description: 'Controls & planning',     emoji: '🎛️' },
  { name: 'Sajina Pathak',     description: 'Vision',   emoji: '🤖' },
];


const Team = () => (
  <section id="team" className="container team">
    <h3 className="section-title">About Our Team</h3>
    <div className="grid four">
      {TEAM.map((m, i) => (
        <div className="card person" key={i}>
          <div
            className="avatar"
            aria-hidden="true"
            style={{ display: 'grid', placeItems: 'center', fontSize: 28 }}
          >
            {m.emoji}
          </div>
          <h4>{m.name}</h4>
          <p className="muted">{m.description}</p>
        </div>
      ))}
    </div>
  </section>
);


const Footer = () => (
  <footer className="footer">
    <div className="cols">
      <div>
        <h5>BayesBot Navigator</h5>
        <p className="muted small">© {new Date().getFullYear()} — For class demo use.</p>
      </div>
      <div>
        <h5>Links</h5>
        <ul>
          <li><a href="#project">Project</a></li>
          <li><a href="#methods">Methods</a></li>
          <li><a href="#demo">Demo</a></li>
          <li><a href="#team">Team</a></li>
        </ul>
      </div>
      <div>
        <h5>Contact</h5>
        <p className="muted small">team@bayesbot.local</p>
      </div>
    </div>
  </footer>
);

export default function App() {
  const [theme, setTheme] = useState('blue');
  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme);
  }, [theme]);

  return (
    <>
      <Nav theme={theme} onToggle={() => setTheme(t => (t === 'blue' ? 'pink' : 'blue'))} />
      <Hero />
      <Project />
      <Methods />
      <Demo />
      <Team />
      <Footer />
    </>
  );
}
