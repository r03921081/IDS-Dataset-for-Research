f1 = open("adult_testing.csv", "r")
f2 = open("testing.csv", "w")
l = f1.readline()
f2.write(l)
for line in f1:
	write_line = []
	for token in line.split(","):
		if token.isdigit() == True:
			#print token
			write_line.append(token)
		else:
			#print token[1:]
			write_line.append(token[1:])
	print line
	print write_line
	print

	f2.write(",".join(map(lambda x: str(x), write_line))) 