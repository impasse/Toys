require "concurrent/channel"

c = Channel(Int32).new

future {
    (1..100).each do |i| 
        c.send(i)
    end 
}

future {
    loop do
     puts c.receive
    end 
}

sleep(3)
