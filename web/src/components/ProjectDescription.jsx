// components/ProjectDescription.tsx
import React from "react";

const ProjectDescription = () => {
  return (
    <section id="project" className="py-12 px-6 text-center">
      <h2 className="text-3xl font-bold mb-4">Project Description</h2>
      <p className="max-w-3xl mx-auto text-lg text-gray-700 dark:text-gray-300">
        Our project teaches a robot to <b>understand its surroundings</b> using
        its sensors and logical reasoning. The robot moves along a wall using a
        <b> PID controller</b> that keeps a steady distance while collecting
        sonar and infrared readings. These readings are processed through a{" "}
        <b>Bayesian Network</b> — a probabilistic model that helps the robot
        make decisions even with noisy data.
      </p>

      <p className="max-w-3xl mx-auto text-lg mt-4 text-gray-700 dark:text-gray-300">
        This allows the robot to:
        <ul className="list-disc list-inside text-left mt-2">
          <li>Estimate its distance from the wall as a probability distribution</li>
          <li>Decide whether it has just passed a door (about 10 cm ago)</li>
        </ul>
      </p>

      <div className="mt-10 flex justify-center">
        {/* <img
          src="/public/workflow-diagram.png"
          alt="Workflow Diagram"
          className="w-full max-w-3xl rounded-2xl shadow-md transition-all
                     dark:invert dark:brightness-90"
        /> */}
        HELOOOOO
      </div>

      <p className="mt-4 text-sm text-gray-600 dark:text-gray-400">
        Workflow: Sensors → PID Controller → Bayesian Network → Belief Map Output
      </p>
    </section>
  );
};

export default ProjectDescription;
