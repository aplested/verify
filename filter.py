## Digital Gaussian Filter from Blue Book Chapter 19 ##
## Python Implementation
## Andrew Plested 2006
## 
## Takes input from tab-delimited Excel file 'file.txt'.
## Each column of file should be one trace
## Filter fc is expressed in units of sampling frequency
## Output is tab delimited columns of filtered traces 'filtered.txt'
## Excluded light sampling shortcut
##



from math import *
from trace_tools import baseline_subtract

def gaussian (fc):
# Calculate coefficients of gaussian filter 	
	
	sigma = 0.13205 / fc
	nc = int ( 4 * sigma) +1 #python rounds down
	
	B = -0.5 / ( sigma * sigma)
	a = []


	
	sum = 0
	for i in range (nc):
		coefficient = exp ( B * i * i)
		a.append (coefficient)
		sum = sum + coefficient
	
	# normalise coefficients
	norm = 2 *sum - 1
	print 'Normalized coefficients of Gaussian filter'
	for x in range(len(a)):
		a [x] = a [x]/norm
		print x, a[x]
	return a

def filter_fn (input, coeffs):
## filtering function
	out =[]
	
	
	np = len (input)
	nc=len (coeffs) -1    # The central component is the zeroth, therefore reduce
					#Actual number of comps in sum is now 2nc +1 
	i = 0
	while i < (np):
		
		jl = i - nc
		if jl < 0: jl = 0
		ju = i + nc +1
		if ju > np: ju = np
		sum = 0
		
		for j in range (jl,ju):
	
			k = abs(j-i)	#which component	
			sum = sum + input [j] * coeffs[k]	
		out.append(sum)
		i = i + 1
	
	return out

def filter_traces(traces,fc=0.1):	# 5 kHz if sampling is 50kHz
	"""Takes a list of traces and passes them to the filter"""
					
	a = gaussian (fc)
	filtered = []

	for each_trace in traces:
		filter_output = filter_fn (each_trace,a) 	#Send each trace in turn to gaussian filter
					
		filtered.append(filter_output)
	
	return filtered

def file_read (file):
	"""Strip from file"""
		
	f=open(file, 'r')
	LinesOfFile = f.readline()		#takes whole file as a string because it doesn't recognise 
							#carriage returns
	Lines= LinesOfFile.split('\r')  ##divide into lines at carriage rtns
	
	split_lines=[]
	for line in Lines:
		values=line.split('\t')	#divide lines into values at tabs		
		split_lines.append(values)
	
	#Look at the first element of the first line
	try:
		t = float(split_lines[0][0])			
		Header = False
	
	#If it's not a number, it's probably the header	
	except ValueError:
		Header = split_lines.pop(0)
		print 'HEADER',Header	
	#print split_lines

	traces = []
	#work out how many traces from the no of columns
	num_of_traces = len(split_lines[0])			
	
	## make an empty list
	for i in range(num_of_traces):
		traces.append([])
	
	## transpose lines into traces made from columns	
	for line in split_lines:
		try:
			for i in range (num_of_traces):
				#print i,line[i]
				traces[i].append (float(line[i]))   
		except ValueError:
			print ' reached a non-numeric element, assumed eof'
			break	
	#print traces
				
	f.close()	#	close the file	
	return traces,Header

def main():
	#Begin main loop by getting a list of traces from the input file
	input_traces,Header=file_read('file.txt')

	print 'Number of Input Traces:',len(input_traces)
	fc =0.1
	
	#subtract the baseline
	bs_sub_traces = []
	n = 0
	for trace in input_traces:
		bs_sub_trace = baseline_subtract(trace,1600,2000)
		bs_sub_traces.append(bs_sub_trace)	
		n += 1
		print n,'',
	#send traces for filtering
	filtered_traces = filter_traces(bs_sub_traces,fc)

	

	lines_of_output = len(filtered_traces[0])
	decimation = 5

	#make an empty list with the right number of lines to write
	output_lines = []
	for i in range(0,lines_of_output,decimation):
		output_lines.append([])
	
	
	#transpose the traces into lines
	for i in range(0,lines_of_output,decimation):		
		for t in filtered_traces:
			output_lines[i/decimation].append(str(t[i]))

	OutputFile = 'filtered.txt'
	f=open(OutputFile, "w")			


	if Header is not False:
		#If we think that ripped a header, join it and write it to the o/p file.
		JoinedHeader = '\t'.join(Header)
		f.write(JoinedHeader)


		f.write('\r') 	

	for each_line in output_lines:
		joined_line = '\t'.join(each_line)   #\t for tab
		f.write(joined_line) 	# Write the isochronous line.
		f.write('\r') 		
				# write a carriage return what a nasty hack!
	f.close()

	print 'There were',len(filtered_traces),' traces, each of ',lines_of_output,' points'
	print 'Filtered at', fc,' times sampling frequency'
	print 'Decimated ',decimation,'-fold'
	print len(output_lines),' lines output to', OutputFile
