#To use as main, run python SecurityService.py "http request message"
#in command line.

import sys

primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] 
	 
def hash(message):
	message = str(message)
	length = len(message)

	count = 0
	index = 0
	value = 0

	for c in message:
		if(count%2 == 0):
			c_val = ord(c)
			value = value + (c_val*primes[index])

			if(index == len(primes)-1):
				index = 0
			else:
				index = index + 1

		count = count + 1

	return value


def encrypt(message):
	value = hash(message)
	return value


if __name__ == "__main__":
	arg = str(sys.argv[1])
	value = encrypt(arg)
	print value
