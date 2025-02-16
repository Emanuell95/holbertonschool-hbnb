# HBnB Project Technical Documentation

## Introduction

The purpose of this document is to provide a comprehensive technical blueprint for the HBnB application. It outlines the system architecture, key components, and interactions necessary for the development and maintenance of the project. This documentation serves as a reference guide for developers during the implementation phase.

## High-Level Architecture

The HBnB application is designed using a three-layer architecture with the facade pattern to simplify interactions between layers. The three layers are:

1. Presentation Layer: Manages user interactions via services and APIs.
2. Business Logic Layer: Handles core application logic and processes.
3. Persistence Layer: Manages data storage and retrieval.

### High-Level Package Diagram

```mermaid
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
```

**Explanation:**

- The **Presentation Layer** interfaces with clients.
- The **Business Logic Layer** processes requests and applies business rules.
- The **Persistence Layer** provides data storage support.

## Business Logic Layer

The core of the HBnB application lies in its Business Logic Layer, which contains the primary entities:

- `User`
- `Place`
- `Review`
- `Amenity`

### Detailed Class Diagram

```mermaid
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
```

**Explanation:**

- **User** can create places and write reviews.
- **Place** can receive reviews and have multiple amenities.
- **Review** links users and places.
- **Amenity** represents additional features for places.

## API Interaction Flow

The interaction between layers during API calls follows a structured sequence to ensure data integrity and performance.

### 1. User Registration

```mermaid
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
```

**Explanation:**

- The User initiates a registration request.
- The API validates the request and delegates processing to Business Logic.
- Business Logic stores the data in the Database.

### 2. Place Creation

```mermaid
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
```

**Explanation:**

- User requests a new place creation.
- API forwards the request to the Business Logic Layer.
- Database stores the new Place.

### 3. Review Submission

```mermaid
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
```

**Explanation:**

- User submits a review.
- API validates the request and sends it to Business Logic.
- Database records the review.

### 4. Fetching a List of Places

```mermaid
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
```

**Explanation:**

- **User** requests available places.
- **API** asks **Business Logic** to query **Database**.
- **Database** returns the list to the client.

## Conclusion

This document provides an architectural overview of the HBnB application, detailing its layered structure, core entities, and essential API interactions. This serves as a guide for developers to implement, maintain, and extend the application effectively.

