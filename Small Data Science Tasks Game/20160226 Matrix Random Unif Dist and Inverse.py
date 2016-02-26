# for "small data science tasks game"
# posted by Verena
# "Create a random matrix of size 5 x 5 with values between 0 and 10 (e.g. uniform distribution) and compute the inverse of it."

import numpy as np

#random number from uniform distribution between 0 and 10
#first used numpy random.uniform, but wanted integers, so changed to random.random_integers (documentation says it's uniform)
#http://docs.scipy.org/doc/numpy-1.10.0/reference/generated/numpy.random.random_integers.html#numpy.random.random_integers

#output some to test
#for i in range(1,10):
#    randnum = np.random.random_integers(0,10)
#    print(randnum)

#numpy has a built-in way to load a matrix with random numbers (or rather, to generate the numbers in matrix format)
rm = np.random.random_integers(0,10,size=(5,5))
print('\nRandom 5x5 matrix (integers 0 to 10):\n',rm)

#now invert the matrix using numpy linear algebra
#http://docs.scipy.org/doc/numpy-1.10.0/reference/generated/numpy.linalg.inv.html
#here's what a matrix inverse is: http://mathworld.wolfram.com/MatrixInverse.html
rm_inv = np.linalg.inv(rm)
print('\nInverse of matrix above:\n',rm_inv)

