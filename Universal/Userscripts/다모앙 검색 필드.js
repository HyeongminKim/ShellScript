// ==UserScript==
// @name        다모앙 검색 필드
// @namespace   Violentmonkey Scripts
// @match       *://damoang.net/*
// @grant       none
// @version     1.0
// @author      Hyeongmin Kim
// @description 9/19/2024, 8:59:55 PM
// ==/UserScript==

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
  const sidebarElement = document.getElementById('sidebar-sub-s1-1');
  if (sidebarElement) sidebarElement.classList.add('show');
  addFilterInput();
};
