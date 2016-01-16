new Promise(function (resolve, reject) {
    reject(Promise.resolve('A').then(function (val) {
        return new Promise(res=> { setTimeout(_=> { res(val + 'B') }, 1000); }).then(val=> { return Promise.resolve(val + "C") });
    }));
}).then(val=> { console.log(val) }).catch(reason=>console.error('e:',reason));
