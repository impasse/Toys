function binary_search(arr, value, start = 0, end = arr.length-1) {
	if (start > end) {
		return -1;
	}
	let mid = (end - start) / 2 + start;
	if (arr[mid] == value) {
		return mid;
	} else if (arr[mid] > value) {
		return binary_search(arr, value, start, mid - 1);
	} else {
		return binary_search(arr, value, mid + 1, end);
	}
}
console.log(binary_search([0, 1, 2, 3, 4, 5, 6], 3));
