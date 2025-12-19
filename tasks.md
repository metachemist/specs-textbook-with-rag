# Tasks: AI-Native Textbook with RAG Platform

**Input**: Design documents from `/specs/001-textbook-rag-platform/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- **Web app**: `backend/src/`, `frontend/src/`
- **Mobile**: `api/src/`, `ios/src/` or `android/src/`
- Paths shown below assume single project - adjust based on plan.md structure

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create web directory for Docusaurus frontend
- [X] T002 Initialize Docusaurus project (TypeScript) in `/web`
- [X] T003 [P] Install Tailwind CSS & PostCSS dependencies
- [X] T004 [P] Configure `tailwind.config.js` and `docusaurus.config.ts`
- [X] T005 [P] Clean up default "Hello World" blog posts and pages
- [X] T006 Create the `/src/components` folder for future widgets
- [X] T007 Create server directory for FastAPI backend
- [X] T008 Initialize FastAPI project in `/server`
- [X] T009 Create requirements.txt file in server directory with required dependencies

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T010 [P] Create docs directory structure in web/docs for all modules
- [X] T011 Setup sidebars.js to match the specified syllabus structure
- [X] T012 Create base component files for ChatBotWidget, PersonalizeButton, and TranslateButton
- [X] T013 Setup basic API structure in server for chat and personalization endpoints
- [ ] T014 [P] Install and configure Better Auth for user authentication
- [X] T015 Create database models for User and ChatLog entities
- [X] T016 Set up environment configuration management for both web and server

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Access Interactive Textbook Content (Priority: P1) 🎯 MVP

**Goal**: Provide users with access to interactive textbook content covering Physical AI & Humanoid Robotics topics

**Independent Test**: Can navigate through all 4 modules of the textbook and read the content without technical issues.

### Tests for User Story 1 (OPTIONAL - only if tests requested) ⚠️

- [ ] T017 [P] [US1] Create navigation test for textbook modules
- [ ] T018 [P] [US1] Create content rendering test

### Implementation for User Story 1

- [X] T019 [P] [US1] Generate `web/docs/01-introduction/01-physical-ai-foundations.md`
- [X] T020 [P] [US1] Generate `web/docs/02-module-1-ros2/01-nodes-and-topics.md`
- [X] T021 [P] [US1] Generate `web/docs/02-module-1-ros2/02-urdf-humanoids.md`
- [X] T022 [P] [US1] Generate `web/docs/03-module-2-digital-twin/01-gazebo-physics.md`
- [X] T023 [P] [US1] Generate `web/docs/03-module-2-digital-twin/02-unity-integration.md`
- [X] T024 [P] [US1] Generate `web/docs/04-module-3-nvidia-isaac/01-isaac-sim-setup.md`
- [X] T025 [P] [US1] Generate `web/docs/04-module-3-nvidia-isaac/02-nav2-path-planning.md`
- [X] T026 [P] [US1] Generate `web/docs/05-module-4-vla/01-voice-to-action.md`
- [X] T027 [P] [US1] Generate `web/docs/05-module-4-vla/02-llm-cognitive-planning.md`
- [X] T028 [P] [US1] Generate `web/docs/06-capstone/01-autonomous-humanoid.md`
- [X] T029 [US1] Update sidebar navigation to include all generated content
- [X] T030 [US1] Implement responsive design with Tailwind CSS for all content pages

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Ask Questions via RAG Chatbot (Priority: P1)

**Goal**: Enable users to ask questions about textbook content and receive contextual answers

**Independent Test**: Can ask a question about textbook content and receive an accurate answer that references the appropriate textbook material.

### Tests for User Story 2 (OPTIONAL - only if tests requested) ⚠️

- [ ] T031 [P] [US2] Create contract test for POST /api/chat endpoint
- [ ] T032 [P] [US2] Create integration test for RAG functionality

### Implementation for User Story 2

- [ ] T033 [P] [US2] Implement POST /api/chat endpoint in server
- [ ] T034 [P] [US2] Create Qdrant vector database integration for textbook content
- [ ] T035 [P] [US2] Implement OpenAI integration for answer generation
- [ ] T036 [US2] Create ChatBotWidget React component with proper styling
- [ ] T037 [US2] Integrate ChatBotWidget with the textbook content pages
- [ ] T038 [US2] Implement error handling for RAG queries
- [ ] T039 [US2] Add logging for chat interactions

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Personalize Learning Experience (Priority: P2)

**Goal**: Allow users to personalize textbook content based on their expertise level

**Independent Test**: Can click the Personalize button and see textbook content adapted to my background (e.g., "Explain this for a Python expert").

### Tests for User Story 3 (OPTIONAL - only if tests requested) ⚠️

- [ ] T040 [P] [US3] Create contract test for POST /api/personalize endpoint
- [ ] T041 [P] [US3] Create integration test for personalization functionality

### Implementation for User Story 3

- [ ] T042 [P] [US3] Implement POST /api/personalize endpoint in server
- [ ] T043 [P] [US3] Create personalization service that adapts content based on user profile
- [ ] T044 [US3] Create PersonalizeButton React component with proper styling
- [ ] T045 [US3] Integrate PersonalizeButton with content pages
- [ ] T046 [US3] Implement user profile storage with background information
- [ ] T047 [US3] Add caching for personalized content

**Checkpoint**: At this point, User Stories 1, 2 AND 3 should all work independently

---

## Phase 6: User Story 4 - Access Content in Different Languages (Priority: P2)

**Goal**: Enable translation of textbook content into Urdu for non-English speakers

**Independent Test**: Can click the Translate button and see the current page content in the selected language (Urdu).

### Tests for User Story 4 (OPTIONAL - only if tests requested) ⚠️

- [ ] T048 [P] [US4] Create translation functionality test
- [ ] T049 [P] [US4] Create language switching test

### Implementation for User Story 4

- [ ] T050 [P] [US4] Create translation service for converting content to Urdu
- [ ] T051 [US4] Create TranslateButton React component with proper styling
- [ ] T052 [US4] Integrate TranslateButton with content pages
- [ ] T053 [US4] Implement language persistence across page navigation
- [ ] T054 [US4] Add error handling for translation failures

**Checkpoint**: At this point, User Stories 1, 2, 3 AND 4 should all work independently

---

## Phase 7: User Story 5 - Create and Manage Account (Priority: P3)

**Goal**: Allow users to create accounts and save their learning progress

**Independent Test**: Can sign up with email, provide background information, and log back in to access my account.

### Tests for User Story 5 (OPTIONAL - only if tests requested) ⚠️

- [ ] T055 [P] [US5] Create user registration test
- [ ] T056 [P] [US5] Create user authentication test

### Implementation for User Story 5

- [ ] T057 [P] [US5] Implement user registration with background information capture
- [ ] T058 [P] [US5] Create user profile management functionality
- [ ] T059 [US5] Integrate user authentication with personalization features
- [ ] T060 [US5] Implement secure session management

**Checkpoint**: All user stories should now be independently functional

---

## Phase N: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T061 [P] Documentation updates in docs/
- [ ] T062 Code cleanup and refactoring to ensure PEP 8 and Prettier compliance
- [ ] T063 Performance optimization across all stories (especially RAG pipeline)
- [ ] T064 [P] Additional unit tests (if requested) in tests/unit/
- [ ] T065 Security hardening especially for external API calls
- [ ] T066 Run quickstart.md validation
- [ ] T067 Final constitution compliance check for tech stack and architecture
- [ ] T068 Verify local server runs (`npm start`) without errors
- [ ] T069 Verify that the Sidebar navigation is working

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P1)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 3 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1/US2 but should be independently testable
- **User Story 4 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1/US2/US3 but should be independently testable
- **User Story 5 (P3)**: Can start after Foundational (Phase 2) - May integrate with US1/US2/US3/US4 but should be independently testable

### Within Each User Story

- Tests (if included) MUST be written and FAIL before implementation
- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All tests for a user story marked [P] can run in parallel
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all content creation tasks for User Story 1 together:
Task: "Generate web/docs/01-introduction/01-physical-ai-foundations.md"
Task: "Generate web/docs/02-module-1-ros2/01-nodes-and-topics.md"
Task: "Generate web/docs/02-module-1-ros2/02-urdf-humanoids.md"
Task: "Generate web/docs/03-module-2-digital-twin/01-gazebo-physics.md"
Task: "Generate web/docs/03-module-2-digital-twin/02-unity-integration.md"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Add User Story 4 → Test independently → Deploy/Demo
6. Add User Story 5 → Test independently → Deploy/Demo
7. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
   - Developer D: User Story 4
   - Developer E: User Story 5
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence