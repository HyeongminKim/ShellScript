// ==UserScript==
// @name        클리앙 검색 필드
// @namespace   Violentmonkey Scripts
// @match       *://www.clien.net/*
// @grant       none
// @version     2025.01160
// @author      Hyeongmin Kim
// @description 10/23/2024, 12:13:43 PM
// @updateURL   https://raw.githubusercontent.com/HyeongminKim/ShellScript/refs/heads/master/Universal/Userscripts/%ED%81%B4%EB%A6%AC%EC%95%99/%ED%81%B4%EB%A6%AC%EC%95%99%20%EA%B2%80%EC%83%89%20%ED%95%84%EB%93%9C.js
// @downloadURL https://raw.githubusercontent.com/HyeongminKim/ShellScript/refs/heads/master/Universal/Userscripts/%ED%81%B4%EB%A6%AC%EC%95%99/%ED%81%B4%EB%A6%AC%EC%95%99%20%EA%B2%80%EC%83%89%20%ED%95%84%EB%93%9C.js
// ==/UserScript==

function addFilterInput() {
  var sidebar = document.getElementsByClassName('menu_somoim')[0];

  var input = document.createElement('input');
  input.type = 'text';
  input.inputMode = 'search';
  input.id = 'filter-input';
  input.placeholder = '게시판 검색...';
  input.style.margin = '10px 5px';
  input.style.padding = '4px';
  input.style.width = '140px';
  input.onkeyup = filterSomoimLinks;

  sidebar.insertAdjacentElement('afterend', input);;
}

function filterSomoimLinks() {
  var input = document.getElementById('filter-input');
  var filter = input.value.toLowerCase().trim();
  var navLinks = document.getElementsByClassName('menu-list somoim');

  for(var i = 0; i < navLinks.length; i++) {
    var link = navLinks[i];
    if(filter.length === 0) {
      link.style.display = '';
      link.style.color = '';
    } else if (link.textContent.toLowerCase().indexOf(filter) > -1) {
      link.style.display = '';
      link.style.color = 'orange';
    } else {
      link.style.display = 'none';
      link.style.color = '';
    }
  }
}

window.onload = function() {
  addFilterInput();
};

