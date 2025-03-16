# 🏡 HBnB - Auth & DB

## 📌 Project Description

HBnB is a Auth and DB  that manages users, places, reviews, and amenities, providing a scalable infrastructure for rental and reservation applications.

## 🚀 Main Features

- 🟢 **Users**: Registration, authentication, and account management with admin roles.
- 🏠 **Places**: Create, update, and delete properties with detailed information.
- ⭐ **Reviews**: Allows users to leave comments and ratings on places.
- 🛠️ **Amenities**: Associate special features with places.
- 📅 **Reservations**: Manage check-in and check-out dates.
- 🔐 **Security**: JWT-based authentication and role-based access control (RBAC).

🏡 **Main EndPoints**

### **Users**

- `POST /api/v1/users/` - Create a new user
- `PUT /api/v1/users/<user_id>/` - Modify user information
- `GET /api/v1/users/<user_id>/` - Retrieve user details

### **Places**

- `POST /api/v1/places/` - Create a place
- `PUT /api/v1/places/<place_id>/` - Modify a place
- `GET /api/v1/places/` - Retrieve all places
- `GET /api/v1/places/<place_id>/` - Retrieve place details

### **Reviews**

- `POST /api/v1/reviews/` - Create a review
- `PUT /api/v1/reviews/<review_id>/` - Modify a review
- `DELETE /api/v1/reviews/<review_id>/` - Delete a review

### **Amenities**

- `POST /api/v1/amenities/` - Add an amenity
- `PUT /api/v1/amenities/<amenity_id>/` - Modify an amenity

### **Reservations**

- `POST /api/v1/reservations/` - Create a reservation
- `GET /api/v1/reservations/<reservation_id>/` - Retrieve reservation details

---

## 📊 Database ER Diagram

### **Database Structure in Mermaid.js**

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

    %% Relationships %%
    USER ||--o{ PLACE : "owns"
    USER ||--o{ REVIEW : "writes"
    PLACE ||--o{ REVIEW : "has"
    PLACE ||--o{ PLACE_AMENITY : "has"
    AMENITY ||--o{ PLACE_AMENITY : "belongs to"
    USER ||--o{ RESERVATION : "books"
    PLACE ||--o{ RESERVATION : "reserved in"
```

---

## 👨‍💻 Author

Developed by Emanuel Mendoza GitHub.com/Emanuell95\


