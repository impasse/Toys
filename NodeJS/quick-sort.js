function qsort(head, ...tail) {
  return head == undefined ? [] : qsort(...tail.filter(_ => _ <= head)).concat(head,qsort(...tail.filter(_ => _ > head)));
}

console.log(qsort(1, 3, 2, 4, 6, 10, 8, 9, 11, 99, 100, 7));
