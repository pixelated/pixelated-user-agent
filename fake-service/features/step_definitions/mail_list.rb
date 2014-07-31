When(/^I open the first mail in the '(.*)'$/) do |tag|
  page.execute_script("window.scrollBy(0, -200)")
  step "I select the tag '#{tag}'"
  step 'I open the first mail in the mail list'
end

When(/^I open the first mail in the mail list$/) do
  within('#mail-list') do
    mail_link = first('a')
    @current_mail_id = mail_link.native.attribute('href').scan(/\/(\d+)$/).flatten.first
    begin
      mail_link.click
    rescue # in Chrome, the 'a' in mail_list is not clickable because it's hidden inside the 'li'
      mail_link_parent_li = mail_link.find(:xpath, '../..')
      mail_link_parent_li.click
    end
  end
end

When(/I see that mail under the '(.*)' tag/) do |tag|
  step "I select the tag '#{tag}'"
  check_current_mail_is_visible
end

And(/^I open the mail I previously tagged$/) do
  open_current_mail
end

When(/^I open that mail$/) do
  open_current_mail
end

Then(/^I see the mail I sent$/) do
  check_current_mail_is_visible
end

Then(/^the deleted mail is there$/) do
  check_current_mail_is_visible
end

def open_current_mail
  within('#mail-list') do
    begin
      first("#mail-#{@current_mail_id} a").click
    rescue # in Chrome, the 'a' in mail_list is not clickable because it's hidden inside the 'li'
      first("#mail-#{@current_mail_id}").click
    end
  end
end

def check_current_mail_is_visible
  within('#mail-list') do
    have_selector?("#mail-#{@current_mail_id}").should be_true
  end
end
