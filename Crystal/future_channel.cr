require "concurrent/channel"

c = Channel(Int32).new

future {
    (1..100).each do |i| 
        c.send(i)
    end 
    c.send(0)
}

loop do
    r = c.receive
    break if r == 0
    puts r
end
