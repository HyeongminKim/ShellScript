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
const visitCountElements = document.querySelectorAll('.wr-num.text-nowrap.order-4');
const yourPostsElements = document.querySelectorAll('.list-group-item.da-link-block.writter-bg');
const emptyCommentElements = document.querySelectorAll('.btn.btn-basic');
const membersInfo = document.querySelectorAll('.sv_member.sideview.sideview--member.d-flex.align-items-center.gap-1');

const searchElement = document.getElementById('boardSearch');
const searchUserName = document.getElementById('bo_sfl').querySelector('option[value="wr_name,1"]');
const searchUserID = document.getElementById('bo_sfl').querySelector('option[value="wr_name,0"]');

const userOnline = document.querySelector('.d-flex.align-items-center.justify-content-between.small'); //Desktop Only

const commentCountStyle = document.createElement('style');
const recommendBtnStyle = document.createElement('style');

schWordElements.forEach(element => {
  element.style.backgroundColor = 'yellow';
  element.style.color = 'black';
});

emptyCommentElements.forEach(element => {
  if(element.getAttribute('title') === '공백문자') {
    const buttonElement = element.querySelector('.bi');
    if(buttonElement) buttonElement.textContent = '빈';
  }
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
        element.title = '받은 추천수: ' + number.toLocaleString(navigator.language);
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
    element.title = '조회수: ' + number.toLocaleString(navigator.language);
  }
});

yourPostsElements.forEach(listItem => {
  const svNameElement = listItem.querySelector('.sv_name.text-truncate');
  if (userOnline && svNameElement) {
    svNameElement.textContent = '<< YOU >>';
  }
});

membersInfo.forEach(member => {
  const xpIcon = member.querySelector('.xp-icon');

  if (userOnline && xpIcon) {
    if (xpIcon.getAttribute('data-member-level')) {
      const memberLevel = xpIcon.getAttribute('data-member-level');
      member.setAttribute('title', member.getAttribute('title').replace(' 자기소개', '님 Lv.' + memberLevel));
    } else if(xpIcon.getAttribute('data-member-level-icon') === 'special') {
      member.setAttribute('title', member.getAttribute('title').replace('자기소개', '광고주님'));
    }
  } else if(!userOnline && xpIcon) {
    member.setAttribute('title', member.getAttribute('title').replace(' 자기소개', '님의 정보를 확인하시려면 로그인하세요.'));
    xpIcon.setAttribute('data-member-level', '');
    xpIcon.setAttribute('data-member-level-icon', '');
  }
});

if (searchElement) searchElement.className = '';
if (searchUserName) searchUserName.textContent = '작성자 (이름)';
if (searchUserID) searchUserID.textContent = '작성자 (ID)';

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
