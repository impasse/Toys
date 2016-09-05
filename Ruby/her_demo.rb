require 'her'

Her::API::setup url:'https://shyling.com/api/v1', ssl: { verify: false } do |c|
	c.use Faraday::Request::UrlEncoded
	c.use Her::Middleware::DefaultParseJSON
	c.use Faraday::Adapter::NetHttp
end

class Post
	include Her::Model
end

p Post.find(1)
