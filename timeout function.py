"sudo apt-get install espeak python-mechanize"
import os, time, sys, mechanize, threading, random, copy
from multiprocessing.pool import ThreadPool
pool = ThreadPool(processes=1)

threadmatch = {}

def foo(args):
	global threadmatch
	newargs = args[:-2]
	thefunc = args[-2]
	random = args[-1]
	threadmatch[random] = thefunc(*newargs) 
  
def tpx(x,y,z):
	time.sleep(5)
	return 1000000+x+y+z

def timeout(function, arguments, timelimit):
	threadmatch = {}
	def underlying_in_thread(args):
		newargs = args[:-2]
		thefunc = args[-2]
		random = args[-1]
		threadmatch[random] = thefunc(*newargs) 
	

	r = random.random()
	arguments = list(arguments)
	arguments.append(function)
	arguments.append(r)
	a = arguments[-1]
	threadmatch[a] = a
	initial = copy.copy(a)
	async_result = pool.apply_async(underlying_in_thread, [arguments]) 
	start = time.time()
	while time.time() < start + timelimit:	
		if threadmatch[a] != initial: #i.e. function changed and answer updated
			return threadmatch[a]
		time.sleep(0.01)
	return "timed out"

print "tpx", tpx(1,2,3)
print "timeout", timeout(tpx, (1, 2, 3), 7)

