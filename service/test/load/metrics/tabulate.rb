require 'open-uri'

def get_data_from_file(f)
  data = Hash.new do |h, k|
    h[k] = []
  end

  open(f) do |fn|
    fn.each_line do |ll|
      _, timing, operation = ll.strip.split(" ", 3)
      data[operation] << Float(timing)
    end
  end

  data
end

user1 = get_data_from_file("1user.txt")
user2 = get_data_from_file("2user.txt")
user5 = get_data_from_file("5users.txt")

EPSILON = 0.5

def wildly_different?(val, vals)
  vals.each do |v|
    return true if (v - val).abs > EPSILON
  end
  return false
end

def divergent(vals)
  vals.each do |v|
    return true if wildly_different?(v, vals)
  end
  return false
end

def report(*datas)
  datas.map(&:keys).flatten.uniq.sort.each do |k|
    report_line_avg = datas.map do |dd|
      dd[k].inject(:+) / dd[k].length
    end
    report_line_all = datas.map do |dd|
      "{#{dd[k].sort.map{|d| "%.4f" % [d]}}}"
    end
#    if divergent(report_line_avg)
      puts "key: #{k}:"
      puts report_line_avg.map{|x| "%.4f" %[x]}.join("\t")
      puts report_line_all.join("\t")
      puts
#    end

  end
end

report(user1, user2, user5)
