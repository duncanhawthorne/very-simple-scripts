'''
Script to speed up "independent" functions by caching results. Independent in the sense that gets all information from the arguments, gives all information back through return values.
'''

from __future__ import division
import sys
sys.setrecursionlimit(200000)

cached_results  = {}

def cached(function, args):
	#print("running cached")
	assert type(args) == tuple, "you need to pass a tuple, if you want to pass one arg, pass (arg,)"
	if function in cached_results and args in cached_results[function]:
		return cached_results[function][args]
	else:
		answer = function(*args)
		if not function in cached_results:
			cached_results[function] = {}
		cached_results[function][args] = answer
		return answer

decode_list = {"current":None, "orig":None}
		
def bob(args):
	#print "bob", args
	return cached(decode_list["orig"], (args,))
		
def cached_seamless(function, args):
	'''
	This is not threadsafe
	'''
	#print function, args
	
	
	orig_function = function
	
	
	
	#print "cacehd_seamless", function, args
	decode_list["orig"] = function
	
	#print locals()
	
	for item in globals():
		if not item == "bob":
			if globals()[item] == function:
				external_function = item
	
	exec external_function+" = bob" in globals()
	
	answer =  cached(bob, (n,))
	
	exec external_function+" = decode_list['orig']" in globals()
	#now reset the function back again
	
	#TODO
	
	return answer
	

	
	
	
		
	
def fib_slow(n):
	#print("running fib_slow")
	if n == 1 or n == 2:
		return 1
	else:
		return fib_slow(n-1) + fib_slow(n-2)
		
def fib_fast(n):
	if n == 1 or n == 2:
		return 1
	else:
		return cached(fib_fast, (n-1,)) + cached(fib_fast, (n-2,)) 

def fib_with_cache(n):
	function, args = fib_with_cache, (n,)
	
	assert type(args) == tuple, "you need to pass a tuple, if you want to pass one arg, pass (arg,)"
	if function in cached_results and args in cached_results[function]:
		return cached_results[function][args]
	else:
	
		#START MAIN FUNCTION BODY
		if n == 1 or n == 2:
			answer = 1
		else:
			answer = fib_with_cache(n-1) + fib_with_cache(n-2)			
		#answer should be set to what would usually be the main return value
		#END MAIN FUNCTION BODY
		
		if not function in cached_results:
			cached_results[function] = {}
		cached_results[function][args] = answer
		return answer	
	

if __name__ == "__main__":
	n = 70
	
	#print globals()
	
	print cached_seamless(fib_slow, (10,))
	print cached_seamless(fib_slow, (n,))
	
	print fib_slow(n)
	
	#print cached(bob, (n,))
	quit()
	
	
	print(fib_fast(n))
	print(fib_with_cache(n))
	print(fib_slow(n))

