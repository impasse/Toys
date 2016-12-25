#!/usr/bin/ruby

require 'mail'
require 'open-uri'
require 'rss'

TO = %w[]
SUBJECT = 'Packages Updated'
URL = 'https://www.archlinux.org/feeds/packages/'

Mail.defaults do
  delivery_method :smtp,
  address: '',
  port: 465,
  domain: '',
  authentication: :login,
  user_name: 'e',
  password: '',
  ssl: true,
  enable_starttls_auto: true
end

class Package < Struct.new(:name,:pubDate,:description); end

def html(packages)
  <<-MSG_END
  <table style="border:1px solid #ccc;width: 100%">
    <tr>
      <th>包名</th>
      <th>更新时间</th>
      <th>描述</th>
    </tr>
    #{packages.map{|package| "<tr><td>#{package.name}</td><td>#{package.pubDate}</td><td>#{package.description}</td></tr>" }.join}
  </table>
  MSG_END
end

def fetch
  open URL do |rss|
    feed = RSS::Parser.parse(rss)
    packages = []
    feed.channel.items.each do |item|
      packages << Package.new(item.title, item.pubDate, item.description)
    end
    return html(packages)
  end
end

Mail.deliver do
    from ''
    to TO.shift
    bcc TO
    subject SUBJECT
    content_type 'text/html;charset=utf-8'
    body fetch
end
