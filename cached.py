'''
Script to speed up "independent" functions by caching results. Independent in the sense that gets all information from the arguments, gives all information back through return values.
'''

from __future__ import division
import sys
sys.setrecursionlimit(200000)

cached_results  = {}
def cached(function, args):
	assert type(args) == tuple, "you need to pass a tuple, if you want to pass one arg, pass (arg,)"
	if function in cached_results and args in cached_results[function]:
		return cached_results[function][args]
	else:
		answer = function(*args)
		if not function in cached_results:
			cached_results[function] = {}
		cached_results[function][args] = answer
		return answer
	
def fib_slow(n):
	if n == 1 or n == 2:
		return 1
	else:
		return fib_slow(n-1) + fib_slow(n-2)
		
def fib_fast(n):
	if n == 1 or n == 2:
		return 1
	else:
		return cached(fib_fast, (n-1,)) + cached(fib_fast, (n-2,)) 

if __name__ == "__main__":
	print fib_fast(35)
	print fib_slow(35)

