// ==UserScript==
// @name        리디 스타일 변경
// @namespace   Violentmonkey Scripts
// @match       *://ridibooks.com/*
// @grant       none
// @version     2025.02200
// @author      Hyeongmin Kim
// @description 12/13/2024, 7:26:20 PM
// @updateURL https://raw.githubusercontent.com/unstable-code/ShellScript/refs/heads/master/Universal/Userscripts/%EB%A6%AC%EB%94%94%20%EC%8A%A4%ED%83%80%EC%9D%BC%20%EB%B3%80%EA%B2%BD.js
// @downloadURL https://raw.githubusercontent.com/unstable-code/ShellScript/refs/heads/master/Universal/Userscripts/%EB%A6%AC%EB%94%94%20%EC%8A%A4%ED%83%80%EC%9D%BC%20%EB%B3%80%EA%B2%BD.js
// ==/UserScript==

var total = 0;
var page = 0;

const museoElements = document.querySelectorAll('.main_value');
const webtoonElements = document.querySelectorAll('.b-kw94g7');
const pageTitleElement = document.querySelector('.pagetitle_text');
const pageBtnElements = document.querySelectorAll('.page_list');
const recommendElements = document.querySelector('.rigrid-a6cwv8');
const imgElements = document.querySelectorAll(".EventCalendar_TableBadge");
const booksCounts = document.querySelector(".rigrid-snzzqn");

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

if(recommendElements) {
  recommendElements.style.background = 'orange';
}

if (booksCounts) {
  booksCounts.style.color = 'orange';
  booksCounts.style.fontWeight = 'bold';
}

if (pageTitleElement) {
  pageTitleElement.textContent += ` (총계: ${total.toLocaleString()}원 / ${page} 페이지)`;
}

webtoonElements.forEach(element => {
  if(element.textContent.includes('화')) {
    element.style.color = 'red';
  }
});

document.querySelectorAll(".rigrid-11zvsio").forEach(element => {
  element.title = element.textContent.trim();
});

imgElements.forEach(element => {
  const src = element.getAttribute("src");
  var titleText = "";

  if (src.includes("482261")) {
    titleText = "후속권 업데이트";
  } else if(src.includes("434923")) {
    titleText = "세트전";
  } else if(src.includes("529079")) {
    titleText = "RIDI ONLY";
  } else if(src.includes("031013")) {
    titleText = "신작";
  }
  element.setAttribute("title", titleText);
});

