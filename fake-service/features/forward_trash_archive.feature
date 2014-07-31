Feature: forward_trash_archive
  Scenario: User forwards a mail, add CC and BCC address, later trash and archive the mail
    When I open the first mail in the 'inbox'
    Then I choose to forward this mail
    And for the 'CC' field I type 'ab' and chose the first contact that shows
    And for the 'Bcc' field I type 'fu' and chose the first contact that shows
    And I forward this mail
    When I open the first mail in the 'sent'
    Then I see the mail has a cc and a bcc recipient
    And I remove all tags
    And I choose to trash
    Then I see that mail under the 'trash' tag
