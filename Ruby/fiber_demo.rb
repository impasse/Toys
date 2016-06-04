fib = Fiber.new do |v|
	loop do
		v = Fiber.yield v*v
	end
end

for v in 0..100 do
	p fib.resume v
end
