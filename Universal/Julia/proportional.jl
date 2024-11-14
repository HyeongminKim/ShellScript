#!/home/hm/.juliaup/bin/julia

if length(ARGS) > 4 || length(ARGS) < 3
    @error "Usage: A B C [E <1: A:B=C:X, 2: A:B=X:C>]"
    exit(1)
end

params = zeros(Int64, 4)
for i in 1:length(ARGS)
    params[i] = parse(Int64, ARGS[i])
end

println("=== Choose calculation type ===")
println("1. A:B=C:X")
println("2. A:B=X:C")
print("> ")
if(length(ARGS) == 3)
    params[4] = parse(Int8, readline())
end

if length(ARGS) == 4
    println(join([params[4], " (argv)"]))
end

if params[4] > 2 || params[4] < 1
    @error join(["E value should be 1 or 2. (current value: ", params[4], ")"])
    exit(1)
end

if params[4] == 1
    Z = params[2] * params[3]
    X = Z / params[1]
    println(join([params[1], ":", params[2], " = ", params[3], ":X"]))
else
    Z = params[1] * params[3]
    X = Z / params[2]
    println(join([params[1], ":", params[2], " = ", "X:", params[3]]))
end

println(join(["X = ", X]))

