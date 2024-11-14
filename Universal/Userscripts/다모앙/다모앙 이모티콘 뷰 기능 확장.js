// ==UserScript==
// @name        다모앙 이모티콘 뷰 기능 확장
// @version      2024.1114.1
// @description  이모티콘 미리보기 크기 조절, GIF 자동재생 및 이모티콘 크기 설정 기능 추가. 자동 재생 체크박스가 저장된 값 반영.
// @author      LiNE (fork: HyeongminKim)
// @match        *://damoang.net/*
// @grant        none
// @updateURL   https://raw.githubusercontent.com/HyeongminKim/ShellScript/refs/heads/master/Universal/Userscripts/%EB%8B%A4%EB%AA%A8%EC%95%99/%EB%8B%A4%EB%AA%A8%EC%95%99%20%EC%9D%B4%EB%AA%A8%ED%8B%B0%EC%BD%98%20%EB%B7%B0%20%EA%B8%B0%EB%8A%A5%20%ED%99%95%EC%9E%A5.js
// @downloadURL https://raw.githubusercontent.com/HyeongminKim/ShellScript/refs/heads/master/Universal/Userscripts/%EB%8B%A4%EB%AA%A8%EC%95%99/%EB%8B%A4%EB%AA%A8%EC%95%99%20%EC%9D%B4%EB%AA%A8%ED%8B%B0%EC%BD%98%20%EB%B7%B0%20%EA%B8%B0%EB%8A%A5%20%ED%99%95%EC%9E%A5.js
// ==/UserScript==

(function() {
    'use strict';

    // 기본값 설정
    const defaultScale = 100;
    const defaultAutoPlay = 'true';
    const defaultEmojiSize = 100; // 기본 이모티콘 크기
    let currentId = null;

    // 로컬 스토리지에서 설정된 값 불러오기
    let savedScale = localStorage.getItem('emoScale') || defaultScale;
    let savedAutoPlay = localStorage.getItem('emoAutoPlay') || defaultAutoPlay;
    let savedEmojiSize = localStorage.getItem('emoSize') || defaultEmojiSize;  // 이모티콘 크기 값

    // CSS 스타일 추가 (스크롤과 함께 이동하는 설정 UI)
    const style = document.createElement('style');
    style.innerHTML = `
        .settings-container {
            display: flex;
            align-items: center;
            gap: 10px;
            background-color: white;
            border: 1px solid #ccc;
            padding: 10px;
            border-radius: 5px;
            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
            margin-bottom: 10px;
        }

        .settings-container label {
            font-size: 14px;
            font-weight: bold;
        }

        .toggle-switch {
            position: relative;
            display: inline-block;
            width: 40px;
            height: 20px;
        }

        .toggle-switch input {
            opacity: 0;
            width: 0;
            height: 0;
        }

        .slider {
            position: absolute;
            cursor: pointer;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background-color: #ccc;
            transition: .4s;
            border-radius: 34px;
        }

        .slider:before {
            position: absolute;
            content: "";
            height: 14px;
            width: 14px;
            left: 3px;
            bottom: 3px;
            background-color: white;
            transition: .4s;
            border-radius: 50%;
        }

        input:checked + .slider {
            background-color: #2196F3;
        }

        input:checked + .slider:before {
            transform: translateX(18px);
        }
    `;
    document.head.appendChild(style);

    // #emo_icon 요소 앞에 새로운 DIV를 추가하여 설정 UI를 포함
    const emoIcon = document.querySelector('#emo_icon');
    if (emoIcon) {
        // 새로운 DIV 생성
        const settingsDiv = document.createElement('div');
        settingsDiv.className = 'settings-container';

        // 크기 설정 라벨 추가
        const scaleLabel = document.createElement('label');
        scaleLabel.innerText = '뷰어 크기:';

        // 리스트 박스 생성
        const scaleSelect = document.createElement('select');
        scaleSelect.id = 'scaleSelect';
        scaleSelect.innerHTML = `
            <option value="70">70%</option>  <option value="80">80%</option>  <option value="90">90%</option>
            <option value="100">100%</option> <option value="110">110%</option> <option value="120">120%</option>
            <option value="130">130%</option> <option value="140">140%</option> <option value="150">150%</option>
            <option value="160">160%</option> <option value="170">170%</option> <option value="180">180%</option>
            <option value="190">190%</option> <option value="200">200%</option>
        `;

        // 저장된 크기에 맞게 초기값 설정
        scaleSelect.value = savedScale;

        // 자동 재생 토글 스위치 생성
        const toggleContainer = document.createElement('label');
        toggleContainer.className = 'toggle-switch';

        const autoPlayCheckbox = document.createElement('input');
        autoPlayCheckbox.type = 'checkbox';
        autoPlayCheckbox.id = 'autoPlayCheckbox';
        autoPlayCheckbox.checked = savedAutoPlay === 'true' ? true : false;  // 저장된 값에 따라 초기 체크 상태 설정

        const slider = document.createElement('span');
        slider.className = 'slider';

        toggleContainer.appendChild(autoPlayCheckbox);
        toggleContainer.appendChild(slider);

        const toggleLabel = document.createElement('label');
        toggleLabel.innerText = '자동 재생';

        // 이모티콘 크기 설정 라벨 추가
        const emojiSizeLabel = document.createElement('label');
        emojiSizeLabel.innerText = '이모티콘 크기:';

        // 이모티콘 크기 텍스트 입력 필드 추가
        const emojiSizeInput = document.createElement('select');
        emojiSizeInput.id = 'emojiSizeInput';
        emojiSizeInput.innerHTML = `
            <option value="25">25%</option>  <option value="50">50%</option>
            <option value="75">75%</option>  <option value="100">100%</option>
            <option value="125">125%</option> <option value="150">150%</option>
            <option value="175">175%</option> <option value="200">200%</option>
        `;

        // 저장된 크기에 맞게 초기값 설정
        emojiSizeInput.value = savedEmojiSize;  // 저장된 이모티콘 크기를 불러오기

        // 설정 UI를 새로운 DIV에 추가
        settingsDiv.appendChild(scaleLabel);
        settingsDiv.appendChild(scaleSelect);
        settingsDiv.appendChild(toggleLabel);
        settingsDiv.appendChild(toggleContainer);
        settingsDiv.appendChild(emojiSizeLabel);
        settingsDiv.appendChild(emojiSizeInput);

        // #emo_icon 상단에 새로운 DIV 추가
        emoIcon.parentNode.insertBefore(settingsDiv, emoIcon);

        // 값 변경 시 저장
        scaleSelect.addEventListener('change', function() {
            localStorage.setItem('emoScale', scaleSelect.value);
            applySettings(); // 설정 적용
        });

        autoPlayCheckbox.addEventListener('change', function() {
            localStorage.setItem('emoAutoPlay', autoPlayCheckbox.checked ? 'true' : 'false');
            applySettings(); // 설정 적용
        });

        emojiSizeInput.addEventListener('input', function() {
            localStorage.setItem('emoSize', emojiSizeInput.value);  // 이모티콘 크기 값 저장
        });
    }

    // 설정 적용 함수
    function applySettings() {
        const scaleFactor = parseInt(localStorage.getItem('emoScale')) || defaultScale;
        const autoPlay = localStorage.getItem('emoAutoPlay') === 'true';
        const emojiSize = parseInt(localStorage.getItem('emoSize')) || defaultEmojiSize;

        // 이미지 크기 조정 및 자동 재생 적용
        const images = document.querySelectorAll('#emo_icon .emo-img');
        images.forEach((img) => {
            // 이미지의 원본 크기를 한 번만 저장 (이미 저장된 경우 덮어쓰지 않음)
            if (!img.getAttribute('data-original-width')) {
                const computedStyle = window.getComputedStyle(img);
                img.setAttribute('data-original-width', computedStyle.width);
                img.setAttribute('data-original-height', computedStyle.height);
            }

            // 원본 크기를 불러옴
            const originalWidth = parseFloat(img.getAttribute('data-original-width'));
            const originalHeight = parseFloat(img.getAttribute('data-original-height'));

            // 퍼센트 값에 따라 크기 조정
            img.style.width = `${(originalWidth * scaleFactor) / 100}px`;
            img.style.height = `${(originalHeight * scaleFactor) / 100}px`;

            // 자동 재생 설정
            if (autoPlay && img.getAttribute('url')) {
                img.src = img.getAttribute('url');
            } else if (!autoPlay && img.getAttribute('thumb')) {
                img.src = img.getAttribute('thumb');
            }

            // 터치 동작을 반영한 onmouseenter, onmouseleave 동작 수정
            img.onmouseenter = function() { setFocus(this.id); };
            img.onmouseleave = function() { unFocus(this.id);  };
            img.ontouchend = function() {
                this.isTouched = !this.isTouched;
                if (this.isTouched) { setFocus(this.id); }
                else { unFocus(this.id); }
            };

            img.onclick = function() {
                const emojiUrl = img.getAttribute('url');  // 전체 URL
                const fileName = emojiUrl.split('/').pop();  // 파일명 추출
                const emojiSize = localStorage.getItem('emoSize') || defaultEmojiSize;
                clip_insert(`${fileName}:${emojiSize}`);  // 파일명과 크기 전달
            }
        });
    }

    // setFocus 및 unFocus 함수
    function setFocus(id) {
        if (currentId) unFocus(currentId);
        if (id) {
            var newEle = document.getElementById(id);
            if (newEle) {
                currentId = id;
                newEle.classList.add('border-primary', 'border-2'); // 마우스 오버 시 보더 추가
                const autoPlay = localStorage.getItem('emoAutoPlay') === 'true';
                if (!autoPlay) {
                    newEle.timer = setTimeout(function () {
                        newEle.src = newEle.getAttribute('url');
                    }, 250);
                }
            }
        }
    }

    function unFocus(id) {
        var oldEle = document.getElementById(id);
        if (oldEle) {
            clearTimeout(oldEle.timer);
            oldEle.isTouched = false;
            oldEle.classList.remove('border-primary', 'border-2'); // 마우스가 떠날 때 보더 제거
            const autoPlay = localStorage.getItem('emoAutoPlay') === 'true';
            if (!autoPlay) {
                oldEle.src = oldEle.getAttribute('thumb');
            }
        }
    }

    // 페이지가 로드될 때 설정 적용
    window.addEventListener('load', function() {
        // 저장된 값으로 체크박스 상태 초기화
        const autoPlay = localStorage.getItem('emoAutoPlay') === 'true';
        const autoPlayCheckBox = document.querySelector('#autoPlayCheckbox')
        if(!autoPlayCheckBox) return false;

        autoPlayCheckBox.checked = autoPlay;
        applySettings();
    });

    // 페이지가 변경될 때마다 설정 재적용 (SPA 대응)
    const observer = new MutationObserver(applySettings);
    observer.observe(document.body, { childList: true, subtree: true });
})();
