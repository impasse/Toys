var assert = require('assert');

Function.prototype.bind = function (self, ...args) {
  assert.equal(typeof this, 'function');
  var orgi = this;
  let f = function (...newArgs) {
    if (new.target) {
      var result = orgi.apply(this, args.concat(newArgs));
      if (Object(result) === result) {
        return result;
      }
      return this;
    } else {
      return orgi.apply(self, args.concat(newArgs));
    }
  }
  Object.setPrototypeOf(f.prototype, orgi.prototype);
  Object.defineProperties(f, {
    'length': {
      value: orgi.length,
      writable: false,
      enumerable: false,
      configurable: false
    },
    'name': {
      value: typeof orgi.name === 'string' ? `bound ${orgi.name}` : 'bound',
      writable: false,
      enumerable: false,
      configurable: true
    }
  });
  return f;
}


function multiply(b, c) {
  return this.a * b * c;
}

assert.equal(multiply.bind({ a: 123 }, 456).bind(null, 789)(), 44253432);

///////////////////////////////////////////////////////////////////////////

function Person() {
}

Person.prototype.getId = function () {
  return this.id;
}

var IdPerson = Person.bind({ id: 120 });

var b = new IdPerson();

assert.equal(b.getId(), undefined);




