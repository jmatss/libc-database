from sys import argv
from operator import itemgetter
import os, re

class Argument:
	def __init__(self, name, adr):
		self.name = name
		self.adr = int(adr[2:], 16) if adr == "0x" else int(adr, 16)

# TODO: Add items to result as sorted (binary insertion) instead of doing sort at the end (bisect?)
def usage():
	print("%-7s %s" % ("usage:", "<name> <address> <name> <address> ..."))
	print("%-7s %s" % ("", "<name> <address> <name> <address> ... <list n closest files>"))
	exit()

def create_pattern(arguments):
	pattern = ""
	for i, argument in enumerate(arguments):
		if i > 0:
			pattern += "|"
		pattern += re.escape(argument.name)
	return re.compile("^(" + pattern + ")\s")

def find_offset_diff(arguments):
	offsets = []
	root_dir = "db" if len(os.path.dirname(argv[0])) == 0 else os.path.dirname(argv[0]) + "/db"

	for filename in os.listdir(root_dir):
		if filename.endswith(".symbols"):
			offsets.append((filename, abs(find_offset(arguments, filename, root_dir))))
	return offsets

def find_list_index(the_list, substring):
	for i, s in enumerate(the_list):
		if substring in s:
			return i
	return -1

def find_offset(arguments, filename, root_dir):
	pattern = create_pattern(arguments)
	results = find_positions(pattern, filename, root_dir)

	# TODO: more comparisons to get more accurate results(?)
	offset = 0
	i = find_list_index(results, arguments[0].name)
	for j, argument in enumerate(arguments):
		if j == 0:
			continue
		k = find_list_index(results, arguments[j].name)
		offset += abs( abs(arguments[0].adr - arguments[j].adr) - abs(int(results[i].split()[1], 16) - int(results[k].split()[1], 16)) )

	return offset

def find_positions(pattern, filename, root_dir):
	results = []
	for i, line in enumerate(open(root_dir + "/" + filename)):
		if pattern.search(line):
			results.append(line.strip())
	return results

if len(argv) < 5:
	usage()

arguments = []
i = 1
while(i < len(argv) - 1):
	arguments.append(Argument(argv[i], argv[i+1]))
	i+=2

n = int(argv[-1]) if len(argv) % 2 == 0 else 3
results = find_offset_diff(arguments)
results.sort(key = itemgetter(1))
n = len(results) if n > len(results) else n

for i in range(n):
	print("%s (diff: 0x%x)" % (results[i][0], results[i][1]))