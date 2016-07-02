#!/usr/bin/ruby
# -*- coding: utf-8 -*-
require 'json/ext'
require 'sequel'
require 'time'

class Post
    attr_accessor :coid
    attr_reader :post_id

    def initialize(data)
        @coid = nil
        @post_id = data[:post_id]
        @parent_id = (data[:parents]||[]).any? ? data[:parents][0] : nil
        @value = {}
        @value[:cid] = data[:thread_key]
        @value[:author] = data[:author_name]
        @value[:mail] = data[:author_email]
        @value[:created] = Time.parse(data[:created_at]).to_i
        @value[:url] = data[:author_url]
        @value[:ip] = data[:ip]
        @value[:text] = data[:message]
        @value[:parent] = 0
    end

    def value
        @value
    end
    
    def to_s
        @value.update({parent_id:@parent_id,post_id:@post_id,coid:@coid}).to_s
    end

    def father?
        @parent_id.nil?
    end

    def parent?(other)
        @parent_id == other.post_id
    end

    def parent=(id)
        @value[:parent] = id
    end 
end


Sequel.connect('mysql2://root:@localhost/typecho',:encoding=>'utf8mb4',:collation=>'utf8mb4_unicode_ci')

class PostModel < Sequel::Model(:typecho_comments)
end

open(ARGV[1]||'export.json') do |f|
    posts =  JSON.parse(f.read,symbolize_names:true)[:posts].map {|post| Post.new post }
    PostModel.all.map(&:destroy)
    top,tail = posts.partition{|post| post.father? }
    top.each do |post|
        post.coid = PostModel.create(**post.value).save.coid
    end
    tail.each do |post|
        f = top.find{|o| post.parent? o }
	    post.parent = f.coid unless f.nil?
        PostModel.create(**post.value).save
    end
	puts "转移完成,共#{posts.length}条"
end
