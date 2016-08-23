# We use this script to simulate the login of multiple concurrent users, with
# one login per second.
#
# To use it, you need:
# -ruby
# -pre-created users
#
# This can be run with `ruby blocking_spawner <x>`
# where x is the number of users you want to login.
#
# It was created to measure login times internally on the application with
# varying number of users


USER_PATTERN = "loadtest%d"
PASSWORD_PATTERN = "password_%d"
COUNT = ARGV[0].to_i

def curl_command(index)
  username = USER_PATTERN % [index]
  password = PASSWORD_PATTERN % [index]
  "curl --silent -X POST --data 'username=#{username}&password=#{password}' --cookie 'XSRF-TOKEN: blablabla' --header 'X-Requested-With: XMLHttpRequest' --header 'X-XSRF-TOKEN: blablabla' http://localhost:3333/login"
end

ts = (1...(1+COUNT)).map do |ix|
  t = Thread.new do
    `#{curl_command(ix+19)}`
  end
  sleep 1
  t
end

ts.each(&:join)



./blocking_spawner.rb 5
