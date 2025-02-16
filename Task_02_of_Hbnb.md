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
