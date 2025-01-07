// ==UserScript==
// @name        리디 스타일 변경
// @namespace   Violentmonkey Scripts
// @match       *://ridibooks.com/*
// @grant       none
// @version     2025.01070
// @author      Hyeongmin Kim
// @description 12/13/2024, 7:26:20 PM
// @updateURL https://raw.githubusercontent.com/HyeongminKim/ShellScript/refs/heads/master/Universal/Userscripts/%EB%A6%AC%EB%94%94%20%EC%8A%A4%ED%83%80%EC%9D%BC%20%EB%B3%80%EA%B2%BD.js
// @downloadURL https://raw.githubusercontent.com/HyeongminKim/ShellScript/refs/heads/master/Universal/Userscripts/%EB%A6%AC%EB%94%94%20%EC%8A%A4%ED%83%80%EC%9D%BC%20%EB%B3%80%EA%B2%BD.js
// ==/UserScript==

var total = 0;
var page = 0;

const museoElements = document.querySelectorAll('.main_value');
const webtoonElements = document.querySelectorAll('.b-kw94g7');
const pageTitleElement = document.querySelector('.pagetitle_text');
const pageBtnElements = document.querySelectorAll('.page_list');

pageBtnElements.forEach(element => {
  const pageThis = element.classList.contains("page_this");
  if(pageThis) {
    const museoElement = element.querySelector(".museo_sans");
    page = museoElement.textContent.trim();
  }
})

museoElements.forEach(element => {
  const text = element.textContent.trim().replace(/,/g, '');
  const number = parseInt(text);
  if (!isNaN(number)) {
    total += number;
  }
});

if (pageTitleElement) {
  pageTitleElement.textContent += ` (총계: ${total.toLocaleString()}원 / ${page} 페이지)`;
}

webtoonElements.forEach(element => {
  if(element.textContent.includes('화')) {
    element.style.color = 'red';
  }
});

