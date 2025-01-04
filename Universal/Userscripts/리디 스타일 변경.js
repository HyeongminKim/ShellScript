// ==UserScript==
// @name        리디 스타일 변경
// @namespace   Violentmonkey Scripts
// @match       https://ridibooks.com/order/history
// @grant       none
// @version     2025.01040
// @author      Hyeongmin Kim
// @description 12/13/2024, 7:26:20 PM
// @updateURL https://raw.githubusercontent.com/HyeongminKim/ShellScript/refs/heads/master/Universal/Userscripts/%EB%A6%AC%EB%94%94%20%EC%B4%9D%20%EA%B2%B0%EC%A0%9C%EA%B8%88%EC%95%A1%20%ED%91%9C%EC%8B%9C.js
// @downloadURL https://raw.githubusercontent.com/HyeongminKim/ShellScript/refs/heads/master/Universal/Userscripts/%EB%A6%AC%EB%94%94%20%EC%B4%9D%20%EA%B2%B0%EC%A0%9C%EA%B8%88%EC%95%A1%20%ED%91%9C%EC%8B%9C.js
// ==/UserScript==

var total = 0;
const museoElements = document.querySelectorAll('.main_value');
const webtoonElements = document.querySelectorAll('.b-kw94g7');

museoElements.forEach(element => {
  const text = element.textContent.trim().replace(/,/g, '');
  const number = parseInt(text);
  if (!isNaN(number)) {
    total += number;
  }
});

const pageTitleElement = document.querySelector('.pagetitle_text');
if (pageTitleElement) {
  pageTitleElement.textContent += ` (총계: ${total.toLocaleString()}원)`;
}

webtoonElements.forEach(element => {
  if(element.textContent.includes('화')) {
    element.style.color = 'red';
  }
});

