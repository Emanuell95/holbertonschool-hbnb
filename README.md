# HBnB Project

Overview
The HBnB Project is a simulation project of the AirBnb designed to facilitate short-term rental listings and bookings. The application follows a three-layer architecture pattern and employs also the Facade design pattern to simplify communication between layers. This document provides an overview of the project's architecture, core components, and interactions.

 Architecture
The application is built using a three-layer architecture:

1. **Presentation Layer**: Handles user interactions through services and APIs.
2. **Business Logic Layer**: Contains core logic and application rules.
3. **Persistence Layer**: Manages data storage and retrieval.

### High-Level Package Diagram
The system architecture is illustrated below:

classDiagram

  class PresentationLayer {
      <<Interface>>
      +ServiceAPI
      +RESTfulEndpoints
  }

  class BusinessLogicLayer {
      +User
      +Place
      +Review
      +Amenity
      +Facade
  }

  class PersistenceLayer {
      +DatabaseAccess
      +Repository
      +DataStorage
  }

  PresentationLayer --> BusinessLogicLayer : Uses Facade Pattern
  BusinessLogicLayer --> PersistenceLayer : Database Operations


## Core Components
The core entities and their relationships are illustrated below:

### Business Logic Layer

classDiagram

  class User {
      +UUID id
      +String name
      +String email
      +String password
      +Date created_at
      +Date updated_at
      +create()
      +update()
      +delete()
  }

  class Place {
      +UUID id
      +String name
      +String description
      +String location
      +int max_guests
      +float price_per_night
      +Date created_at
      +Date updated_at
      +create()
      +update()
      +delete()
  }

  class Review {
      +UUID id
      +String text
      +UUID user_id
      +UUID place_id
      +Date created_at
      +Date updated_at
      +create()
      +update()
      +delete()
  }

  class Amenity {
      +UUID id
      +String name
      +Date created_at
      +Date updated_at
      +create()
      +update()
      +delete()
  }

  User "1" --> "*" Place : creates
  User "1" --> "*" Review : writes
  Place "1" --> "*" Review : receives
  Place "1" --> "*" Amenity : has


## API Interaction Flow

### 1. User Registration

sequenceDiagram
    participant User
    participant API
    participant BusinessLogic
    participant Database

    User->>API: Register User
    API->>BusinessLogic: Validate and Process User Data
    BusinessLogic->>Database: Insert New User Record
    Database-->>BusinessLogic: User Record Saved
    BusinessLogic-->>API: User Registered Successfully
    API-->>User: Registration Success


 2. Place Creation

sequenceDiagram
    participant User
    participant API
    participant BusinessLogic
    participant Database

    User->>API: Create New Place
    API->>BusinessLogic: Validate and Process Place Data
    BusinessLogic->>Database: Insert New Place Record
    Database-->>BusinessLogic: Place Record Saved
    BusinessLogic-->>API: Place Created Successfully
    API-->>User: Place Creation Success


 3. Review Submission

sequenceDiagram
    participant User
    participant API
    participant BusinessLogic
    participant Database

    User->>API: Submit Review
    API->>BusinessLogic: Validate and Process Review Data
    BusinessLogic->>Database: Insert New Review Record
    Database-->>BusinessLogic: Review Record Saved
    BusinessLogic-->>API: Review Submitted Successfully
    API-->>User: Review Submission Success


### 4. Fetching a List of Places

sequenceDiagram
    participant User
    participant API
    participant BusinessLogic
    participant Database

    User->>API: Fetch List of Places
    API->>BusinessLogic: Retrieve Place List Based on Criteria
    BusinessLogic->>Database: Query Places
    Database-->>BusinessLogic: Return Place List
    BusinessLogic-->>API: Return Place Data
    API-->>User: Display Place List




## Contributors:
Emanuel Mendoza github.com/Emanuell95


