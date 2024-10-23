// ==UserScript==
// @name        클리앙 검색 필드
// @namespace   Violentmonkey Scripts
// @match       *://www.clien.net/*
// @grant       none
// @version     1.0
// @author      Hyeongmin Kim
// @description 10/23/2024, 12:13:43 PM
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
  var filter = input.value.toLowerCase();
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

