function camelize(str) {
    return str.replace(/([^_]+)_?/g, (_, i)=>{
      return `${i[0].toUpperCase()}${i.substr(1, i.length-1)}`;
  });
}
