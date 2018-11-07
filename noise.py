## Verify fluctuations in difference records 			##
## according to expectation of not exceeding 7 S.D.		##
## from Heinemann and Conti Methods in Enzymology 207		##
## Python Implementation
## Andrew Plested 2006
## 
## Takes input from tab-delimited Excel file 'file.txt'.
## Columns are current traces
## Mean and variance are computed for the set to use in limit calculation
## Baseline noise is determined for each difference trace from the first hundred points (2 ms at 50 kHz)
## Traces that exceed the limit are popped from the list and the failing points are explicitly listed to the terminal
## Output is tab delimited columns of verified traces 'verified.txt'


from math import *
import platform
from trace_tools import mean, variance, rmsd, traces_scale, trace_scale, traces_average, baselines_quality, baseline_subtract
from file_tools import file_read, file_write, traces_into_lines, lines_into_traces

def square (x): return x*x

def mean_inverse_baseline_sub(traces):
	"""get mean current waveform, invert for positive and subtract baseline"""

	mean = traces_average(traces)

	inverse_mean = trace_scale(mean,-1.0)

	mean_bs_sub = baseline_subtract(inverse_mean)
	
	return mean_bs_sub

def parameters ():
	
	Decimation = 1
	UNITARY_CURRENT = .5								#Previously estimated

    #print 'This platform calls itself', platform.system()


def load_traces(input_filename):
	data_in_lines = file_read(input_filename)
	input_traces = lines_into_traces (data_in_lines)
	#input_traces = traces_scale(in_traces,5)			# optional scaling if gain wrong
	
	print 'Read ',len(input_traces),' traces from file'
    return input_traces


def baselines()

	##get baseline variances and their statistics

	mean_sigma2_bs, rmsd_sigma2_bs, bs_variances = baselines_quality (input_traces)

	print 'Mean baseline variance = ', mean_sigma2_bs
	print 'RMSD of baseline variance =', rmsd_sigma2_bs
	print bs_variances

	## discard any trace with excessive baseline noise - Sigma2Bs gt Mean + 4 RMSD
	ex_noise_traces_to_pop = []

	for i in range (len(bs_variances)):
		if bs_variances[i] > mean_sigma2_bs + 4 * rmsd_sigma2_bs:
			ex_noise_traces_to_pop.append(i)

	## Reverse order so highest are popped first

	ex_noise_traces_to_pop.reverse()
	for x in ex_noise_traces_to_pop:
		input_traces.pop(x)
		
	print len(ex_noise_traces_to_pop), ' trace(s) had excessive baseline noise- discarded',ex_noise_traces_to_pop

	print len(input_traces)


def construct_diffs():
	## Construct difference traces according to transform of Sigg et al 1994
	difference_traces = []
	for x in range(len(input_traces)-1):
		diff = []
		for y in range(len(input_traces[0])):
			diff.append((input_traces[x+1][y]-input_traces[x][y])/2)			
		difference_traces.append(diff)							

	print 'Constructed ', len(difference_traces), ' difference traces'

	## calculate mean current, invert and subtract baseline
	mean_I_inverted_bs_sub = mean_inverse_baseline_sub(input_traces)

	##Recalculate mean baseline variance for remaining traces
	mean_sigma2_bs, rmsd_sigma2_bs, bs_variances = baselines_quality (input_traces)

	##calculate theoretical noise limit for each point in the trace
	limits = []
	for point in range(len(difference_traces[0])):
		
			I = abs(mean_I_inverted_bs_sub[point])
			limit =  7 * sqrt(UNITARY_CURRENT * I + mean_sigma2_bs)
			limits.append(limit)

	print 'Verifying variance of difference traces'

	excess_points, excess_limits, excess_differences = [],[],[]

	for difference_trace in difference_traces:
		
		excess,excess_limit,excess_difference = [],[],[]
		
		for i in range(len(difference_trace)):
			point = float(difference_trace[i])

			if abs(point) > limits [i]:
				excess.append(i)
				excess_limit.append(limits[i])
				excess_difference.append(point)
		
		excess_points.append(excess)
		excess_limits.append(excess_limit)
		excess_differences.append(excess_difference)


	failed_traces = 0					#No traces have failed at this point
	header_line = []

	difference_traces_to_pop = []
	input_traces_to_pop= []

	for i in range(len(difference_traces)):	
		if len(excess_points[i]) > 0:
			print 'Trace', i,' contained', len(excess_points[i]), 'points greater than the limit and was removed from set (Limit first).'
			print zip(excess_limits[i],excess_differences[i])
			difference_traces_to_pop.append(i)
			if input_traces_to_pop.count(i) == 0: 	#Check if this trace was already discarded last time
				input_traces_to_pop.append(i) 	
			input_traces_to_pop.append(i+1)	
			failed_traces += 1						#At least one trace has failed
			header_line.append(str(i))				#write to the header

	if failed_traces == 0:				
		print 'None had excess variance over 7 x predicted S.D.'

	#must pop traces in right order (highest first) otherwise numbering will be buggered. 

	difference_traces_to_pop.reverse()
	input_traces_to_pop.reverse()
	
	for x in difference_traces_to_pop:
		difference_traces.pop(x)

	for x in input_traces_to_pop:
		input_traces.pop(x)

	num_of_diff_traces = len (difference_traces)


def final_prep():

	## calculate mean current, invert and subtract baseline
	final_mean_I_inverted_bs_sub = mean_inverse_baseline_sub(input_traces)

	final_ensemble_variance = []

	for isochronous_point in range(len(difference_traces[0])):
		isochrone =[]
		for d_trace in difference_traces:
			isochrone.append(d_trace[isochronous_point])
		
		mean_dZt_squared = mean (map (square, isochrone))
		
		#factor of '2' because of dZt = 1/2 * {y(i+1)-y(i)}; Heinemann and Conti 
		final_ensemble_variance.append(2*mean_dZt_squared)				
		
	## Add Mean and Ensemble variances to output
	difference_traces.append(final_mean_I_inverted_bs_sub)
	difference_traces.append(final_ensemble_variance) 

	output_lines = traces_into_lines (difference_traces)

	## Finish constructing header line

	header_line.insert(0,'Verified Difference Current Traces')

	for x in range(num_of_diff_traces - failed_traces - 1):		
		#Insert correct number of spaces to get to <I> and <Variance>
		header_line.append('')	

	header_line.append('<I>')
	header_line.append('<Variance>')

	output_lines.insert(0,header_line)
	output_file = 'verified.txt'
				
	print 'Writing',num_of_diff_traces,'difference traces to',output_file,', plus mean and variance in last two columns...'	

	file_write (output_file,output_lines)

	print 'Done'
	

