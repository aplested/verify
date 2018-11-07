import sys,os

def file_read (file):
	"""Strip lines of ASCII text from file"""
	print ('Reading '+file+'....')
	f=open(file, 'r')
	block_lines = f.read()
	f.close()							#close the file	
	
	#print block_lines
	eol = os.linesep
	lines_of_file = block_lines.split('\n') 				#divide into lines at carriage rtns
	del lines_of_file [0]						# header
	del lines_of_file [-1]						# last line is blank so remove it
	print lines_of_file [0]
	return lines_of_file
	
def file_write (file,data):
	"""Write lines of data to ASCII file"""
	f=open(file, "w")
	for each_line in data:
		joined_line = '\t'.join(each_line)  	# \t for tab
		f.write(joined_line) 					# Write the isochronous line.
		f.write('\r') 							# write a carriage return what a nasty hack!
	f.close()
	return

def lines_into_traces (lines):
	"""Convert a list of ASCII text lines into traces (a list of lists of floats)""" 
	#print lines
	split_lines=[]
	for line in lines:
		values=line.split('\t')					#divide lines into values at tabs
		split_lines.append(values)
	#print split_lines
	traces = []
	num_of_traces = len(split_lines[0])			#work out how many traces from the no of columns
	
	## make an empty list
	for i in range(num_of_traces):
		traces.append([])
	
	## transpose lines into traces made from columns	
	for line in split_lines:
		for i in range (num_of_traces):
			traces[i].append (float(line[i]))   
		
	return traces

def traces_into_lines (traces):
	"""Convert traces (a list of lists of floats) into a list of ASCII text lines""" 
	
	lines_of_output=len(traces[0])

	## make an empty list
	lines = []
	for i in range(lines_of_output):
		lines.append([])

	## transpose the traces into lines
	for point in range(0,lines_of_output):		
		for trace in traces:
			lines[point].append(str(trace[point]))

	return lines
