Feature: search html mail and destroy

  Scenario: User searches for a mail and deletes it
    When I search for a mail with the words "this is a html mail"
    When I open the first mail in the mail list
    Then I see one or more mails in the search results
    Then I see if the mail has html content
    When I try to delete the first mail
    # Then I learn that the mail was deleted
    When I select the tag 'trash'
    Then the deleted mail is there
