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
