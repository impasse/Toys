require 'socket'

s = TCPServer.new 3000

def try(default = nil)
  begin
    yield    
  rescue => e
    p e
    default
  end
end

loop do
  c = s.accept
  try do
    c.instance_eval do
      puts "HTTP/1.1 200 OK\r\n"
      puts "Content-Type: text/html\r\n"
      puts "Connection: close\r\n"
      puts "Transfer-Encoding: chunked\r\n"
      puts "\r\n"
      (1..100).each do |i|
        i = i.to_s
        puts "#{i.bytesize.to_s(16)}\r\n"
        puts "#{i}\r\n"
        sleep 0.1
      end
      puts "0\r\n"
      puts "\r\n"
      close
    end
  end
end
