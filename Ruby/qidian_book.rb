require 'time'
require 'nokogiri'
require 'http'
require 'sequel'


DB = Sequel.connect 'mysql2://root:@a.com/qidian'

DB.create_table? :books do
    primary_key :id
    String :book
    String :chapter
    Integer :size
    column :date, :datetime
    column :content, :mediumtext
end

Book = DB[:books]


def book id
    dom = Nokogiri::HTML.parse HTTP.get("http://book.qidian.com/info/#{id}").to_s
    title = dom.css('h1 em').text
    urls = dom.css('#j-catalogWrap li > a').map{|e| e.attr('href') }
    urls.each do |url|
	chapter, size, date, content = content url
	Book.insert book: title, chapter: chapter, size: size, date: date, content: content.strip
    end
end

def content url
    dom = Nokogiri::HTML.parse HTTP.get("http:#{url}").to_s
    chapter = dom.css('.j_chapterName').text
    size = dom.css('.j_chapterWordCut').text
    date = dom.css('.j_updateTime').text
    content = dom.css('.j_readContent p').map{|e| e.text }.join("\n")
    [chapter, size, date, content]
end

book '1001411233'
