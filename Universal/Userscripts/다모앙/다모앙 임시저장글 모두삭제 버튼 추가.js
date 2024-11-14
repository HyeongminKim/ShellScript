// ==UserScript==
// @name        다모앙 임시저장글 모두삭제 버튼 추가
// @namespace    http://tampermonkey.net/
// @version      2024.1114.0
// @description  임시 저장글 목록에 "모두 삭제" 버튼을 추가합니다.
// @author      LiNE (fork: HyeongminKim)
// @match        *://damoang.net/*
// @grant        none
// @downloadURL  https://raw.githubusercontent.com/HyeongminKim/ShellScript/refs/heads/master/Universal/Userscripts/%EB%8B%A4%EB%AA%A8%EC%95%99/%EB%8B%A4%EB%AA%A8%EC%95%99%20%EC%9E%84%EC%8B%9C%EC%A0%80%EC%9E%A5%EA%B8%80%20%EB%AA%A8%EB%91%90%EC%82%AD%EC%A0%9C%20%EB%B2%84%ED%8A%BC%20%EC%B6%94%EA%B0%80.js
// ==/UserScript==

(function() {
  'use strict';

  // "임시 저장글 목록" 옆에 "모두 삭제" 버튼 추가
  const addDeleteAllButton = () => {
    const closeButton = document.querySelector('.btn-close[data-bs-dismiss="offcanvas"]');
    if (closeButton && !document.getElementById('deleteAllBtn')) {
      const deleteAllBtn = document.createElement('button');
      deleteAllBtn.textContent = '모두 삭제';
      deleteAllBtn.id = 'deleteAllBtn';
      deleteAllBtn.classList.add('btn', 'btn-danger', 'btn-sm', 'nofocus');
      deleteAllBtn.style.marginLeft = '10px';

      deleteAllBtn.addEventListener('click', deleteAllAutosave);

      // "모두 삭제" 버튼을 X 버튼 왼쪽에 삽입
      closeButton.parentNode.insertBefore(deleteAllBtn, closeButton);
    }
  };

  // 모든 임시 저장글 삭제 함수
  const deleteAllAutosave = () => {
    const subject_ID = document.getElementById('wr_subject').value;
    const g5_bbs_url = window.g5_bbs_url || 'https://www.damoang.net/bbs';
    const autosaveListUrl = g5_bbs_url + '/ajax.autosavelist.php';

    if(subject_ID) {
      if(window.confirm('계속 진행할 경우 현재 편집중인 게시글 "' + subject_ID + '"가 즉시 등록됩니다!\n변경사항을 폐기하시겠습니까?\n\n"취소": 임시저장글 모두 삭제 계속진행\n"확인": damoang.net으로 이동')) {
        window.location.href = "https://damoang.net"
        return false;
      }
    }

    // 임시 저장글 목록을 가져옴
    $.get(autosaveListUrl, function(data) {
      const items = $(data).find('item');
      if (items.length === 0) {
        alert('삭제할 임시 저장글이 없습니다.');
        return;
      }

      items.each(function(index) {
        const as_id = $(this).find('id').text();

        // 각 항목 삭제 요청
        $.get(g5_bbs_url + "/ajax.autosavedel.php", {"as_id": as_id}, function(data) {
          if (data != -1) {
            console.log(`삭제 완료: ${as_id}`);
          } else {
            alert('임시 저장된글을 삭제하는 중에 오류가 발생하였습니다.');
          }

          // 마지막 항목 삭제 후 새로고침
          if (index === items.length - 1) {
            setTimeout(() => {
              location.reload();
            }, 500);
          }
        });
      });
    }, 'xml');
  };

  // 페이지 로드 후 "모두 삭제" 버튼 추가
  const init = () => {
    const observer = new MutationObserver(() => {
      if (document.querySelector('#autoSaveLabel')) {
        addDeleteAllButton();
        observer.disconnect();
      }
    });

    observer.observe(document.body, { childList: true, subtree: true });
  };

  window.addEventListener('load', init);
})();
