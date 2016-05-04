function merge(left = [], right = []) {
	let l = 0, r = 0, result = [];
	while (l < left.length && r < right.length) {
		if (left[l] < right[r]) {
			result.push(left[l++]);
		} else {
			result.push(right[r++]);
		}
	}
	return result.concat(left.slice(l),right.slice(r));
}

function sort(...arr) {
	if (arr.length <= 1) {
		return arr;
	} else {
		let len = arr.length / 2;
		return merge(sort(...arr.slice(0, len)), sort(...arr.slice(len)));
	}
}

console.log(sort(10,9,8,7,6,5,4,3,2,1));
