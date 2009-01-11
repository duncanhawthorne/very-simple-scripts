import random, math
#500 voters
#6 candidates



def distance(a, b):
	total = 0
	for i in range(len(a)):
		total += (a[i] - b[i])**2
	return math.sqrt(total)

def order(a, list):
	global whoisin
	total = 0
	for i in range(len(list)):
		if i in whoisin:
			if a >= list[i]:
				total += 1
			#if a == list[i]:
				
	return total


def howmany(place, candidate):
	total = 0
	for i in range(0, numvoters):
		if voterprefs[i][candidate] == place:
			total += 1
	return total
	
def howmuch(place, candidate):
	total = 0
	for i in range(0, numvoters):
		if voterchoice[i] == candidate:
			total += 1
	return total	
			

btrstvutility = 0
stvutility = 0
fptputility = 0
numvoters = 500
numcandidates = 6
random.seed()

for repeat in range(0, 1000):
	print repeat
	try:
		whoisin = [0,1,2,3,4,5]

		voterpos = []
		for i in range(0, numvoters):
			voterpos.append([random.random(), random.random(), random.random()])
	
		candipos = []
		for i in range(0, numcandidates):
			candipos.append([random.random(), random.random(), random.random()])

		voterdist = []
		for i in range(0, numvoters):
			voterdist.append([])
			for j in range(0, numcandidates):
				voterdist[i].append(distance(voterpos[i], candipos[j]))





		for k in range(0, numcandidates-1):

			voterprefs = []		
			for i in range(0, numvoters):
				voterprefs.append([])
				for j in range(0,numcandidates):

					voterprefs[i].append(order(voterdist[i][j], voterdist[i]))

			

			#for line in voterchoice:
			#	print line
			#print voterchoice



			voterchoice = []
			for i in range(0, numvoters):
				for j in range(0, numcandidates):
					if order(voterprefs[i][j], voterprefs[i]) == 1:
						voterchoice.append(j)




			candidatesfirsts = []
			for i in range(0, numcandidates):
				candidatesfirsts.append(howmany(1, i))
	
			#print candidatesfirsts
		
			setbob=0
			setfred=0
		
			#print whoisin
			for i in range(0, numcandidates):
				#print order(candidatesresults[i], candidatesresults)
			
				if order(candidatesfirsts[i], candidatesfirsts) == 1:#smallest number of firsts
					setbob=1
					bob = i
				if order(candidatesfirsts[i], candidatesfirsts) == 2:#second smallest number of firsts
					setfred=1
					fred = i
		
			#print setfred
			#print setbob		
	
			voterchoice = []
			for i in range(0, numvoters):
				if order(voterprefs[i][bob], voterprefs[i]) < order(voterprefs[i][j], voterprefs[fred]):#bob better than fred
					voterchoice.append(bob)
				else:
					voterchoice.append(fred)
			#print voterchoice		
			
			candidatesfirsts = []
			#print candidatesfirsts
			for i in range(0, numcandidates):
				candidatesfirsts.append(howmuch(1, i))
		
			#print candidatesfirsts
			#print bob
			#print fred
			#print whoisin
	
			for i in range(0, numcandidates):
				if candidatesfirsts[bob] < candidatesfirsts[fred]:#smallest number of firsts	
					whoisin.remove(bob)#
					for m in range(0, numvoters):
						voterdist[m][bob] = 100
					break
				else:
					whoisin.remove(fred)
					for m in range(0, numvoters):
						voterdist[m][fred] = 100
					break
	

		btrstv = whoisin[0]
		#print "btrstv winner:"	
		#print whoisin


		#now onto stv
		whoisin = [0,1,2,3,4,5]

		voterdist = []
		for i in range(0, numvoters):
			voterdist.append([])
			for j in range(0, numcandidates):
				voterdist[i].append(distance(voterpos[i], candipos[j]))





		for k in range(0, numcandidates-1):

			voterprefs = []		
			for i in range(0, numvoters):
				voterprefs.append([])
				for j in range(0,numcandidates):

					voterprefs[i].append(order(voterdist[i][j], voterdist[i]))

			

			#for line in voterchoice:
			#	print line
			#print voterchoice



			voterchoice = []
			for i in range(0, numvoters):
				for j in range(0, numcandidates):
					if order(voterprefs[i][j], voterprefs[i]) == 1:
						voterchoice.append(j)




			candidatesfirsts = []
			for i in range(0, numcandidates):
				candidatesfirsts.append(howmany(1, i))
	
			#print candidatesfirsts
	
	
			for i in range(0, numcandidates):
				#print order(candidatesresults[i], candidatesresults)
				if order(candidatesfirsts[i], candidatesfirsts) == 1:
					whoisin.remove(i)#
					for m in range(0, numvoters):
						voterdist[m][i] = 100
					break
			#print whoisin

			
		stv = whoisin[0]
		#print "stv winner:"	
		#print whoisin	













		#now onto fptp
		whoisin = [0,1,2,3,4,5]

		voterdist = []
		for i in range(0, numvoters):
			voterdist.append([])
			for j in range(0, numcandidates):
				voterdist[i].append(distance(voterpos[i], candipos[j]))





		voterprefs = []		
		for i in range(0, numvoters):
			voterprefs.append([])
			for j in range(0,numcandidates):

				voterprefs[i].append(order(voterdist[i][j], voterdist[i]))

		

		#for line in voterchoice:
		#	print line
		#print voterchoice



		voterchoice = []
		for i in range(0, numvoters):
			for j in range(0, numcandidates):
				if order(voterprefs[i][j], voterprefs[i]) == 1:
					voterchoice.append(j)




		candidatesfirsts = []
		for i in range(0, numcandidates):
			candidatesfirsts.append(howmany(1, i))

		#print candidatesfirsts


		for i in range(0, numcandidates):
			#print order(candidatesresults[i], candidatesresults)
			if order(candidatesfirsts[i], candidatesfirsts) == numcandidates -1:
				whoisin = [i]
				break


		#print "fptp winner:"
			
		#print whoisin
		fptp = whoisin[0]


		##now onto mass stv elimination
		












		for m in range(0, numvoters):
			btrstvutility += distance(candipos[btrstv], voterpos[m])
			stvutility += distance(candipos[stv], voterpos[m])
			fptputility += distance(candipos[fptp], voterpos[m])

		#print btrstvutility	
		#print stvutility
		#print fptputility
	except:
		continue
	
print btrstvutility	
print stvutility
print fptputility


#results after 1000 trials:
#265817.056303
#266164.402722
#296656.00766
	
