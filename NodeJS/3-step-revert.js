let revert = (str = "") => {
	let arr = str.split(""), start = 0, len = arr.length;
	while (start <= len / 2) {
		let tmp = arr[start];
		arr[start] = arr[len - start - 1];
		arr[len - start - 1] = tmp;
		start++;
	}
	return arr.join("");
};

//123|45678->45678123
console.log(revert(revert('123')+revert('45678')));
