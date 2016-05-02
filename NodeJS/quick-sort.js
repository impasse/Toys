function qsort(...arr) {
  if (arr.length <= 1) {
    return arr;
  } else {
    let key = arr.shift();
    return qsort(...arr.filter(_ => _ <= key)).concat([key]).concat(qsort(...arr.filter(_ => _ > key)));
  }
}

console.log(qsort(1, 3, 2, 4, 6, 10, 8, 9, 11, 99, 100, 7));
