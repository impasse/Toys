require 'active_support/all'
 
 365.times do
     system "date -s \"#{ Date.today.next_day.to_time }\""
     10.times do |i|
         system "echo \"#{i}\" >> counter"
         system "git add counter && git commit -m \"#{Date.today}:#{i}\""
     end
 end
