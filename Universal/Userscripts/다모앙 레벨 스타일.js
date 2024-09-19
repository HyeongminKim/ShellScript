// ==UserScript==
// @name        다모앙 레벨 스타일
// @namespace   Violentmonkey Scripts
// @match       *://damoang.net/*
// @grant       none
// @version     1.0
// @author      Hyeongmin Kim
// @description 9/19/2024, 10:18:52 PM
// @downloadURL https://raw.githubusercontent.com/HyeongminKim/ShellScript/master/Universal/Userscripts/%EB%8B%A4%EB%AA%A8%EC%95%99%20%EB%A0%88%EB%B2%A8%20%EC%8A%A4%ED%83%80%EC%9D%BC.js
// ==/UserScript==

const xpIconElements = document.querySelectorAll('.xp-icon');

xpIconElements.forEach(element => {
  const memberLevel = element.getAttribute('data-member-level');
  const currentLevel = 0;
  const imgTag = element.querySelector('img');
  if (imgTag) imgTag.remove();

  element.textContent = memberLevel < 10 + currentLevel ? memberLevel : '☠';
  element.style.display = 'unset';
  element.style.color = memberLevel >= 10 + currentLevel ? 'white' : memberLevel >= 6 + currentLevel ? 'red' : memberLevel >= 3 + currentLevel ? 'orange' : memberLevel >= currentLevel ? 'yellow' : memberLevel <= currentLevel - 5 ? 'grey' : 'green';
});
