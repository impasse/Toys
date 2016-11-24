 require 'sinatra'
 require 'sinatra/contrib/all'
 require 'multi_json'
 
 before do
     params.merge!(MultiJson.load(request.body)) if request.content_type == 'application/json'
 end
 
 post '/webhook' do
     event = request.env['HTTP_X_GITHUB_EVENT']
     json params
 end
