---
id: 1
title: hackathon-project-constitution
stage: constitution
date: 2025-12-19
surface: agent
model: Qwen
feature: none
branch: main
user: user
command: /sp.constitution
labels: ["hackathon", "constitution", "physical-ai", "textbook"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - .specify/memory/constitution.md
 - .specify/templates/plan-template.md
 - .specify/templates/spec-template.md
 - .specify/templates/tasks-template.md
 - README.md
tests:
 - none
---

## Prompt

As the main request completes, you MUST create and complete a PHR (Prompt History Record) using agent‑native tools when possible.

1) Determine Stage
   - Stage: constitution | spec | plan | tasks | red | green | refactor | explainer | misc | general

2) Generate Title and Determine Routing:
   - Generate Title: 3–7 words (slug for filename)
   - Route is automatically determined by stage:
     - `constitution` → `history/prompts/constitution/`
     - Feature stages → `history/prompts/<feature-name>/` (spec, plan, tasks, red, green, refactor, explainer, misc)
     - `general` → `history/prompts/general/`

3) Create and Fill PHR (Shell first; fallback agent‑native)
   - Run: `.specify/scripts/bash/create-phr.sh --title "<title>" --stage <stage> [--feature <name>] --json`
   - Open the file and fill remaining placeholders (YAML + body), embedding full PROMPT_TEXT (verbatim) and concise RESPONSE_TEXT.
   - If the script fails:
     - Read `.specify/templates/phr-template.prompt.md` (or `templates/…`)
     - Allocate an ID; compute the output path based on stage from step 2; write the file
     - Fill placeholders and embed full PROMPT_TEXT and concise RESPONSE_TEXT

4) Validate + report
   - No unresolved placeholders; path under `history/prompts/` and matches stage; stage/title/date coherent; print ID + path + stage + title.
   - On failure: warn, don't block. Skip only for `/sp.phr`.


/sp.constitution Act as a Senior AI Solutions Architect and Technical Lead. I am participating in a hackathon to build an "AI-Native Textbook" on Physical AI & Humanoid Robotics.

Your task is to generate a single, comprehensive file named `PROJECT_CONSTITUTION.md`. This file will serve as the "Source of Truth" for this entire development lifecycle.

The `PROJECT_CONSTITUTION.md` must contain the following sections:

1. **Project Mission:**
   - Develop a Docusaurus-based interactive textbook for "Physical AI & Humanoid Robotics" (covering ROS 2, Gazebo, NVIDIA Isaac).
   - Integrate a RAG Chatbot (Project Two) that answers student queries using the textbook content.

2. **Tech Stack & Architecture (Strict Enforcement):**
   - **Frontend:** Docusaurus (React/TypeScript), Tailwind CSS.
   - **Backend:** FastAPI (Python), Pydantic for validation.
   - **Database:** Neon (Serverless Postgres) for chat history/user data.
   - **Vector Search:** Qdrant for RAG (retrieving book context).
   - **AI/LLM:** OpenAI Agents or ChatKit for response generation.
   - **Auth:** Better Auth (optional but preferred).

3. **Agentic Workflow Rules (For You):**
   - **Code Style:** Strict PEP 8 (Python) and Prettier (JS/TS).
   - **Modularity:** The backend and frontend must be in separate directories (`/server` and `/web`).
   - **Error Handling:** You must implement try/catch blocks and logging for all external API calls (OpenAI/Qdrant).
   - **Visuals:** When explaining complex logic, use Mermaid.js syntax to create diagrams.

4. **Development Roadmap:**
   - **Phase 1:** Setup Docusaurus & Generate basic chapters using Claude Code.
   - **Phase 2:** Setup FastAPI + Qdrant & Implement RAG pipeline.
   - **Phase 3:** Integrate Chat Widget into Docusaurus.
   - **Phase 4:** Deployment (GitHub Pages for Front, Railway/Render for Back).

5. **Key Deliverables Checklist:**
   - List the specific artifacts required by the Hackathon (Public Repo, Live Link, Video Demo).

Please generate this `PROJECT_CONSTITUTION.md` file now. It should be formatted effectively so I can pin it in my IDE or feed it back to you in future sessions to maintain context.

## Response snapshot

I've successfully created the project constitution for your AI-Native Textbook on Physical AI & Humanoid Robotics. Here's what was accomplished:

1. Created a comprehensive constitution file at `.specify/memory/constitution.md` with all required sections:
   - Core Principles aligned with your requirements
   - Architecture & Implementation Standards
   - Development Workflow & Quality Assurance
   - Governance section

2. Updated dependent templates to align with the constitution:
   - Modified plan-template.md to include constitution checks and proper project structure
   - Updated spec-template.md with functional requirements based on your tech stack
   - Enhanced tasks-template.md with specific tasks aligned to your project phases
   - Updated README.md to reflect the project mission and architecture

3. The constitution enforces the required tech stack and architecture:
   - Docusaurus frontend with Tailwind CSS
   - FastAPI backend with Pydantic validation
   - Neon database for user data
   - Qdrant for vector search/RAG
   - OpenAI Agents for response generation
   - Proper separation of /web and /server directories

4. Included all agentic workflow rules:
   - Code style enforcement (PEP 8, Prettier)
   - Error handling requirements
   - Visual documentation with Mermaid.js
   - Modular architecture requirements

The constitution serves as the source of truth for your hackathon project and will guide all development decisions throughout the project lifecycle.

## Outcome

- ✅ Impact: Created comprehensive project constitution and updated all dependent templates
- 🧪 Tests: none
- 📁 Files: .specify/memory/constitution.md, .specify/templates/plan-template.md, .specify/templates/spec-template.md, .specify/templates/tasks-template.md, README.md
- 🔁 Next prompts: none
- 🧠 Reflection: The constitution will ensure consistent development practices and tech stack adherence throughout the hackathon project.

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A