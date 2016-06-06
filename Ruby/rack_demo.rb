#!/usr/bin/ruby
# -*- encoding: utf-8 -*-
require 'rack'

app = proc do |env|
    ['200',{'Content-Type'=>'text/plain; charset=utf-8'},[env.map{|k,v| "#{k}:#{v}"}.join("\r\n")]]
end

Rack::Handler::WEBrick.run app
