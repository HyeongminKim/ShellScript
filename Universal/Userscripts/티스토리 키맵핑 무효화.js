// ==UserScript==
// @name        티스토리 키맵핑 무효화
// @namespace   Violentmonkey Scripts
// @match       *://*.tistory.com/*
// @grant       none
// @version     2025.02250
// @author      Hyeongmin Kim
// @description 2/1/2025, 10:47:43 PM
// @updateURL   https://raw.githubusercontent.com/HyeongminKim/ShellScript/refs/heads/master/Universal/Userscripts/%ED%8B%B0%EC%8A%A4%ED%86%A0%EB%A6%AC%20%ED%82%A4%EB%A7%B5%ED%95%91%20%EB%AC%B4%ED%9A%A8%ED%99%94.js
// @downloadURL https://raw.githubusercontent.com/HyeongminKim/ShellScript/refs/heads/master/Universal/Userscripts/%ED%8B%B0%EC%8A%A4%ED%86%A0%EB%A6%AC%20%ED%82%A4%EB%A7%B5%ED%95%91%20%EB%AC%B4%ED%9A%A8%ED%99%94.js
// ==/UserScript==

const moreButton = document.querySelector('.paging-more');

document.addEventListener("keydown", (event) => {
    event.stopImmediatePropagation();
    event.preventDefault();
}, true);

document.addEventListener("keyup", (event) => {
    event.stopImmediatePropagation();
    event.preventDefault();
}, true);

document.addEventListener("keypress", (event) => {
    event.stopImmediatePropagation();
    event.preventDefault();
}, true);

if (moreButton) {
  moreButton.textContent = "더보기";
}
