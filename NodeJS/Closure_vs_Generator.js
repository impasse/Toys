console.time('Generator');

let arr = [];

for(let i  of function*(){
    let s = 0;
    while(s<10000000){
        yield s++
    }
}()){
    arr.push(i);
}

console.timeEnd('Generator');

function G(){
    let s = 0;
    return function(){
        return s++;
    }
}

console.time('Closure');

let g = G();

arr = []
for(;;){
    let i = g();
    if(i>=10000000) break;
    arr.push(i);
}

console.timeEnd('Closure');
