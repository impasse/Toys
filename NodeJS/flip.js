function flip(fn){
      if(typeof fn !== 'function'){
            throw new Error(`require a function,but ${Object.prototype.toString.call(fn)} given`);
      }
      return function(...args){
            return fn(...args.reverse());
      }
}

flip(console.log)(3,2,1);
