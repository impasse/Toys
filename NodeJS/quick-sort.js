Array.prototype.partition = function (guard) {
  let a = [], b = [];
  for (let i of this) {
    if (guard(i)) {
      a.push(i);
    } else {
      b.push(i);
    }
  }
  return [a, b];
}

function qsort(...arr) {
  if (arr.length <= 1) {
    return arr;
  } else {
    let key = arr.shift();
    let [lower, higher] = arr.partition(_ => _ <= key);
    return qsort(...lower).concat([key], qsort(...higher));
  }
}

console.log(qsort(1, 3, 2, 4, 6, 10, 8, 9, 11, 99, 100, 7));
