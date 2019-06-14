f = open("utf8-ZhuYin.map", 'r', encoding = 'utf-8')
content = f.readline()

trans_map = {}
while content:
	if content[2] not in trans_map:
		trans_map[content[2]] = content[0]
	else:
		trans_map[content[2]] += " " + content[0]

	if "/" in content:
		loc = [i + 1 for i, e in enumerate(content) if e == "/"]
		loc.insert(0, 2)
		for i in range(1, len(loc)):
			if content[loc[i]] != content[loc[i - 1]]:
				if content[loc[i]] not in trans_map:
					trans_map[content[loc[i]]] = content[0]
				else:
					trans_map[content[loc[i]]] += " " + content[0]

	content = f.readline()

f.close()

z = open("ZhuYin-utf8.map", 'w', encoding = 'utf-8')
for k, v in trans_map.items():
	z.write("%s %s\n" % (k, v))
	for s in v.replace(" ", ""):
		z.write("%s %s\n" % (s, s))

z.close()