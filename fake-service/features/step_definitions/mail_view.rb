A_MAIL = /[^\s@]+@[^\s@]+\.[^\s@]+/

Then(/^I see the mail has a cc and a bcc recipient$/) do
  within('.msg-header') do
    first('.cc').text.should =~ A_MAIL
    first('.bcc').text.should =~ A_MAIL
  end
end

Then(/^that email has the '(.*)' tag$/) do |tag|
  within('#mail-view') do |e|
    all('.tagsArea .tag').map(&:text).map(&:downcase).to_a.should include(tag)
  end
end

When(/I add the tag '(.*)' to that mail/) do |tag|
  page.execute_script("$('#new-tag-button').click();")
  page.execute_script("$('#new-tag-input').val('#{tag}');")
  find('#new-tag-input').native.send_keys [:return]
end

And(/^I reply to it$/) do
  click_button('Reply')
  click_button('Send')
end

Then(/^I choose to forward this mail$/) do
  click_button('Forward')
end

Then(/^I forward this mail$/) do
  click_button('Send')
end


Then(/^I remove all tags$/) do
  within('.tagsArea') do
    all('.tag').each do |tag|
      tag.click
    end
  end
end

Then(/^I choose to trash$/) do
  click_button('Trash message')
end

When(/^I try to delete the first mail$/) do
  step 'I open the first mail in the mail list'
  within('#mail-view') do
    page.driver.find_css('#view-more-actions')[0].click
    page.driver.execute_script("$('#delete-button-top').click();")
  end
  find('#user-alerts').text.should == 'Your message was moved to trash!'
end

Then(/^I see that the subject reads '(.*)'$/) do |expected_subject|
  find('#mail-view .subject').text.should == expected_subject
end

Then(/^I see that the body reads '(.*)'$/) do |expected_body|
  find('#mail-view .bodyArea').text.should == expected_body
end

Then(/^I see if the mail has html content/) do
  find('#mail-view .bodyArea').should have_css('h2[style*=\'color: #3f4944\']', :text => "cborim")
end
