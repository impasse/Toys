class Node {
	constructor(value) {
		this.value = value;
		this.next = null;
	}
	find(value) {
		let n = this;
		while (n !== null) {
			if (n.value === value) {
				return n;
				break;
			}
			n = n.next;
		}
		return null;
	}
	remove(index) {
		let pos = 0, pos_node = this, prev_node = null;
		while (pos_node !== null) {
			if (pos == index) {
				prev_node.next = pos_node.next;
				return true;
			}
			++pos;
			prev_node = pos_node;
			pos_node = pos_node.next;
		}
		return false;
	}
	update(index, value) {
		let pos = 0, n = this;
		while (n !== null) {
			if (pos === index) {
				n.value = value;
				return true;
			}
			++pos;
			n = n.next;
		}
		return false;
	}
	index(index) {
		let pos = 0, n = this;
		while (n !== null) {
			if (pos === index) {
				return n.value;
			}
			++pos;
			n = n.next;
		}
	}
	concat(next) {
		let n = this;
		for (; n.next !== null; n = n.next) { }
		n.next = next;
		return this;
	}
	toString() {
		let n = this, arr = [];
		while (n !== null) {
			arr.push(n.value);
			n = n.next;
		}
		return JSON.stringify(arr);
	}
	inspect() {
		return this.toString();
	}
}

let linklist = new Node(1).concat(new Node(2)).concat(new Node(3)).concat(new Node(4)).concat(new Node(5));
console.log(linklist.find(1));
console.log(linklist.index(4));
console.log(linklist.update(4, 6));
console.log(linklist.remove(4));
console.log(linklist);
