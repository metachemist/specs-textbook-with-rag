// @ts-check

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

/**
 * Creating a sidebar enables you to:
 - create an ordered group of docs
 - render a sidebar for each doc of that group
 - provide next/previous navigation

 The sidebars can be generated from the filesystem, or explicitly defined here.

 Create as many sidebars as you want.

 @type {import('@docusaurus/plugin-content-docs').SidebarsConfig}
 */
const sidebars = {
  textbook: [
    {
      type: 'category',
      label: 'Introduction',
      items: [
        'introduction/physical-ai-foundations',
      ],
    },
    {
      type: 'category',
      label: 'Module 1: The Robotic Nervous System (ROS 2)',
      items: [
        'module-1-ros2/nodes-and-topics',
        'module-1-ros2/urdf-humanoids',
      ],
    },
    {
      type: 'category',
      label: 'Module 2: The Digital Twin (Gazebo & Unity)',
      items: [
        'module-2-digital-twin/gazebo-physics',
        'module-2-digital-twin/unity-integration',
      ],
    },
    {
      type: 'category',
      label: 'Module 3: The AI-Robot Brain (NVIDIA Isaac)',
      items: [
        'module-3-nvidia-isaac/isaac-sim-setup',
        'module-3-nvidia-isaac/nav2-path-planning',
      ],
    },
    {
      type: 'category',
      label: 'Module 4: Vision-Language-Action (VLA)',
      items: [
        'module-4-vla/voice-to-action',
        'module-4-vla/llm-cognitive-planning',
      ],
    },
    {
      type: 'category',
      label: 'Capstone Project: The Autonomous Humanoid',
      items: [
        'capstone/autonomous-humanoid',
      ],
    },
  ],
};

export default sidebars;
