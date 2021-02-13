import sys

digit_string = sys.argv[1]

sum = 0
for letter in digit_string:
    sum += int(letter)

print(sum)