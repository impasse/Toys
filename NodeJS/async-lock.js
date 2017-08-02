const AwaitLock = require('await-lock');

const lock = new AwaitLock();

let c = 1;

async function t() {
  console.log('run');
  try {
    await lock.acquireAsync();
    if (c) {
      c--;
      console.log('true');
      return await t();
    } else {
      console.log('false');
      return 2;
    }
  } catch (e) {
    console.error(e);
  } finally {
    lock.release();
  }
}


(async function () {
  console.log(await t());
})();

why?
