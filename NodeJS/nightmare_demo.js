let Nightmare = require('nightmare');

let nm = Nightmare({ show: true });

let q = nm.goto('https:///www.baidu.com')
  .insert('#kw', '江泽民')
  .click('#su')
  .wait('#content_left')
  .evaluate(() => {
    let divs = document.querySelectorAll('#content_left .t > a');
    return Array.from(divs).map(div => div.innerText);
  })
  .end();

q.then(console.log);
