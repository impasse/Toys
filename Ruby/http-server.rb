require 'socket'

STATUS_MESSAGE = { '200'=> 'OK', '404'=> 'Not Found', '500'=> 'Server Error'}

server = TCPServer.new('0.0.0.0',3000)

$index = -> (env) do
  if env[:method] == 'POST'
    ['500', {'Content-Type' => 'text/html'}, [env[:body].inspect]]
  else
    ['200', {'Content-Type' => 'text/html'}, ['I am work.']]
  end
end

def dispatch(client)
  env = {:headers=>{}}
  begin
    method,uri,protocol = client.readline.split
    if ['GET','POST','HEAD'].include? method
      env.update(
        {:method=>method,:request_uri=>uri,:protocol=>protocol}
      )
    else
      raise Error.new 'method not support' # 405
    end
    loop do
      line = client.gets.strip
      case line
        when '' # headers end
          break
        else
          name,value = line.split(':').map(&:strip)
          env[:headers][name.downcase.to_sym] = value.include?(',') ? value.split(',').map(&:strip) : value
      end
    end
    # decode urlencoded
    if env[:method] == 'POST'
      length = env[:headers][:'content-length'].to_i
      body = client.read(length)
      if env[:headers][:'content-type'] === 'application/x-www-form-urlencoded'
        env[:body] = Hash[body.split('&').map{|kv| kv.split('=')}]
      end
    end
    code,headers,body = $index.call(env)
    client.puts "HTTP/1.1 #{code} #{STATUS_MESSAGE[code]}\r\n"
    headers[:Connection] = 'close'
    headers.each_entry {|k,v| client.puts "#{k.capitalize}:#{v}\r\n"} # todo: with -
    client.puts "\r\n\r\n"
    body.each {|v| client.puts v} if env[:method] != "HEAD"
    client.close
  rescue => e
    unless client.closed?
      client.puts "HTTP/1.1 500 Server Error\r\nConnection:close\r\n\r\n#{e}"
      client.close
    end
  end
end

loop do
  client = server.accept
  Thread.new { dispatch(client) }
end
