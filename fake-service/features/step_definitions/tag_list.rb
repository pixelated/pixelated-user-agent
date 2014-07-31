When(/^I select the tag '(.*)'$/) do |tag|
  wait_for_user_alert_to_disapear # in Chrome, the 'flash message is on top of the toggle
  first('.left-off-canvas-toggle').click
  page.execute_script("window.scrollBy(0, -200)")
  within('#tag-list') { find('li', text: /#{tag}/i).click }
end

def wait_for_user_alert_to_disapear
  begin
    while find('#user-alerts')
      sleep 0.1
    end
  rescue #if it couldn't find it, go ahead
  end
end
