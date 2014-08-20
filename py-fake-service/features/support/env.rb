require 'capybara'
require 'capybara-screenshot'
require 'capybara-screenshot/cucumber'

RACK_PORT = ENV['RACK_PORT'] || '4567'
HOST = "http://localhost:#{RACK_PORT}"

Capybara.register_driver :selenium_chrome do |app|
  Capybara::Selenium::Driver.new(app, :browser => :firefox)
end

Capybara::Screenshot.register_driver(:selenium_chrome) do |driver, path|
  driver.browser.save_screenshot(path)
end

driver = ENV['CUCUMBER_DRIVER'] ? ENV['CUCUMBER_DRIVER'].to_sym : :selenium_chrome

Capybara.configure do |config|
  config.run_server = false
  config.default_driver = driver
  config.app_host = HOST
end

include Capybara::DSL

Before do
  #{ }`curl -d '' #{HOST}/control/mailset/mediumtagged/load`
  sleep 3
  visit '/?lang=en'
  page.driver.browser.manage.window.maximize
end
