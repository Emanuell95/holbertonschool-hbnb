# 🧭 Simple Web Client – HBNB Project (Part 4)

This is Part 4 of the **Holberton School HBNB** project, focused on building a dynamic web client using **HTML5, CSS3, and JavaScript ES6** that connects to a Flask-based REST API.

---

## 🎯 Objectives

- Build a responsive and interactive frontend interface
- Connect the client with back-end services via RESTful API
- Use JWT authentication to manage user sessions
- Dynamically render data and handle user interactions without page reloads

---

## 📁 Project Structure
---

## 🔐 Authentication

- **Login** is handled via a `POST` request to the API.
- On successful login, a **JWT token** is returned and stored in cookies.
- Authenticated routes (e.g., viewing details, adding reviews) check for this token.

---

## 🔗 API Endpoints (example)

> Replace `http://localhost:5000` with your actual backend URL.

| Endpoint                  | Method | Description                      |
|---------------------------|--------|----------------------------------|
| `/api/login`              | POST   | Authenticates user, returns JWT |
| `/api/places`             | GET    | Returns a list of places        |
| `/api/places/:id`         | GET    | Returns details of a place      |
| `/api/places/:id/reviews` | POST   | Submits a review for a place    |

---

## 🧪 Features Per Page

### `login.html`
- Email/password login form
- On success: stores JWT in cookie, redirects to `index.html`

### `index.html`
- Fetches and displays list of places as cards
- Includes price filter dropdown
- Redirects to login if user is not authenticated

### `place.html`
- Displays full details of a selected place
- Lists all reviews
- If user is logged in, shows review form or button

### `add_review.html`
- Lets authenticated users submit a review for a place
- Redirects to login if JWT is missing

---

## 🧰 Technologies

- HTML5
- CSS3
- JavaScript ES6
- Fetch API
- JWT Authentication
- Flask (backend)

---

## ✅ Tasks Implemented

- [x] Task 0: Page structure and design using HTML + CSS
- [x] Task 1: Login functionality and token storage
- [x] Task 2: Places list and filtering (next)
- [x] Task 3: Place details and reviews
- [x] Task 4: Add review form and submission

---

## 🧪 Testing

- Login tested using correct and incorrect credentials
- JWT verified via browser cookies
- Network tab used to inspect requests/responses

---

## 📌 Notes

- Pages are responsive and W3C-valid
- Color palette and fonts are customizable
- All user interaction is handled client-side using JavaScript

---

## 👤 Author

Developed by Emanuel Mendoza, GitHub.com/Emanuell95
