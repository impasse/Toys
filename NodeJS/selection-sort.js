function sort(...arr) {
  for (let j = 0; j < arr.length; j++) {
    let low = j;
    for (let i = j+1; i < arr.length; i++) {
      if (arr[i] < arr[low]) {
        low = i;
      }
    }
    [arr[low],arr[j]] = [arr[j],arr[low]];
  }
  return arr;
}

console.log(sort(1, 3, 2, 4, 6, 10, 8, 9, 11, 99, 100, 7));
