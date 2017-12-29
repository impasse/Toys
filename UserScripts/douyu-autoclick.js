// ==UserScript==
// @name         douyu-autoclick
// @namespace    http://uuz.io
// @version      0.1
// @description  用于 pass 斗鱼 “你还在电脑前吗”
// @author       uuz
// @match        https://www.douyu.com/*
// @grant        none
// ==/UserScript==

(function() {
    'use strict';
    if (!/^\/[\w\d]+$/.test(location.pathname)) {
        return;
    }
    var ele = document.getElementById('js-room-video');
    if (ele) {
        setInterval(function () {
            ele.click();
        }, 10 * 60e3);
    }
    console.log('Auto click start');
})();
