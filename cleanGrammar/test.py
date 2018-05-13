
def weird_chars(a, b):
	assert a < b
	for i in range(a, b):
	    print(i, ': ', chr(i))

x = 1
def increment_var():
	global x
	x += 1
	print(x)

increment_var()
print(x)
	
