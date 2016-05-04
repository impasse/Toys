function sort(...arr) {
	for (let i = 1; i < arr.length; i++){
		let tmp = arr[i];
		let j = i - 1;
		while (j > -1 && arr[j] > tmp) {
			arr[j + 1] = arr[j];
			j--;
		}
		arr[j + 1] = tmp;
	}
	return arr;
}


console.log(sort(5,4,3,2,1));
