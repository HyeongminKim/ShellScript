// ==UserScript==
// @name        스마트민방위교육 UX 최적화
// @namespace   Violentmonkey Scripts
// @match       *://www.cdec.kr/*
// @grant       none
// @version     1.0
// @author      HyeongminKim
// @icon        https://i.namu.wiki/i/2R9UASCEkjwtVVvcP4q0r765eu3xJ_a5e8o6y7C2c_OgWtzJTX9Z_2pdxf3Wo11HPjgXi3Lg_71TlkotyM7DSw.svg
// @description 9/9/2024, 민방위 학습 플레이어 크기 및 볼륨값 재지정
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

