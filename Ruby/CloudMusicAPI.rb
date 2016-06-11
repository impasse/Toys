#!/usr/bin/ruby
# -*- encoding: utf-8 -*-
require 'net/http'
require 'json'

module CloudMusic
    # =CloudMusicAPI
    # 网易云音乐API ruby版本

    module API
        def self.search(s,limit=30,offset=0)
            APIPoster.new('/api/search/get',{:type=>1,:s=>s,:limit=>limit,:offset=>offset}).call
        end

        def self.detail(id)
            APIPoster.new('/api/song/detail',{:id=>id,:ids=>"[#{id}]"}).call
        end

        def self.lyric(id)
            APIPoster.new('/api/song/lyric',{:os=>'pc',:id=>id,:lv=>-1,:kv=>-1,:tv=>-1}).call
        end
    end

    class APIPoster
        attr_reader :url, :fields

        def initialize(url,fields)
            @url = url
            @fields = URI.encode_www_form(fields)
        end

        def call
            Net::HTTP.start 'music.163.com',80 do |c|
                JSON.parse c.post(@url,fields,{'Referer'=>'http://music.163.com/','User-Agent'=>'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.152 Safari/537.36'}).body
            end
        end
    end
end

if $0.include? 'CloudMusicAPI'
    puts CloudMusic::API.search('爱し子よ')
    puts CloudMusic::API.detail(640545)
    puts CloudMusic::API.lyric(640545)
end
