Given /^I compose a message with$/ do |table|
  find('#compose-mails-trigger').click
  data = table.hashes.first
  fill_in('Subject', with: data['subject'])
  fill_in('Body', with: data['body'])
end

Given /^for the '(.*)' field I type '(.*)' and chose the first contact that shows$/ do |recipients_field, to_type|
  recipients_field.downcase!
  within("#recipients-#{recipients_field}-area") do
    find('.tt-input').native.send_keys(to_type)
    sleep 1
    first('.tt-dropdown-menu div div').click
  end
end

Given /^I save the draft$/ do
  click_button("Save Draft")
end

When /^I open the saved draft and send it$/ do
  step "I select the tag 'drafts'"
  step "I open the first mail in the mail list"
  page.should_not have_css("#send-button[disabled]")
  click_button('Send')
  find('#user-alerts').should have_content("Your message was sent!")
end
