// ==UserScript==
// @name        다모앙 게시글 스타일 변경
// @namespace   Violentmonkey Scripts
// @match       *://damoang.net/*
// @grant       none
// @version     1.0
// @author      Hyeongmin Kim
// @description 9/13/2024, 3:13:33 PM
// @downloadURL https://raw.githubusercontent.com/HyeongminKim/ShellScript/master/Universal/Userscripts/%EB%8B%A4%EB%AA%A8%EC%95%99/%EB%8B%A4%EB%AA%A8%EC%95%99%20%EA%B2%8C%EC%8B%9C%EA%B8%80%20%EC%8A%A4%ED%83%80%EC%9D%BC%20%EB%B3%80%EA%B2%BD.js
// ==/UserScript==

const schWordElements = document.querySelectorAll('.sch_word');
const userOnlyElements = document.querySelectorAll('em.border.rounded.p-1.me-1');
const commentParentElements = document.querySelectorAll('.d-flex.align-items-center.border-top.bg-secondary-subtle.py-1.px-3.small');
const recommendElements = document.querySelectorAll('[class^="rcmd-box step"]');
const uniqueElements = document.querySelectorAll('.sv_name.text-truncate');
const xpIconElements = document.querySelectorAll('.xp-icon');
const visitCountElements = document.querySelectorAll('.wr-num.text-nowrap.order-4');
const userInfoElements = document.querySelectorAll('.sv_member.sideview.sideview--member.d-flex.align-items-center.gap-1');

const searchElement = document.getElementById('boardSearch');
const myXp = document.querySelector('.d-flex.align-items-center.justify-content-between.small');

const commentCountStyle = document.createElement('style');
const recommendBtnStyle = document.createElement('style');

schWordElements.forEach(element => {
  element.style.backgroundColor = 'yellow';
  element.style.color = 'black';
});

userOnlyElements.forEach(element => {
  element.style.color = 'red';
});

commentParentElements.forEach(element => {
  const target = element.querySelector('.sv_name.text-truncate');
  target.textContent = target.textContent + ' 🎤';
});

recommendElements.forEach(element => {
  const classNames = element.className.split(' ');
  classNames.forEach(className => {
    if(className.startsWith('step') && className.length === 5) {
      let number = parseInt(element.textContent.trim(), 10);
      if(!isNaN(number) && number >= 1000) {
        let formattedNumber = (number / 1000).toFixed(1) + 'k';
        formattedNumber = formattedNumber.replace('.0', '');
        element.textContent = formattedNumber;
      }
      element.textContent = '♥ ' + element.textContent;
    }
  })
});

uniqueElements.forEach(element => {
  if (element.textContent.trim() === 'SDK') {
    element.style.color = 'orange';
  }
});

visitCountElements.forEach(element => {
  let number = parseInt(element.textContent.trim(), 10);

  if (!isNaN(number) && number >= 1000) {
    let formattedNumber = (number / 1000).toFixed(1) + 'k';
    formattedNumber = formattedNumber.replace('.0', '');
    element.textContent = formattedNumber;
  }
});

xpIconElements.forEach(element => {
  const memberLevel = element.getAttribute('data-member-level');
  const currentLevel = parseInt(myXp.textContent.replace('Level', '').trim(), 10);
  const imgTag = element.querySelector('img');
  if (imgTag) imgTag.remove();

  element.textContent = memberLevel < 10 + currentLevel ? memberLevel : '☠';
  element.style.display = 'unset';
  element.style.color = memberLevel >= 10 + currentLevel ? 'white' : memberLevel >= 6 + currentLevel ? 'red' : memberLevel >= 3 + currentLevel ? 'orange' : memberLevel >= currentLevel ? 'yellow' : memberLevel <= currentLevel - 5 ? 'grey' : 'green';
});

userInfoElements.forEach(button => {
  button.removeAttribute('onclick');
});

if (searchElement) searchElement.className = '';

commentCountStyle.innerHTML = `
  .count-plus::before {
    content: '댓';
  }
`;
recommendBtnStyle.innerHTML = `
  .bi.bi-hand-thumbs-up::before {
    content: '♥';
  }
`;
document.head.appendChild(commentCountStyle);
document.head.appendChild(recommendBtnStyle);
