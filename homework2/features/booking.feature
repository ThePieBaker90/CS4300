Feature: Movie seat booking

  Scenario: User books an available seat
    Given a movie exists
    And a seat is available
    And the user is logged in
    When the user books the seat
    Then the seat should be marked as booked