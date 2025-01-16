// ==UserScript==
// @name        클리앙 게시글 스타일 변경
// @namespace   Violentmonkey Scripts
// @match       *://www.clien.net/service/*
// @grant       none
// @version     1.0
// @author      Hyeongmin Kim
// @updateURL   -
// @downloadURL -
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
