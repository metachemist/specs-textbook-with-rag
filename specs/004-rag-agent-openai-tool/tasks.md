---

description: "Task list for RAG Agent with OpenAI Tool Use implementation"
---

# Tasks: RAG Agent with OpenAI Tool Use

**Input**: Design documents from `/specs/004-rag-agent-openai-tool/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Server project**: `server/src/`, `server/tests/` in server directory
- Paths shown below follow this structure

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Update requirements.txt with OpenAI dependency if not already present
- [X] T002 [P] Create agent_service.py file in server directory
- [X] T003 [P] Create test_agent.py file in server directory

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T004 [P] Create OpenAI client initialization in agent_service.py
- [X] T005 [P] Create the RetrievalTool definition with JSON schema in agent_service.py
- [X] T006 [P] Create system prompt for "Textbook Assistant" in agent_service.py
- [X] T007 [P] Create data models: AgentRequest in server/src/models/agent_request.py
- [X] T008 [P] Create data models: AgentResponse in server/src/models/agent_response.py
- [X] T009 [P] Create data models: RetrievedContext in server/src/models/retrieved_context.py
- [X] T010 [P] Create data models: Citation in server/src/models/citation.py
- [X] T011 [P] Create data models: RetrievalTool in server/src/models/retrieval_tool.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Query Processing with Tool Calling (Priority: P1) 🎯 MVP

**Goal**: Implement the core agent logic that processes user queries, decides whether to call the retrieval tool, and generates responses based on retrieved context

**Independent Test**: Can ask a question to the agent, verify that it calls the retrieval tool, receives context, and generates a relevant answer citing the source

### Implementation for User Story 1

- [X] T012 [US1] Implement generate_agent_response function in server/agent_service.py
- [X] T013 [US1] Add logic to check if OpenAI model wants to call the retrieval tool
- [X] T014 [US1] Add logic to execute the retrieval tool when requested by OpenAI
- [X] T015 [US1] Add logic to send retrieved context back to OpenAI for final response
- [X] T016 [US1] Add error handling for OpenAI API calls

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Tool Definition and Integration (Priority: P1)

**Goal**: Ensure the retrieval tool is properly defined and integrated with the agent to call search functionality from Spec 2

**Independent Test**: Can verify that the retrieval tool is properly defined and integrated with the agent, allowing it to call the search functionality from Spec 2

### Implementation for User Story 2

- [X] T017 [US2] Integrate with rag_service.search_knowledge_base function in agent_service.py
- [X] T018 [US2] Ensure proper parameters are passed to the retrieval tool
- [X] T019 [US2] Validate the retrieved context format matches agent expectations
- [X] T020 [US2] Add fallback handling when retrieval tool returns no results

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Citation and Source Attribution (Priority: P2)

**Goal**: Implement citation logic so the agent mentions which chapter/file the information came from

**Independent Test**: Can ask a question and verify that the agent's response includes proper citations to the textbook chapters or files where the information was found

### Implementation for User Story 3

- [X] T021 [US3] Extract source information from retrieved context in agent_service.py
- [X] T022 [US3] Format citations properly in the agent response
- [X] T023 [US3] Ensure citations are integrated naturally into the response text
- [X] T024 [US3] Handle multiple citations when information comes from different sources

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: User Story 4 - Standalone Testing and Validation (Priority: P2)

**Goal**: Create a standalone test script that validates the complete agent workflow

**Independent Test**: Can run the standalone test script, ask a question, and verify that the agent calls the tool, receives context, and generates an appropriate response

### Implementation for User Story 4

- [X] T025 [US4] Create basic test_agent.py script structure
- [X] T026 [US4] Add sample question "What is a sensor in robotics?" to test script
- [X] T027 [US4] Implement logic to call agent service from test script
- [X] T028 [US4] Add verification that tool was called and context received
- [X] T029 [US4] Print final agent response with citations to console

**Checkpoint**: All user stories should be functional and validated

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T030 [P] Add comprehensive logging for agent interactions
- [X] T031 Add proper error handling and graceful fallbacks
- [ ] T032 Performance optimization for agent response times
- [X] T033 [P] Add unit tests for agent service functions
- [ ] T034 Security hardening for API key handling
- [X] T035 Run quickstart.md validation to ensure everything works as expected
- [X] T036 Final constitution compliance check for tech stack and architecture

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P1)**: Depends on US1 - Builds on the agent response functionality
- **User Story 3 (P2)**: Depends on US1, US2 - Works with the retrieved context and response
- **User Story 4 (P2)**: Depends on US1, US2, US3 - Tests the complete pipeline

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
Task: "Implement generate_agent_response function in server/agent_service.py"
Task: "Add logic to check if OpenAI model wants to call the retrieval tool"
Task: "Add logic to execute the retrieval tool when requested by OpenAI"
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
5. Add User Story 4 → Test complete pipeline → Deploy/Demo
6. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
   - Developer D: User Story 4
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