import sys

def test_length_equality(x,y):
	"""Assertion test of the length of 2 arrays"""
	try:
		assert len(x) == len(y)
	except AssertionError:
		print("Length of x: %i" %len(x))
		print("Length of y: %i" %len(y))
		sys.exit("x and y vectors are of different length")

		