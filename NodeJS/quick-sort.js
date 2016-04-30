function qsort(...arr) {
  let key = arr.shift();
  return key === undefined ? [] : qsort(...arr.filter(_ => _ <= key)).concat([key]).concat(qsort(...arr.filter(_ => _ > key)));
}

console.log(qsort(1, 3, 2, 4, 6, 10, 8, 9, 11, 99, 100, 7));
