/*
*Random Generator
*@return range [min,max)
*@example <p>for(let i of random(0,100,100){ console.log(i); }</p>
*/
function *random(min = 0, max = 1,count=10) {
  while (--count > 0) {
    yield min + Math.round(Math.random() * max);
  }
}
