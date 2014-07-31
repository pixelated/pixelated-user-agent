Feature: tagging and replying
  Scenario: User tags a mail, replies to it then checks that mail is in the right tag
    When I open the first mail in the 'inbox'
    Then that email has the 'inbox' tag
    When I add the tag 'website' to that mail
    Then I see that mail under the 'website' tag
    And I open the mail I previously tagged
    And I reply to it
    When I select the tag 'sent'
    Then I see the mail I sent

    
