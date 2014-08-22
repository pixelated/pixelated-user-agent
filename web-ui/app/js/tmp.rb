#!/usr/bin/env ruby

def update_directory(directory)
  Dir.entries(directory).each do | file |
    path = "#{directory}/#{file}"
    if File.directory?(path)
      update_directory(path) unless (file =~ /^[.]+$/)
    else
      update_file(path) if file =~ /\.(js)$/
    end
  end
end

def update_file(filename)
  tmpname = "#{filename}.orig"
  `mv #{filename} #{tmpname}`
  infile = File.open("#{tmpname}", "r")
  outfile = File.open("#{filename}", "w")
  replace_banner(infile, outfile)
  `rm #{tmpname}`
end

def replace_banner(infile, outfile)
  in_banner = true
  year = nil
  infile.each_line do | line |
    if in_banner
      copyright_match = /Copyright \(c\) ([0-9]{4})/.match(line)
      if copyright_match
        year = copyright_match[1]
      end
      if !(line =~ /^\/\//) && !(line =~ /^[\/ ]\*/)
        write_banner(outfile, year)
        in_banner = false
      end
    end
    if !in_banner
      outfile.puts line
    end
  end
end

def write_banner(outfile, year)
  banner = <<-EOS
/*
 * Copyright (c) %YEARS% ThoughtWorks, Inc.
 *
 * Pixelated is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Affero General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * Pixelated is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU Affero General Public License for more details.
 *
 * You should have received a copy of the GNU Affero General Public License
 * along with Pixelated. If not, see <http://www.gnu.org/licenses/>.
 */
  EOS
  years = (year != "2014") ? "#{year}-2014" : year
  banner.gsub!(/%YEARS%/, years)
  outfile.write(banner)
end

update_directory(ARGV[0])

