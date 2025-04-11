-- Drop tables if they exist (to prevent conflicts)
DROP TABLE IF EXISTS place_amenities;
DROP TABLE IF EXISTS reviews;
DROP TABLE IF EXISTS places;
DROP TABLE IF EXISTS amenities;
DROP TABLE IF EXISTS users;

-- Users Table
CREATE TABLE users (
    id CHAR(36) PRIMARY KEY,  -- UUID stored as CHAR(36)
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    is_admin BOOLEAN DEFAULT FALSE
);

-- Places Table (One-to-Many: User → Places)
CREATE TABLE places (
    id CHAR(36) PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10,2) NOT NULL CHECK (price >= 0), -- Ensuring non-negative price
    latitude FLOAT,
    longitude FLOAT,
    owner_id CHAR(36) NOT NULL,
    FOREIGN KEY (owner_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Reviews Table (One-to-Many: User → Reviews)
CREATE TABLE reviews (
    id CHAR(36) PRIMARY KEY,
    text TEXT NOT NULL,
    rating INT NOT NULL CHECK (rating BETWEEN 1 AND 5),
    user_id CHAR(36) NOT NULL,
    place_id CHAR(36) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (place_id) REFERENCES places(id) ON DELETE CASCADE,
    UNIQUE (user_id, place_id) -- Ensuring a user can only review a place once
);

-- Amenities Table (Independent Entity)
CREATE TABLE amenities (
    id CHAR(36) PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL
);

-- Many-to-Many Relationship: Places ↔ Amenities
CREATE TABLE place_amenities (
    place_id CHAR(36) NOT NULL,
    amenity_id CHAR(36) NOT NULL,
    PRIMARY KEY (place_id, amenity_id),
    FOREIGN KEY (place_id) REFERENCES places(id) ON DELETE CASCADE,
    FOREIGN KEY (amenity_id) REFERENCES amenities(id) ON DELETE CASCADE
);

-- Insert Administrator User
INSERT INTO users (id, first_name, last_name, email, password, is_admin)
VALUES (
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1',
    'Admin',
    'HBnB',
    'admin@hbnb.io',
    '$2b$12$XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX',  -- Replace with bcrypt hash
    TRUE
);

--Amenities
INSERT INTO amenities (id, name) VALUES
    (UUID(), 'Wi-Fi'),
    (UUID(), 'Pool'),
    (UUID(), 'Gym'),
    (UUID(), 'Air Conditioner'),
    (UUID(), 'Parking'),
    (UUID(), 'TV'),
    (UUID(), 'Kitchen available'),
    (UUID(), 'Pets Allowed'),
    (UUID(), 'Breakfast Included');
