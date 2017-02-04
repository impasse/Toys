function* triangle() {
    var k;
    for (var i = 1; ; i++) {
        k = 1, a = [];
        for (var j = 1; j < i; j++) {
            a.push(k);
            k = k * (i - j) / j;
        }
        a.push(1);
        yield a;
    }
}

function pascalsTriangle(n) {
    var g = triangle()
    var a = []
    for (let i = 0; i < n; i++) {
        // a = a.concat(g.next().value);
        a.splice(a.length, 0, ...g.next().value);
    }
    return a;
}

console.log(pascalsTriangle(4))
