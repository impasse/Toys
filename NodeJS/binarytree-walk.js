const assert = require('assert')

class Node {
  constructor (value, left, right) {
    this.value = value
    this.left = left
    this.right = right
  }
}

function DLR (n) {
  if (n === undefined) {
    return
  }
  console.log(n.value)
  DLR(n.left)
  DLR(n.right)
}

function LDR (n) {
  if (n === undefined) {
    return
  }
  LDR(n.left)
  console.log(n.value)
  LDR(n.right)
}
function LRD (n) {
  if (n === undefined) {
    return
  }
  LRD(n.left)
  LRD(n.right)
  console.log(n.value)
}

function level (n) {
  assert(n != undefined, 'No Tree')
  let queue = [n]
  while (queue.length != 0) {
    let n = queue.shift()
    console.log(n.value)
    if (n.left !== undefined) {
      queue.push(n.left)
    }
    if (n.right !== undefined) {
      queue.push(n.right)
    }
  }
}

function width (n) {
  let queue = [n]
  let width = 1
  while(queue.length != 0){
    next = []
    for (let i of queue) {
      if (i.left !== undefined) {
        next.push(i.left)
      }
      if (i.right !== undefined) {
        next.push(i.right)
      }
    }
    width = Math.max(width, next.length)
    queue = next
  }
  return width
}

function deep (n) {
  if (n === undefined) {
    return 0
  } else {
    return deep(n.left) > deep(n.right) ? deep(n.left) + 1 : deep(n.right) + 1
  }
}

/*
        A
      /   \
     B     C 
    / \   / \
   D   E F   G
  / \
 H   I
      \
       J
*/

let n = new Node('A',
  new Node('B', new Node('D', new Node('H'), new Node('I', undefined, new Node('J'))), new Node('E')),
  new Node('C', new Node('F'), new Node('G'))
)

console.log('先序')
DLR(n)
console.log('中序')
LDR(n)
console.log('后序')
LRD(n)
console.log('层序')
level(n)
console.log('----')
console.log('深度:%d', deep(n))
console.log('宽度:%d', width(n))
