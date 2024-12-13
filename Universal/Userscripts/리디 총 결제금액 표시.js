// ==UserScript==
// @name        리디 총 결제금액 표시
// @namespace   Violentmonkey Scripts
// @match       https://ridibooks.com/order/history
// @grant       none
// @version     1.0
// @author      Hyeongmin Kim
// @description 12/13/2024, 7:26:20 PM
// ==/UserScript==

var total = 0;
const museoElements = document.querySelectorAll('.museo_sans');

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

