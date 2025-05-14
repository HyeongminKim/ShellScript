function LookupDate(input)
  local fmt
  if input == "d" then
    fmt = "%m월 %d일"
  elseif input == "D" then
    fmt = "%Y년 %m월 %d일"
  elseif input == "t" then
    fmt = "%H:%M"
  elseif input == "T" then
    fmt = "%H시 %M분"
  elseif input == "f" then
    fmt = "%Y-%m-%d %H:%M"
  elseif input == "F" then
    fmt = "%Y년 %m월 %d일 %H:%M"
  else
    return "usage: dt[dDtTfF]"
  end
  return os.date(fmt)
end

ime.register_command("dt", "LookupDate", "날짜·시간 입력")
