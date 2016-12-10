#!/usr/bin/ruby

require 'mail'

TO = ['def@qq.com','abc@qq.com']
SUBJECT = 'Packages Updated'

Mail.defaults do
  delivery_method :smtp,
  address: '',
  port: 465,
  domain: '',
  authentication: :login,
  user_name: '',
  password: '',
  ssl: true,
  enable_starttls_auto: true
end

def content(packages)
  <<-MSG_END
  <table style="border:1px solid #ccc">
    <tr>
      <th>包名</th>
      <th>原版本</th>
      <th>升级后</th>
    </tr>
    #{packages.map{|package| "<tr><td>#{package[0]}</td><td>#{package[1]}</td><td>#{package[2]}</td></tr>" }.join}
  </table>
  MSG_END
end

`pacman -Sy --noconfirm`

raw_packages = `pacman -Qu`
packages = []

raw_packages.scan /^(.+) (.+) -> (.+)$/ do |package|
    packages << package
end

if packages.any?
  Mail.deliver do
      from 'Notifier<notifier@zyy.moe>'
      to TO
      subject SUBJECT
      content_type 'text/html;charset=utf-8'
      body content(packages)
  end
else
    puts 'Nothing to update'
end

`pacman -Su --noconfirm --force`
