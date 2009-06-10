'''
Script to speed up "independent" functions by caching results. Independent in the sense that gets all information from the arguments, gives all information back through return values.
'''

from __future__ import division,  print_function
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

def cached_seamless(*arguments):
	'''
	This is not safe to be called multiple time until it is finished
	'''
	
	try: #should be if has attribute
		cached_seamless.first_run #check if this is defined
		#second run
		assert cached_seamless.first_run == False
		args, = arguments #so we are just getting args
	except:
		cached_seamless.first_run = True #first run, 
		function, args = arguments #so we are getting a function and argument
	
	if cached_seamless.first_run == True:
	
		#remember the original function for later
		cached_seamless.orig_function = function
	
		this_function_name = "cached_seamless"
	
		#as the external function remains unchanged, 
		#we need to change the function it calls to be this one
		#first find out that functions name	
		for item in globals():
			if not item == this_function_name:
				if globals()[item] == function:
					external_function = item
	
		#now set its value globally to actually refer to this function
		exec(external_function+" = "+this_function_name) in globals()

		#so that next time it wont do the setup again, 
		#change the first_run to be False
		cached_seamless.first_run = False	
		answer =  cached(cached_seamless, (n,)) #THIS IS THE MEAT
	

		#now reset the function back again
		exec(external_function+" = cached_seamless.orig_function") in globals()
		del cached_seamless.first_run
		del cached_seamless.orig_function
	
		#this is the final exit from the function
		return answer

	else:
		#the recursive function will get here lots of times
		#and pass the arguments straight over to the cached function
		return cached(cached_seamless.orig_function, (args,))	
	
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
	n = 2000

	cached_results  = {} #just put this here to show if starting from scratch
	print(cached_seamless(fib_slow, (n,)))
	
	cached_results  = {} #just put this here to show if starting from scratch
	print(fib_fast(n))
	
	cached_results  = {} #just put this here to show if starting from scratch
	print(fib_with_cache(n))
	
	#now for the slow one
	print(fib_slow(n))

