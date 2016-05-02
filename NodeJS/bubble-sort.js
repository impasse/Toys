function sort(...arr) {
	for (let i = 0; i < arr.length; i++){
		for (let j = 0; j < arr.length - 1; j++){
			if (arr[j] > arr[j + 1]) {
				[arr[j], arr[j + 1]] = [arr[j + 1], arr[j]];
			}
		}
	}
	return arr;
}

console.log(sort(1,3,2,4,5,2,10,11,98,2123,212));
