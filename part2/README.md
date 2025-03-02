# 🏡 HBnB Business logic and API Endpoints

## 📌 Overview

This project is a RESTful API built with Flask and Flask-RESTx for managing users, places, reviews, and amenities. It includes data validation, authentication, and automated testing.

## 📁 Project Structure

```
Hbnb
│── app.py                 # Main entry point
│── config.py              # Configuration settings
│── models/
│   │── __init__.py        # Initialize database models
│   │── user.py            # User model
│   │── place.py           # Place model
│   │── review.py          # Review model
│   │── amenity.py         # Amenity model
│── routes/
│   │── __init__.py        # Initialize API routes
│   │── user_routes.py     # User-related endpoints
│   │── place_routes.py    # Place-related endpoints
│   │── review_routes.py   # Review-related endpoints
│── tests/
│   │── test_users.py      # Unit tests for users
│   │── test_places.py     # Unit tests for places
│── requirements.txt       # Dependencies
│── README.md              # Project documentation
```

## 🚀 Features

✅ User management (Create, Read, Update, Delete)
✅ Place management with geolocation
✅ Review system for places
✅ Amenity listing
✅ Data validation using SQLAlchemy
✅ Automated testing with `pytest` and `unittest`
✅ API documentation with Swagger (Flask-RESTx)

## 🛠️ Installation & Setup

### 1️⃣ Install Dependencies

```sh
pip install -r requirements.txt
```

### 2️⃣ Set Up Database

Make sure you have **PostgreSQL** or **SQLite** installed, then initialize the database:

```sh
flask db init
flask db migrate
flask db upgrade
```

### 3️⃣ Run the Application

```sh
flask run
```

API will be available at: [http://127.0.0.1:5000/api/v1/](http://127.0.0.1:5000/api/v1/)

## 📌 API Endpoints

### ➤ User Endpoints

| Method   | Endpoint             | Description         |
| -------- | -------------------- | ------------------- |
| `POST`   | `/api/v1/users/`     | Create a new user   |
| `GET`    | `/api/v1/users/`     | Retrieve all users  |
| `GET`    | `/api/v1/users/<id>` | Get a specific user |
| `PUT`    | `/api/v1/users/<id>` | Update a user       |
| `DELETE` | `/api/v1/users/<id>` | Delete a user       |

#### Example Request (Create User)

```sh
curl -X POST "http://127.0.0.1:5000/api/v1/users/" \
     -H "Content-Type: application/json" \
     -d '{
          "first_name": "John",
          "last_name": "Doe",
          "email": "john.doe@example.com"
     }'
```

### ➤ Place Endpoints

| Method | Endpoint              | Description          |
| ------ | --------------------- | -------------------- |
| `POST` | `/api/v1/places/`     | Create a new place   |
| `GET`  | `/api/v1/places/`     | Retrieve all places  |
| `GET`  | `/api/v1/places/<id>` | Get a specific place |

### ➤ Review Endpoints

| Method | Endpoint           | Description          |
| ------ | ------------------ | -------------------- |
| `POST` | `/api/v1/reviews/` | Create a review      |
| `GET`  | `/api/v1/reviews/` | Retrieve all reviews |

## 🔬 Testing

Run unit tests to ensure everything is working correctly:

```sh
pytest tests/
```

OR

```sh
python -m unittest discover -s tests
```

## 👨‍💻 Author

Developed by Emanuel Mendoza GitHub.com/Emanuell95

