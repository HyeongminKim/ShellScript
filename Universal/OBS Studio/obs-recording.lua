obs = obslua

-- 기본값
player_name = "firefox"

------------------------------------------------------
-- OBS에서 보여질 스크립트 설명
------------------------------------------------------
function script_description()
    return "녹화 시작 시 지정된 MPRIS 플레이어 (예: Firefox)의 재생을 자동으로 시작합니다."
end

------------------------------------------------------
-- OBS 속성 설정
------------------------------------------------------
function script_properties()
    local props = obs.obs_properties_create()
    obs.obs_properties_add_text(props, "player_name", "Player Name (default: firefox)", obs.OBS_TEXT_DEFAULT)
    return props
end

------------------------------------------------------
-- 속성 값이 변경되었을 때 호출됨
------------------------------------------------------
function script_update(settings)
    local name = obs.obs_data_get_string(settings, "player_name")
    if name == nil or name == "" then
        player_name = "firefox"  -- 기본값
    else
        player_name = name
    end
end

------------------------------------------------------
-- 녹화 시작 시 호출될 콜백 함수
------------------------------------------------------
function on_recording_started()
    local cmd = "playerctl --player=" .. player_name .. " play &"
    os.execute(cmd)
    print("[obs-lua] playerctl play 실행됨: " .. cmd)
end

------------------------------------------------------
-- 스크립트 로드 시 호출
------------------------------------------------------
function script_load(settings)
    obs.obs_frontend_add_event_callback(function(event)
        if event == obs.OBS_FRONTEND_EVENT_RECORDING_STARTED then
            on_recording_started()
        end
    end)
end

