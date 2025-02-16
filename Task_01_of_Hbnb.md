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
