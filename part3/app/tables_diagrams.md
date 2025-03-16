```mermaid
erDiagram
    USER {
        string id PK
        string first_name
        string last_name
        string email UNIQUE
        string password
        boolean is_admin
    }

    PLACE {
        string id PK
        string title
        string description
        float price
        float latitude
        float longitude
        string owner_id FK
    }

    REVIEW {
        int id PK
        string text
        int rating
        int user_id FK
        int place_id FK
    }

    AMENITY {
        int id PK
        string name UNIQUE
    }

    PLACE_AMENITY {
        int place_id FK
        int amenity_id FK
    }

    RESERVATION {
        int id PK
        int user_id FK
        int place_id FK
        date check_in_date
        date check_out_date
        float total_price
    }

    %% Relaciones %%
    USER ||--o{ PLACE : "owns"
    USER ||--o{ REVIEW : "writes"
    PLACE ||--o{ REVIEW : "has"
    PLACE ||--o{ PLACE_AMENITY : "has"
    AMENITY ||--o{ PLACE_AMENITY : "belongs to"
    USER ||--o{ RESERVATION : "books"
    PLACE ||--o{ RESERVATION : "reserved in"