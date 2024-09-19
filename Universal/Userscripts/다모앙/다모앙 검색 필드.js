// ==UserScript==
// @name        다모앙 검색 필드
// @namespace   Violentmonkey Scripts
// @match       *://damoang.net/*
// @grant       none
// @version     1.0
// @author      Hyeongmin Kim
// @description 9/19/2024, 8:59:55 PM
// @downloadURL https://raw.githubusercontent.com/HyeongminKim/ShellScript/master/Universal/Userscripts/%EB%8B%A4%EB%AA%A8%EC%95%99/%EB%8B%A4%EB%AA%A8%EC%95%99%20%EA%B2%80%EC%83%89%20%ED%95%84%EB%93%9C.js
// ==/UserScript==

const sidebarElement = document.getElementById('sidebar-sub-s1-1');

function addFilterInput() {
  var input = document.createElement('input');
  input.type = 'text';
  input.id = 'filter-input';
  input.placeholder = '게시판/카테고리 검색...';
  input.onkeyup = filterNavLinks;

  var sidebar = document.getElementById('sidebar-site-menu');
  sidebar.insertBefore(input, sidebar.firstChild);
}

function filterNavLinks() {
  var input = document.getElementById('filter-input');
  var filter = input.value.toLowerCase();
  var navLinks = document.getElementsByClassName('nav-link');

  if(filter.length > 0 && !sidebarElement.classList.contains('show')) {
    if (sidebarElement) sidebarElement.classList.add('show');
  } else {
    if (sidebarElement) sidebarElement.classList.remove('show');
  }

  for (var i = 0; i < navLinks.length; i++) {
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
