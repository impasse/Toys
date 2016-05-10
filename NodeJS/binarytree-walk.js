class Node{
	constructor(value,left,right) {
		this.value = value;
		this.left = left;
		this.right = right;
	}
}

function DLR(n) {
	if (n === undefined) {
		return;
	}
	console.log(n.value);
	DLR(n.left);
	DLR(n.right);
}

function LDR(n) {
	if (n === undefined) {
		return;
	}
	LDR(n.left);
	console.log(n.value);
	LDR(n.right);
}
function LRD(n) {
	if (n === undefined) {
		return;
	}
	LRD(n.left);
	LRD(n.right);
	console.log(n.value);
}

function level(n) {
	let queue = [n];
	while (queue.length != 0) {
		let n = queue.shift();
		console.log(n.value);
		if (n.left !== undefined) {
			queue.push(n.left);
		}
		if (n.right !== undefined) {
			queue.push(n.right);
		}
	}
}

/*
	A
      /   \
     B     C 
    / \   /
   D   E F
*/

let n = new Node('A',
	new Node('B', new Node('D'), new Node('E')),
	new Node('C', new Node('F'))
);

DLR(n);
console.log('----');
LDR(n);
console.log('----');
LRD(n);
console.log('----');
level(n);
