import sys

length = int(sys.argv[1])

for i in range(1, length + 1):
    print(' ' * (length - i) + '#' * i)