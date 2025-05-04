// ==UserScript==
// @name         다모앙 레벨 및 경험치 스타일 변경
// @version      2024.11141
// @description  경험치에 퍼센트를 추가로 표시하고 레벨 아이콘을 표시합니다
// @author       LiNE (fork: Hyeongmin Kim)
// @match        *://damoang.net/*
// @grant        none
// @updateURL    https://raw.githubusercontent.com/unstable-code/ShellScript/refs/heads/master/Universal/Userscripts/%EB%8B%A4%EB%AA%A8%EC%95%99/%EB%8B%A4%EB%AA%A8%EC%95%99%20%EB%A0%88%EB%B2%A8%20%EB%B0%8F%20%EA%B2%BD%ED%97%98%EC%B9%98%20%EC%8A%A4%ED%83%80%EC%9D%BC%20%EB%B3%80%EA%B2%BD.js
// @downloadURL  https://raw.githubusercontent.com/unstable-code/ShellScript/refs/heads/master/Universal/Userscripts/%EB%8B%A4%EB%AA%A8%EC%95%99/%EB%8B%A4%EB%AA%A8%EC%95%99%20%EB%A0%88%EB%B2%A8%20%EB%B0%8F%20%EA%B2%BD%ED%97%98%EC%B9%98%20%EC%8A%A4%ED%83%80%EC%9D%BC%20%EB%B3%80%EA%B2%BD.js
// ==/UserScript==

(function() {
  'use strict';

  // 퍼센트를 추가하는 함수
  function addExpPercentage() {
    // Exp 요소 선택
    const expElement = document.querySelector('.win_point');
    if (!expElement) return;

    // Exp 값을 가져와 숫자로 변환
    const expText = expElement.textContent.trim();
    const expValue = parseInt(expText.replace(/,/g, '').replace(/[^0-9]/g, ''), 10);

    // 특정 data-bs-title 속성 요소 선택
    const nextElement = document.querySelector('div[data-bs-title*="Next"]');
    if (!nextElement) return;

    // data-bs-title에서 Next 값을 가져와 숫자로 변환
    const nextText = nextElement.getAttribute('data-bs-title');
    const cleanedNextText = nextText.replace("Next ", "").replace(/,/g, '');
    const nextValue = parseInt(cleanedNextText, 10);

    // 퍼센트 계산
    const percentage = (expValue / (expValue + nextValue)) * 100;
    // 퍼센트를 소숫점 두 자리로 포맷
    const formattedPercentage = percentage.toFixed(2);
    // 총 값 계산
    const totalValue = expValue + nextValue;
    // Exp 요소의 텍스트를 업데이트
    expElement.textContent = `+${nextValue.toLocaleString()} (${formattedPercentage}%)`;
  }

  // 레벨 아이콘을 추가하는 함수
  function addLevelIcon() {
    // 특정 small 요소 선택 (정확한 위치를 위해 CSS 선택자 사용)
    const levelElement = document.querySelector('div.d-flex.align-items-center.justify-content-between.small > small:first-child');

    if (!levelElement) {
      return;
    }

    // Level 값을 가져오기
    const levelText = levelElement.textContent.trim();
    const levelValue = parseInt(levelText.replace("Level", "").trim(), 10);

    // 이미지 URL 생성
    const imgUrl = `https://damoang.net/plugin/nariya/skin/level/playonly/${levelValue}.svg?4`;

    // 이미지 태그 생성
    const imgElement = document.createElement('img');
    imgElement.src = imgUrl;
    imgElement.alt = `Level ${levelValue} Icon`;
    imgElement.style.marginRight = '5px';
    //imgElement.style.height = '12px'; // 원하는 크기로 조정

    // Level 요소의 텍스트를 "Lv"로 수정하고, 이미지 태그를 앞에 추가
    levelElement.textContent = `Lv.${levelValue}`;
    levelElement.prepend(imgElement);
  }

  // 페이지가 로드된 후 함수를 실행
  window.addEventListener('load', () => {
    addExpPercentage();
    addLevelIcon();
  });
})();
