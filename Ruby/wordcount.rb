couter = Hash.new(0)
ARGF.read.chomp.split.each{ |word| couter[word]+=1 }
couter.keys.sort.each{|key| puts "#{key}: #{couter[key]}"}
