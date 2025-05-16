obs = obslua

player_name = "firefox"

function script_description()
    return "playerctl 상태를 OBS 상태바에 1초마다 표시합니다."
end

function script_properties()
    local props = obs.obs_properties_create()
    obs.obs_properties_add_text(props, "player_name", "Player Name (예: firefox)", obs.OBS_TEXT_DEFAULT)
    return props
end

function script_update(settings)
    local name = obs.obs_data_get_string(settings, "player_name")
    if name ~= nil and name ~= "" then
        player_name = name
    end
end

function update_status_to_statusbar()
    -- 먼저 상태 확인
    local status_cmd = string.format("playerctl --player=$(playerctl -l | grep %s) status", player_name)
    local status_handle = io.popen(status_cmd)
    local status = status_handle:read("*a"):gsub("\n", ""):lower()
    status_handle:close()

    local result = ""

    if status == "playing" then
        local info_cmd = string.format("playerctl --player=$(playerctl -l | grep %s) metadata --format '{{duration(position)}} / {{duration(mpris:length)}}'", player_name)
        local info_handle = io.popen(info_cmd)
        local info = info_handle:read("*a")
        info_handle:close()

        result = string.format("▶ %s [%s]", player_name, info:gsub("\n", ""))

        obs.script_log(obs.LOG_INFO, result)
    end
end

function script_load(settings)
    obs.timer_add(update_status_to_statusbar, 1000)
end

