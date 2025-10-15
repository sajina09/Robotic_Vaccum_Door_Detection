import React, { useEffect, useState } from "react";
import CollapsibleSection from "./components/CollapsibleSection";

const Nav = ({ theme, onToggle }) => (
  <nav className="nav">
    <a href="#home" className="brand">
      BayesBot Navigator
    </a>
    <div className="links">
      <a href="#project">Project</a>
      <a href="#description">Description</a>
      <a href="#methods">Methods</a>
      <a href="#demo">Demo</a>
      <a href="#team">Team</a>
      <button className="toggle" onClick={onToggle}>
        {theme === "blue" ? "Girl" : "Guy"} Mode
      </button>
    </div>
  </nav>
);

const Hero = () => (
  <header className="hero" id="home">
    <div className="hero-inner">
      <div className="hero-text">
        <h1 className="hero-title">
          BayesBot Navigator — The Self-Learning Indoor Robot
        </h1>
        <p className="hero-desc">
          BayesBot Navigator is an intelligent indoor robot that learns its
          surroundings through sensor fusion and Bayesian reasoning. It maps
          rooms, adapts to obstacles, and refines its understanding with every
          move — blending robotics, AI, and probability into one self-learning
          system.
        </p>
        <a href="#project" className="cta">
          Explore the Project
        </a>
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
          BayesBot learns a probabilistic map of rooms and hallways and updates
          its belief over location using sensor fusion (IR, bumpers) and a
          Bayesian filter.
        </p>
        <div className="actions">
          <a className="btn" href="#description">
            Learn More
          </a>
          <a className="link" href="#methods">
            See Methods
          </a>
        </div>
      </div>
      <div
        className="image-card"
        role="img"
        aria-label="Robot placeholder"
      ></div>
    </div>
  </section>
);

const ProjectDescription = () => (
  <section id="description" className="container text-center">
    <h3 className="section-title">🧠 Project Description</h3>
    <p className="max-w-3xl mx-auto text-lg text-gray-700 dark:text-gray-300">
      Our project focuses on teaching the robot how to{" "}
      <b>understand its surroundings</b> using its sensors and reasoning. The
      robot moves along a wall using a <b>PID controller</b> that keeps a steady
      distance, while collecting sonar and infrared readings. These readings are
      processed using a <b>Bayesian Network</b> — a probabilistic model that
      helps the robot make intelligent decisions from uncertain data.
    </p>

    <p className="max-w-3xl mx-auto text-lg mt-4 text-gray-700 dark:text-gray-300">
      This allows the robot to:
      <ul className="list-disc list-inside text-left mt-2 inline-block text-gray-600 dark:text-gray-400">
        <li>
          Estimate its distance from the wall as a probability distribution
        </li>
        <li>Decide whether it just passed a door (~10 cm ago)</li>
      </ul>
    </p>
    <p className="mt-3 text-sm text-gray-600 dark:text-gray-400">
      Sensors → PID Controller → Bayesian Network → Belief Map Output
    </p>

    <div className="mt-8 flex justify-center px-4">
      <div className="w-full max-w-3xl">
        <img
          src="/Workflow.png"
          alt="Workflow Diagram"
          className="block mx-auto max-w-full h-auto object-scale-down rounded-xl shadow-lg"
          style={{
            display: "block",
            margin: "auto",
            maxWidth: "100%",
            height: "auto",
          }}
        />
      </div>
    </div>

    <h3 className="section-title">🤖 Robot in Use: Create3 robot </h3>
    <div className="mt-8 flex justify-center px-4">
      <div className="w-full max-w-3xl">
        <img
          src="/icreateRobo.jpg"
          alt="Create3 Robot"
          className="block mx-auto max-w-full h-auto object-scale-down rounded-xl shadow-lg"
          style={{
            display: "block",
            margin: "auto",
            maxWidth: "100%",
            height: "auto",
          }}
        />
      </div>
    </div>
    <p className="mt-2 text-gray-700 dark:text-gray-300">
      We used the iRobot Create 3 platform equipped with infrared sensors,
      bumpers, and PID-based motion control. Data from these sensors was logged
      and fused through a Bayesian Network to help the robot infer its
      surroundings and make intelligent navigation decisions in real time.
    </p>

    <h2 className="section-title">💻 Link to our Code</h2>

    <p className="mt-3 text-center">
      <a
        href="https://github.com/sajina09/Robotic_Vaccum_Door_Detection/tree/main"
        target="_blank"
        rel="noopener noreferrer"
        className="inline-block text-blue-600 dark:text-pink-400 font-semibold hover:underline hover:text-blue-800 transition-colors cursor-pointer"
      >
        View Project on GitHub 🚀
      </a>
    </p>
  </section>
);

const Methods = () => (
  <section id="methods" className="container">
    <div className="grid two">
      <div
        className="image-card plant"
        role="img"
        aria-label="Plant-like placeholder"
      ></div>
      <div className="card">
        <h3>Methods</h3>
        <ul className="bullets">
          <li>Bayesian filtering over discrete locations</li>
          <li>Sensor fusion: IR proximity + bumper booleans</li>
          <li>Online learning of transition/emission probabilities</li>
          <li>PID tuned motion with collision recovery</li>
        </ul>
        {/* <div className="actions">
          <a className="btn" href="#demo">
            See Demo
          </a>
          <span className="dot"></span>
          <span className="muted">Self-updating belief grid</span>
        </div> */}
      </div>
    </div>
  </section>
);

const Demo = () => (
  <section id="demo" className="container">
    <div className="feature-band">
      <h3 className="band-title">Real-Time Belief Updates</h3>
      <p className="band-sub">
        As BayesBot moves, it refines its posterior over the indoor map — from
        uncertainty to confident localization.
      </p>
      <a href="#team" className="cta ghost">
        Meet the Team
      </a>
    </div>
  </section>
);

const TEAM = [
  {
    name: "Asmaa Alqurashi",
    description: "Mapping & localization",
    emoji: "🗺️",
  },
  {
    name: "Jackson Contreras",
    description: "Sensor fusion & data",
    emoji: "📡",
  },
  { name: "Mirajul Islam", description: "Controls & planning", emoji: "🎛️" },
  { name: "Sajina Pathak", description: "Vision", emoji: "🤖" },
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
            style={{ display: "grid", placeItems: "center", fontSize: 28 }}
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
        <p className="muted small">
          © {new Date().getFullYear()} — For class demo use.
        </p>
      </div>
      <div>
        <h5>Links</h5>
        <ul>
          <li>
            <a href="#project">Project</a>
          </li>
          <li>
            <a href="#description">Description</a>
          </li>
          <li>
            <a href="#methods">Methods</a>
          </li>
          <li>
            <a href="#demo">Demo</a>
          </li>
          <li>
            <a href="#team">Team</a>
          </li>
        </ul>
      </div>
      <div>
        <h5>Contact</h5>
        <p className="muted small">aalqurashi2023@fit.edu</p>
        <p className="muted small">islamm2024@fit.edu</p>
        <p className="muted small">jcontreras2010@fit.edu</p>
        <p className="muted small">spathak2024@fit.edu</p>
      </div>
    </div>
  </footer>
);

export default function App() {
  const [theme, setTheme] = useState("blue");
  useEffect(() => {
    document.documentElement.setAttribute("data-theme", theme);
  }, [theme]);

  return (
    <>
      <Nav
        theme={theme}
        onToggle={() => setTheme((t) => (t === "blue" ? "pink" : "blue"))}
      />
      <Hero />
      <Project />
      <ProjectDescription />
      <Methods />

      <Demo />
      <Team />
      <Footer />
    </>
  );
}
