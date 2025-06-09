// ==UserScript==
// @name        스마트민방위교육 UX 최적화
// @namespace   Violentmonkey Scripts
// @match       *://www.cdec.kr/*
// @grant       none
// @version     2025.06090
// @author      Hyeongmin Kim
// @icon        https://i.namu.wiki/i/2R9UASCEkjwtVVvcP4q0r765eu3xJ_a5e8o6y7C2c_OgWtzJTX9Z_2pdxf3Wo11HPjgXi3Lg_71TlkotyM7DSw.svg
// @description 9/9/2024, 민방위 학습 플레이어 크기 및 볼륨값 재지정
// @updateURL   https://raw.githubusercontent.com/unstable-code/ShellScript/master/Universal/Userscripts/%EC%8A%A4%EB%A7%88%ED%8A%B8%EB%AF%BC%EB%B0%A9%EC%9C%84%EA%B5%90%EC%9C%A1%20UX%20%EC%B5%9C%EC%A0%81%ED%99%94.js
// @downloadURL https://raw.githubusercontent.com/unstable-code/ShellScript/master/Universal/Userscripts/%EC%8A%A4%EB%A7%88%ED%8A%B8%EB%AF%BC%EB%B0%A9%EC%9C%84%EA%B5%90%EC%9C%A1%20UX%20%EC%B5%9C%EC%A0%81%ED%99%94.js
// ==/UserScript==

const AAA = document.getElementById('player');
if (AAA && AAA.classList.contains('player-dimensions')) {
  AAA.style.width = '600px';
  AAA.style.height = '400px';
}

const volumeLevels = document.querySelectorAll('.vjs-volume-level');
volumeLevels.forEach(element => {
  element.style.width = '25%';
});

const educationContents = document.getElementById('educationContents');
if (educationContents) {
  educationContents.style.margin = '0'; // margin 비활성화
}

