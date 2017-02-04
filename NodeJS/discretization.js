let _ = require('lodash/fp');

let arr = [34867, 145256, 603, 199480, 30917, 19756, 169700, 165310];

console.log(
    _.map(v => _.indexOf(v)(_.sortBy(_.identity)(arr)))(arr)
);
