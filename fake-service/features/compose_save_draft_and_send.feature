Feature: compose mail, save draft and send mail

  @wip
  Scenario: user composes and email, save the draft, later sends the draft and checks the sent message
    Given I compose a message with
      | subject      | body                                        |
      | Smail rocks! | You should definitely use it. Cheers, User. |
    And for the 'To' field I type 'ab' and chose the first contact that shows
    And I save the draft
    When I open the saved draft and send it
    Then I see that mail under the 'sent' tag
    When I open that mail
    Then I see that the subject reads 'Smail rocks!'
    And I see that the body reads 'You should definitely use it. Cheers, User.'

