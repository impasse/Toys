/******************************************
**a simple crud orm for nodejs with mysql**
**           @author shyling             **
******************************************/


var db = require('mysql-promise')();
var R = require('ramda');

db.configure({
    host: 'localhost',
    user: 'root',
    password: '',
    database: ''
});


//monkey patch for print sql
db._query = db.query;
db.query = function() {
    console.log(arguments[0]);
    return db._query.apply(db, arguments);
};

// function* zip(...arrays) {
//     var length = arrays.reduce((_, __) => _.length <= __.length ? _.length : __.length);
//     var pos = 0;
//     while (pos < length) {
//         yield arrays.map(_ => _[pos]);
//         ++pos;
//     }
// }

function Model(model) {
    var base_fields = new model();
    var table_name = model.name;
    var rules = {
        'find_some_by_some': /find_(.+)_by_(.+)/,
        'find_all_by_some': /find_by_(.+)/,
        'find_all': /find/,
        'delete_where': /delete_where_(.+)/,
        'update_by_some': /update_by_(.+)/,
        'create':/create/
    };
    function check_field(fields) {
        if (fields.some(field => base_fields[field] === undefined)) {
            throw new Error('some field not exists in model');
        }
        return fields;
    }
    return new Proxy(base_fields, {
        get: function(target, name) {
            if (target[name]) {
                return target[name];
            } else {
                var match = R.toPairs(rules).find(([key, val]) => val.exec(name));
                if (match) {
                    matches = match[1].exec(name);
                    switch (match[0]) {
                        case 'find_some_by_some':
                            target[name] = function() {
                                var [selectors, conditions] = [matches[1], matches[2]].map(_ => _.split('_'));
                                var used_fields = check_field(selectors.concat(conditions));
                                var query = `SELECT ${selectors.join(',')} FROM ${table_name} WHERE ${R.zip(conditions, arguments).map(([k, v]) => `${k}='${v}'`).join(' and ')}`;
                                return db.query(query);
                            };
                            break;
                        case 'find_all':
                            target[name] = function() {
                                return db.query(`SELECT * FROM ${table_name}`);
                            };
                            break;
                        case 'find_all_by_some':
                            target[name] = function() {
                                var conditions = check_field(matches[1].split('_'));
                                return db.query(`SELECT * FROM ${table_name} WHERE ${R.zip(conditions, arguments).map(([k, v]) => `${k}='${v}'`).join(' and ')} `);
                            };
                            break;
                        case 'delete_where':
                            target[name] = function() {
                                var conditions = check_field(matches[1].split('_'));
                                return db.query(`DELETE FROM ${table_name} WHERE ${R.zip(conditions, arguments).map(([k, v]) => `${k}='${v}'`).join(' and ')} `);
                            };
                            break;
                        case 'update_by_some':
                            target[name] = function() {
                                var conditions = check_field(matches[1].split('_'));
                                var statment = R.toPairs(arguments[0]).map(([key, val]) => `${key}='${val}'`).join(',');
                                delete arguments['0'];
                                return db.query(`UPDATE ${table_name} SET ${statment} WHERE ${R.zip(conditions, R.values(arguments)).map(([k, v]) => `${k}='${v}'`).join(' and ')} `);
                            };
                            break;
                        case 'create':
                            target[name] = function(data) {
                                var row = Object.assign(Object.create(base_fields),data);
                                return db.query(`INSERT INTO ${table_name} (${R.keys(row).join(',')}) VALUES(${R.values(row).map(_=>`'${_}'`)}) `);
                            };
                    }
                    return target[name];
                } else {
                    throw new Error(name + " unsupported");
                }
            }
        },
        set: function(target, name, value) {
            throw new Error('Oops');
        }
    });
}

var users = Model(function users() {
    this.name = "";
    this.pass = "";
});

/*
*CREATE TABLE IF NOT EXISTS `users` (
* `name` varchar(16) NOT NULL,
* `pass` int(16) NOT NULL
*) ENGINE=InnoDB DEFAULT CHARSET=utf8;
*/

//examples
users.find_all();
users.find_by_name('aaa');
users.find_by_name('bbb');
users.find_by_pass('123');
users.find_pass_by_name('aaa');
users.delete_where_name('ddd');
users.update_by_name({ pass: 123 }, 'eee');
users.create({name:'fff',pass:'123'});