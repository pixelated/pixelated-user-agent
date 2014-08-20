When(/^I search for a mail with the words "(.*)"$/) do |search_term|
  search_field = find('#search-trigger input[type="search"]').native
  search_field.send_keys(search_term)
  search_field.send_keys(:return)
end

Then(/^I see one or more mails in the search results$/) do
  within('#mail-list') do
    all('li').length.should >= 1
  end
end

