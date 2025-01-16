// ==UserScript==
// @name        클리앙 게시글 스타일 변경
// @namespace   Violentmonkey Scripts
// @match       *://*.clien.net/service/*
// @grant       none
// @version     2025.01161
// @author      Hyeongmin Kim
// @updateURL   https://raw.githubusercontent.com/HyeongminKim/ShellScript/refs/heads/master/Universal/Userscripts/%ED%81%B4%EB%A6%AC%EC%95%99/%ED%81%B4%EB%A6%AC%EC%95%99%20%EA%B2%8C%EC%8B%9C%EA%B8%80%20%EC%8A%A4%ED%83%80%EC%9D%BC%20%EB%B3%80%EA%B2%BD.js
// @downloadURL https://raw.githubusercontent.com/HyeongminKim/ShellScript/refs/heads/master/Universal/Userscripts/%ED%81%B4%EB%A6%AC%EC%95%99/%ED%81%B4%EB%A6%AC%EC%95%99%20%EA%B2%8C%EC%8B%9C%EA%B8%80%20%EC%8A%A4%ED%83%80%EC%9D%BC%20%EB%B3%80%EA%B2%BD.js
// @description 1/16/2025, 12:59:01 PM
// ==/UserScript==

const timePopoverElements = document.querySelectorAll('.time.popover');
const commentPopoverElements = document.querySelectorAll('.comment_time.popover');

timePopoverElements.forEach(element => {
  const textContent = Array.from(element.childNodes)
    .filter(node => node.nodeType === Node.TEXT_NODE)
    .map(node => node.textContent.trim())
    .join('');

  if (textContent.includes(':')) {
    element.style.color = 'red';
  }
});

commentPopoverElements.forEach(element => {
  const textContent = Array.from(element.childNodes)
    .filter(node => node.nodeType === Node.TEXT_NODE)
    .map(node => node.textContent.trim())
    .join('');

  if (textContent.includes(':')) {
    element.style.color = 'red';
  }
});
