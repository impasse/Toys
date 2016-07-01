require 'sequel'

Sequel.connect('mysql2://root:@localhost/typecho')

class Option < Sequel::Model(:typecho_contents)
end

Option.all.each do |i|
    puts "#{i.title}: #{i.text}"
end
