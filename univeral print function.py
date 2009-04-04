try:#python 3
	exec('echo = print')
except SyntaxError:#python 2
	def echo(*args):
		for arg in args:
			exec('print arg,')
		exec('print ""')

bob = [17, 14, 5]
echo("freddy", "was", "here", bob)
echo("sarah")
echo(bob)
