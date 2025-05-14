obs = obslua

player_name = "firefox"  -- 기본값
wait_time = 5 -- 기본값
not_playing_since = nil

-- 설명
function script_description()
    return "지정한 MPRIS 플레이어 (예: Firefox) 가 재생 중이지 않으면 자동으로 녹화를 중단합니다."
end

-- 사용자 설정 항목 추가
function script_properties()
    local props = obs.obs_properties_create()
    obs.obs_properties_add_text(props, "player_name", "Player Name (default: firefox)", obs.OBS_TEXT_DEFAULT)
    obs.obs_properties_add_text(props, "wait_time", "Wait until media resume (default: 5)", obs.OBS_TEXT_DEFAULT)

    return props
end

-- 설정 변경시 변수 반영
function script_update(settings)
    player_name = obs.obs_data_get_string(settings, "player_name")
    wait_time = obs.obs_data_get_string(settings, "wait_time")

    player_name = (player_name ~= nil and player_name ~= "") and player_name or "firefox"
    wait_time = (wait_time ~= nil and wait_time ~= "") and wait_time or 5
end

-- 재생 상태 확인
function is_player_playing()
    if player_name == "" then return false end

    local cmd = "playerctl --player=" .. player_name .. " status 2>/dev/null"
    local handle = io.popen(cmd)
    if handle == nil then return false end

    local result = handle:read("*a")
    handle:close()

    return result:match("Playing") ~= nil
end

-- 타이머로 체크해서 녹화 중지
function check_and_stop_recording()
    if is_player_playing() then
        -- 미디어가 재생 중이면 타이머 변수 초기화
        not_playing_since = nil
    else
        if not_playing_since == nil then
            -- 재생중이 아닌 상태를 처음 감지하면 기록 시작
            not_playing_since = os.time()
        else
            -- 이미 재생이 멈춘 상태가 기록되어 있다면 wait_time 초 경과 여부 확인
            if os.difftime(os.time(), not_playing_since) >= wait_time then
                if obs.obs_frontend_recording_active() then
                    obs.obs_frontend_recording_stop()
                    -- 녹화 중단 후 변수 초기화
                    not_playing_since = nil
                end
            end
        end
    end
end

-- 스크립트 로드시 타이머 시작
function script_load(settings)
    obs.timer_add(check_and_stop_recording, 3000)
end

-- 스크립트 언로드시 타이머 제거
function script_unload()
    obs.timer_remove(check_and_stop_recording)
end

