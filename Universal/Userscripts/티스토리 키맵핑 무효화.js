// ==UserScript==
// @name        티스토리 키맵핑 무효화
// @namespace   Violentmonkey Scripts
// @match       *://*.tistory.com/*
// @grant       none
// @version     1.0
// @author      Hyeongmin Kim
// @description 2/1/2025, 10:47:43 PM
// ==/UserScript==

window.onload = function() {
  setTimeout(function() {
    window.onkeydown = function(event) {
      event.preventDefault();
    };

    window.onkeypress = function(event) {
      event.preventDefault();
    };

    window.onkeyup = function(event) {
      event.preventDefault();
    };
  }, 1000);
};

