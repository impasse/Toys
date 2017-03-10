let a = [1,2,2,2,3,4,5];

function uniq(a){
    if(!a.length){
        return 0;
    }
    let index = 1;
    for(let i = 1; i < a.length; i++){
        if(a[i] != a[index - 1])
            a[index++] = a[i];
    }
    return index;
}

console.log(uniq(a));
