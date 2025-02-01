// ==UserScript==
// @name        라프텔 줄거리 확장
// @namespace   Violentmonkey Scripts
// @match       *://laftel.net/*
// @grant       none
// @version     1.0
// @author      Hyeongmin Kim
// @description 2/1/2025, 10:55:01 PM
// ==/UserScript==

const observer = new MutationObserver(() => {
  const elements = document.querySelectorAll('.fmEjHp');

  elements.forEach(element => {
    element.style.webkitLineClamp = '5';
  });
});

observer.observe(document.body, { childList: true, subtree: true });

