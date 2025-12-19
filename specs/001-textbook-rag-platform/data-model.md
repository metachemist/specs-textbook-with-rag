# Data Model: Physical AI & Humanoid Robotics Textbook

**Feature**: AI-Native Textbook with RAG Platform
**Date**: 2025-12-19
**Modeler**: Senior Frontend Engineer

## Overview
This document defines the data models for the Physical AI & Humanoid Robotics textbook application. It captures the entities and their relationships based on the feature specification.

## Entities

### User
Represents a registered user with profile information used for personalization.

**Fields**:
- id: string (unique identifier)
- email: string (user's email address, required)
- softwareBackground: string (user's software experience level)
- hardwareBackground: string (user's hardware experience level)
- createdAt: Date (timestamp of account creation)
- updatedAt: Date (timestamp of last update)

**Validation Rules**:
- Email must be a valid email format
- softwareBackground and hardwareBackground are required fields

### ChatLog
Represents a conversation record between user and the RAG system.

**Fields**:
- id: string (unique identifier)
- userId: string (reference to User.id)
- query: string (the user's question)
- response: string (the AI-generated response)
- timestamp: Date (when the interaction occurred)
- context: string (the chapter/content context at the time of query)

**Validation Rules**:
- userId must reference an existing user
- query and response are required fields
- timestamp defaults to current time

### Chapter
Represents a textbook chapter that can be personalized and translated.

**Fields**:
- id: string (unique identifier)
- title: string (chapter title)
- content: string (the main content in markdown format)
- moduleId: string (reference to the module this chapter belongs to)
- order: number (position within the module)
- createdAt: Date
- updatedAt: Date

**Validation Rules**:
- title and content are required fields
- moduleId must reference an existing module
- order must be a positive integer

### Module
Represents a collection of chapters covering a specific topic.

**Fields**:
- id: string (unique identifier)
- title: string (module title)
- description: string (brief description of the module)
- order: number (position in the curriculum)
- createdAt: Date
- updatedAt: Date

**Validation Rules**:
- title and description are required fields
- order must be a positive integer

### PersonalizedContent
Represents a personalized version of content based on user profile.

**Fields**:
- id: string (unique identifier)
- originalContentId: string (reference to Chapter.id)
- userId: string (reference to User.id)
- personalizedContent: string (the personalized version of the content)
- createdAt: Date

**Validation Rules**:
- originalContentId and userId must reference existing records
- personalizedContent is required

## Relationships

```
User 1----* ChatLog
User 1----* PersonalizedContent
Module 1----* Chapter
Chapter 1----* PersonalizedContent
```

## State Transitions

### User Authentication State
- Unauthenticated → Authenticating → Authenticated/Failed
- Authenticated → Updating Profile → Profile Updated

### Content Personalization State
- Original Content → Personalization Requested → Personalization in Progress → Personalized Content Ready