import sys; args = sys.argv[1:]
myList = open(args[0], 'r', encoding = 'ascii', errors = 'ignore').read()

print(myList)