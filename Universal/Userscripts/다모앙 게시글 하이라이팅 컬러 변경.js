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
const userOnlyElements = document.querySelectorAll('em.border.rounded.p-1.me-1');
const xpIconElements = document.querySelectorAll('.xp-icon');
const commentParentElements = document.querySelectorAll('.d-flex.align-items-center.border-top.bg-secondary-subtle.py-1.px-3.small');
const recommendElements = document.querySelectorAll('[class^="rcmd-box step"]');

const sidebarElement = document.getElementById('sidebar-sub-s1-0');
const searchElement = document.getElementById('boardSearch');

const commentCountStyle = document.createElement('style');

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
  if (imgTag) imgTag.remove();

  element.textContent = memberLevel < 10 ? memberLevel : '☠';
  element.style.display = 'unset';
  element.style.color = memberLevel >= 10 ? 'white' : memberLevel >= 8 ? 'red' : memberLevel >= 6 ? 'orange' : memberLevel >= 4 ? 'green' : 'grey';
});

commentParentElements.forEach(element => {
  const target = element.querySelector('.sv_name.text-truncate');
  target.textContent = target.textContent + ' 🎤';
});

recommendElements.forEach(element => {
  const classNames = element.className.split(' ');
  classNames.forEach(className => {
    if(className.startsWith('step') && className.length === 5) {
      element.textContent = '♥ ' + element.textContent;
    }
  })
});

if (sidebarElement) sidebarElement.classList.add('show');
if (searchElement) searchElement.className = '';

commentCountStyle.innerHTML = `
  .count-plus::before {
    content: '댓';
  }
`;
document.head.appendChild(commentCountStyle);
