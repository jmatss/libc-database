from sys import argv
import os, re


def usage():
	print("%-7s %s %s" % ("usage:", argv[0], "<regex (on the symbol files)> ..."))
	print("%-7s %s %s" % ("", argv[0], "<regex (on the symbol files)> ... \"-\" <name> ..."))
	exit()


def find_matches(arguments):
	root_dir = "db" if len(os.path.dirname(argv[0])) == 0 else os.path.dirname(argv[0]) + "/db"

	# Turn arguments into regex
	patterns = []
	for argument in arguments:
		patterns.append(re.compile(argument))

	# Loop through all files and add files that match ALL arguments to results
	for filename in os.listdir(root_dir):
		if filename.endswith(".symbols"):
			file_results = []
			file_patterns_matched = [False] * len(arguments)

			for _, line in enumerate(open(root_dir + "/" + filename)):
				for i, pattern in enumerate(patterns):
					if pattern.search(line):
						file_patterns_matched[i] = True
						file_results.append(line)

			if False not in file_patterns_matched:
				yield (filename, file_results)


if len(argv) < 2:
	usage()

for result in find_matches(argv[1:]):
	print(result[0])
	for line in result[1]:
		print("  " + line.strip())
