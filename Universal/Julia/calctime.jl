using Dates

function normalize_time(hour::Int64, min::Int64, sec::Int64) :: Dates.CompoundPeriod
    rawTime = (hour * 60 * 60) + (min * 60) + sec
    seconds = rawTime
    hours = trunc(Int64, seconds / 3600)
    seconds = seconds % 3600
    minutes = trunc(Int64, seconds / 60)
    seconds = trunc(Int64, (seconds % 60))
    return Dates.CompoundPeriod(Hour(hours), Minute(minutes), Second(seconds))
end 

function normalize_time(compoundTime::Dates.CompoundPeriod) :: Dates.CompoundPeriod
    hours = 0
    minutes = 0
    seconds = 0
    for p in compoundTime.periods
        type = typeof(p)
        if(type == Dates.Hour)
            hours = p.value
        elseif(type == Dates.Minute)
            minutes = p.value
        elseif(type == Dates.Second)
            seconds = p.value
        end
    end
    return normalize_time(hours, minutes, seconds)
end

function validate_time(tag::String, source::String) :: Vector{SubString{String}}
    test = split(strip(source))
    if(length(test) != 3)
        @error join([tag, " Array<T> should be 3 elements. (current value: ", length(test), ")"])
        exit(1)
    end
    return test
end

print("first time (h m s) > ")
rawInput = readline()
test = validate_time("firstTime", rawInput)
firstTime = normalize_time(parse(Int64, test[1]), parse(Int64, test[2]), parse(Int64, test[3]))

print("operator (+|-) > ")
operator = strip(readline())

print("last time (h m s) > ")
rawInput = readline()
test = validate_time("lastTime", rawInput)
lastTime = normalize_time(parse(Int64, test[1]), parse(Int64, test[2]), parse(Int64, test[3]))

if operator == "+"
    println(normalize_time(firstTime + lastTime))
elseif operator == "-"
    println(normalize_time(firstTime - lastTime))
else
    @error join(["operator ", operator, " does not supported."])
    exit(1)
end
