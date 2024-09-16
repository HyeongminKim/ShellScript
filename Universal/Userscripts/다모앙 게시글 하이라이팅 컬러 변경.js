// ==UserScript==
// @name        다모앙 게시글 하이라이팅 컬러 변경
// @namespace   Violentmonkey Scripts
// @match       *://damoang.net/*
// @grant       none
// @version     1.0
// @author      Hyeongmin Kim
// @description 9/13/2024, 3:13:33 PM
// ==/UserScript==

const schWordElements = document.querySelectorAll('.sch_word');
const userOnlyElements = document.querySelectorAll('em.border.rounded.p-1.me-1')
const xpIconElements = document.querySelectorAll('.xp-icon');
const sidebarElements = document.getElementById('sidebar-sub-s1-0');
const commentParentElement = document.querySelector('.d-flex.align-items-center.border-top.bg-secondary-subtle.py-1.px-3.small');

schWordElements.forEach(element => {
  element.style.backgroundColor = 'yellow';
  element.style.color = 'black';
});

userOnlyElements.forEach(element => {
  element.style.color = 'red';
});

xpIconElements.forEach(element => {
  const memberLevel = element.getAttribute('data-member-level');
  const imgTag = element.querySelector('img');
  if (imgTag) {
    imgTag.remove();
  }

  textContent = memberLevel < 10 ? memberLevel : '☠';
  element.style.display = 'unset';
  element.style.color = memberLevel >= 10 ? 'white' : memberLevel >= 8 ? 'red' : memberLevel >= 6 ? 'orange' : memberLevel >= 4 ? 'green' : 'grey';
});

if (sidebarElements) {
      sidebarElements.classList.add('show');
}

if (commentParentElement) {
  const commentTargetElement = commentParentElement.querySelector('.sv_name.text-truncate');
  commentTargetElement.textContent = commentTargetElement.textContent + ' 🎤';
}
