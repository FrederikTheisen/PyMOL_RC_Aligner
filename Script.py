INITIALMODE = True

def RMSD(elem):
    return elem[1][0]

bestlist = []
names = cmd.get_names()

name = names[0]
bestlist.append(name)

pl = len(cmd.get_fastastr(name)) - 10
stepsize = int(pl / 10)

selectionstring = " and (index 1-" + str(2*stepsize) 
selectionstring = selectionstring + " or index " + str(pl/2) + "-" + str(pl/2 + 1)
selectionstring = selectionstring + " or index " + str(pl-stepsize/4) + "-" + str(pl-1) + ")"

for i in range(0, len(names) - 1):
	dat = []
	local_names = cmd.get_names()
	print("running: " + name)
	
	for i in range(0, len(local_names)): 
		
		name_local = local_names[i]
		
		if name_local == name: continue
		if name_local in bestlist: continue;

		aln = []

		if INITIALMODE:
			cmd.do("select alns, " + name + selectionstring)
			aln = cmd.fit(name_local, "alns", cutoff=2000)
			rms = cmd.rms(name_local, name)
			aln = [rms]
		else: aln = cmd.align(name_local, name)

		dat.append([name_local, aln])

	dat.sort(key=RMSD)
	name = str(dat[0][0])
	bestlist.append(name)
	
for i in range(0, len(bestlist)-1):
	cur = bestlist[i]
	next = bestlist[i+1]

	if INITIALMODE:
		cmd.do("select alns, " + cur + selectionstring)
		cmd.fit(next, "alns", cutoff=2000)
	else : cmd.align(next, cur)

	cmd.do("join_states ens, " + cur)
	cmd.delete(cur)

cmd.do("join_states ens, " + bestlist[-1])
cmd.delete(bestlist[-1])
cmd.do("reset")
cmd.do("zoom")
