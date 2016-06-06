require 'rack'

app = proc do |env|
    ['200',{'Content-Type'=>'text/plain'},[env.map{|k,v| "#{k}:#{v}"}.join("\r\n")]]
end

Rack::Handler::WEBrick.run app
