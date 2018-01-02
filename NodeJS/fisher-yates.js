const arr = [...Array(100).keys()];

function shuffle(arr) {
    for(let i = arr.length - 1; i >= 0; i--) {
        const j = Math.round(Math.random() * arr.length);
        const tmp = arr[i];
        arr[i] = arr[j];
        arr[j] = tmp;
    }
    return arr;
}

console.log(shuffle(arr));
