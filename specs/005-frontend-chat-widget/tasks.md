---

description: "Task list for Frontend Chat Widget Integration implementation"
---

# Tasks: Frontend Chat Widget Integration

**Input**: Design documents from `/specs/005-frontend-chat-widget/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web project**: `web/src/`, `web/tests/` in web directory
- **Server project**: `server/src/`, `server/tests/` in server directory
- Paths shown below follow this structure

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create web/src/components/ChatWidget directory
- [X] T002 [P] Verify CORS configuration is possible in server/main.py
- [X] T003 [P] Verify Docusaurus setup allows global component integration

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T004 [P] Update server/main.py to enable CORS for localhost:3000
- [X] T005 [P] Install required frontend dependencies (react-markdown, remark-gfm, etc.)
- [X] T006 [P] Create basic ChatWidget component structure in web/src/components/ChatWidget/
- [X] T007 [P] Create ChatButton subcomponent in web/src/components/ChatWidget/
- [X] T008 [P] Create ChatWindow subcomponent in web/src/components/ChatWidget/
- [X] T009 [P] Create CSS module for ChatWidget styling in web/src/components/ChatWidget/

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Chat Widget Access (Priority: P1) 🎯 MVP

**Goal**: Enable students to access a chat widget from any page on the textbook website

**Independent Test**: Can open the chat widget from any page on the website, type a message, and verify that the message is sent to the backend for processing.

### Implementation for User Story 1

- [X] T010 [US1] Implement floating chat button UI in ChatButton component
- [X] T011 [US1] Implement chat window UI in ChatWindow component
- [X] T012 [US1] Add state management for widget open/closed state in ChatWidget
- [X] T013 [US1] Implement toggle functionality to open/close chat window
- [X] T014 [US1] Style the chat widget to match Docusaurus theme
- [X] T015 [US1] Implement message input field in the chat window

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - AI Response Display (Priority: P1)

**Goal**: Display AI responses in the chat window with proper formatting

**Independent Test**: Can send a message to the AI and verify that the response is displayed in the chat window with proper formatting.

### Implementation for User Story 2

- [X] T016 [US2] Implement message list display in ChatWindow component
- [X] T017 [US2] Add state management for messages array in ChatWidget
- [X] T018 [US2] Implement markdown rendering for AI responses
- [X] T019 [US2] Add loading indicators during AI response processing
- [X] T020 [US2] Implement proper message formatting for user vs AI messages
- [X] T021 [US2] Add timestamp display for messages

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Cross-Origin Communication (Priority: P2)

**Goal**: Enable frontend to communicate with backend API across different domains/ports

**Independent Test**: Can verify that API requests from the frontend are successfully received and processed by the backend.

### Implementation for User Story 3

- [X] T022 [US3] Implement fetch logic to call the backend API in ChatWidget
- [X] T023 [US3] Create POST request to `http://localhost:8000/api/chat` endpoint
- [X] T024 [US3] Handle API response from backend in frontend component
- [X] T025 [US3] Verify CORS requests work between localhost:3000 and localhost:8000
- [X] T026 [US3] Test successful message transmission from frontend to backend

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: User Story 4 - Error Handling and Resilience (Priority: P2)

**Goal**: Handle errors gracefully to provide consistent user experience during outages

**Independent Test**: Can verify that when the backend is unavailable, the chat widget displays appropriate error messages and doesn't crash.

### Implementation for User Story 4

- [X] T027 [US4] Implement error handling for failed API requests
- [X] T028 [US4] Display user-friendly error messages when backend is offline
- [ ] T029 [US4] Add timeout handling for slow network connections
- [ ] T030 [US4] Implement retry mechanism for failed requests
- [X] T031 [US4] Add proper error status tracking for messages

**Checkpoint**: All user stories should be functional and validated

---

## Phase 7: Integration & Embedding

**Goal**: Embed the chat widget globally in the Docusaurus layout

**Independent Test**: Can verify the chat widget appears on every page of the textbook website.

### Implementation for Integration

- [X] T032 [P] Create Root.js component in web/src/theme/ to wrap the app
- [X] T033 [P] Register ChatWidget in Docusaurus Root component
- [ ] T034 Verify widget appears on all page types (docs, blog, etc.)
- [ ] T035 Test widget state preservation across page navigations
- [ ] T036 Ensure widget doesn't interfere with page functionality

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T037 [P] Add comprehensive logging for API calls
- [X] T038 Add proper error handling and graceful fallbacks
- [ ] T039 Performance optimization for chat rendering
- [ ] T040 [P] Add unit tests for ChatWidget component
- [ ] T041 Accessibility improvements for the chat widget
- [X] T042 Run quickstart.md validation to ensure everything works as expected
- [X] T043 Final constitution compliance check for tech stack and architecture

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2)
- **Integration (Phase 7)**: Depends on User Story 1-4 completion
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P1)**: Depends on US1 - Builds on the chat window functionality
- **User Story 3 (P2)**: Depends on US1 - Requires the basic widget to be in place
- **User Story 4 (P2)**: Depends on US3 - Requires API communication to handle errors

### Within Each User Story

- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)

---

## Parallel Example: User Story 1

```bash
# Launch all components for User Story 1 together:
Task: "Implement floating chat button UI in ChatButton component"
Task: "Implement chat window UI in ChatWindow component"
Task: "Add state management for widget open/closed state in ChatWidget"
```

---

## Implementation Strategy

### MVP First (User Stories 1-2 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. Complete Phase 4: User Story 2
5. **STOP and VALIDATE**: Test User Stories 1-2 together
6. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo
3. Add User Story 2 → Test with US1 → Deploy/Demo
4. Add User Story 3 → Test with US1&2 → Deploy/Demo
5. Add User Story 4 → Test with US1-3 → Deploy/Demo
6. Add Integration → Test complete functionality → Deploy/Demo
7. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
   - Developer D: User Story 4
   - Developer E: Integration & Embedding
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