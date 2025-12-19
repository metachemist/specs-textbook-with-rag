# Docusaurus Development Plan: Physical AI & Humanoid Robotics Textbook

**Branch**: `001-textbook-rag-platform` | **Date**: 2025-12-19 | **Spec**: [link to spec](../specs/001-textbook-rag-platform/spec.md)
**Input**: Feature specification from `/specs/001-textbook-rag-platform/spec.md`

## Summary

This plan outlines the development of a Docusaurus-based interactive textbook for Physical AI & Humanoid Robotics. The implementation will follow the curriculum structure specified in the feature requirements, with integration of RAG chatbot, personalization, and localization features. The project will adhere to the architecture standards defined in the project constitution with separate /web and /server directories.

## Technical Context

**Language/Version**: TypeScript 5.0+, Node.js 18+
**Primary Dependencies**: Docusaurus 3.x, React 18+, Tailwind CSS 3.x, Better Auth, OpenAI SDK
**Storage**: N/A (content will be static markdown files initially)
**Testing**: Jest, React Testing Library
**Target Platform**: Web (client-side rendered static site)
**Project Type**: Web application with Docusaurus frontend
**Performance Goals**: Page load times < 3 seconds, 90% of queries answered within 10 seconds
**Constraints**: Must support Urdu localization, personalization based on user background
**Scale/Scope**: Support 100+ concurrent users, 5 modules with multiple lessons each

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- Tech Stack Adherence: Verify all technology choices align with mandated stack (Docusaurus, FastAPI, Pydantic, Neon, Qdrant, OpenAI Agents/ChatKit, Better Auth)
- Architecture Compliance: Ensure modular separation of /server and /web directories
- Agentic Workflow: Confirm adherence to PEP 8, Prettier, error handling, and Mermaid.js diagram requirements
- Testing Requirements: Verify test-first approach and integration testing coverage
- Observability: Confirm logging and error handling for external API calls

## Project Structure

### Documentation (this feature)

```text
specs/[###-feature]/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
# Web application: Docusaurus frontend
web/
├── docs/
│   ├── 01-introduction/
│   │   └── 01-physical-ai-foundations.md
│   ├── 02-module-1-ros2/
│   │   ├── 01-nodes-and-topics.md
│   │   └── 02-urdf-humanoids.md
│   ├── 03-module-2-digital-twin/
│   │   ├── 01-gazebo-physics.md
│   │   └── 02-unity-integration.md
│   ├── 04-module-3-nvidia-isaac/
│   │   ├── 01-isaac-sim-setup.md
│   │   └── 02-nav2-path-planning.md
│   ├── 05-module-4-vla/
│   │   ├── 01-voice-to-action.md
│   │   └── 02-llm-cognitive-planning.md
│   └── 06-capstone/
│       └── 01-autonomous-humanoid.md
├── src/
│   ├── components/
│   │   ├── ChatBotWidget/
│   │   ├── PersonalizeButton/
│   │   └── TranslateButton/
│   ├── pages/
│   └── css/
├── static/
├── docusaurus.config.ts
├── sidebars.ts
├── package.json
└── tsconfig.json

server/
├── src/
│   ├── models/
│   ├── services/
│   ├── api/
│   └── utils/
├── tests/
│   ├── unit/
│   ├── integration/
│   └── contract/
├── requirements.txt
└── main.py

# Shared resources
config/
├── qdrant_config.yaml
└── deployment/
    ├── github-pages/
    └── railway/
```

**Structure Decision**: Following the mandated architecture of separate /web (Docusaurus) and /server (FastAPI) directories to ensure modularity and adherence to agentic workflow rules.

## Docusaurus Development Plan

### 1. Docusaurus Setup & Configuration

#### Initialize Docusaurus Project
```bash
# Create web directory and initialize Docusaurus
mkdir web
cd web
npm init docusaurus ./website classic
# Choose TypeScript support during initialization
```

#### Install Tailwind CSS
```bash
# Install Tailwind CSS and its dependencies
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
```

#### Configure Tailwind CSS
1. Update `tailwind.config.js`:
```js
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
    "./docs/**/*.{md,mdx}",
    "./blog/**/*.{md,mdx}",
    "./pages/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
```

2. Update `src/css/custom.css` to include Tailwind directives:
```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

#### Configure Docusaurus
1. Update `docusaurus.config.ts` with the project title:
```ts
const config = {
  title: 'Physical AI & Humanoid Robotics',
  tagline: 'An Interactive Textbook',
  // ... rest of configuration
};
```

2. Clean up default template by removing unnecessary blog/docs folders and content

#### Update Dependencies
```bash
# Install additional dependencies for the features
npm install @docusaurus/module-type-aliases @docusaurus/types
npm install react-icons # for UI icons
```

### 2. Content Development Phases (The Syllabus)

#### Phase A: The Nervous System (Module 1) - ROS 2, Nodes, Topics, URDF
- Create content for ROS 2 fundamentals
- Document Nodes, Topics, and Services
- Explain URDF for humanoid robots
- Implement rclpy examples

#### Phase B: The Digital Twin (Module 2) - Gazebo physics, Unity, Sensors
- Create content for physics simulation
- Document Gazebo setup and configuration
- Explain LiDAR and camera simulation
- Cover Unity integration approaches

#### Phase C: The AI Brain (Module 3) - NVIDIA Isaac Sim, Nav2
- Document Isaac Sim setup and usage
- Explain Isaac ROS components
- Cover Nav2 navigation system
- Explain VSLAM concepts

#### Phase D: VLA & Capstone (Module 4) - Voice-to-Action, LLM Planning, Final Project
- Create content for Voice-to-Action with Whisper
- Document cognitive planning with LLMs
- Explain LLMs to ROS 2 integration
- Develop capstone project guidelines

### 3. Strict File Structure (The Architecture)

```
web/
  /docs
    /01-introduction
       - 01-physical-ai-foundations.md
    /02-module-1-ros2
       - 01-nodes-and-topics.md
       - 02-urdf-humanoids.md
    /03-module-2-digital-twin
       - 01-gazebo-physics.md
       - 02-unity-integration.md
    /04-module-3-nvidia-isaac
       - 01-isaac-sim-setup.md
       - 02-nav2-path-planning.md
    /05-module-4-vla
       - 01-voice-to-action.md
       - 02-llm-cognitive-planning.md
    /06-capstone
       - 01-autonomous-humanoid.md
  /src
    /components
      - ChatBotWidget.tsx
      - PersonalizeButton.tsx
      - TranslateButton.tsx
```

### 4. Component Development Requirements

#### Create React Components for Bonus Features
1. `/src/components/ChatBotWidget/` - RAG chatbot interface
2. `/src/components/PersonalizeButton/` - Button to personalize content
3. `/src/components/TranslateButton/` - Button to translate content to Urdu

#### Component Specifications
- Each component must be TypeScript compatible
- Components must follow accessibility standards
- Components must be responsive and work with Tailwind CSS
- Components must integrate with the Docusaurus environment

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |