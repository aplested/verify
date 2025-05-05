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

def mean_baseline_sub(traces, b_start=0, b_end=99):
    """called if traces are positive going
     get mean current waveform and subtract baseline"""

    mean = traces_average(traces)

    mean_bs_sub = baseline_subtract(mean, b_start, b_end)
    
    return mean_bs_sub

def mean_inverse_baseline_sub(traces, b_start=0, b_end=99):
	"""called if traces are negative going
    get mean current waveform, invert for positive and subtract baseline"""

	mean = traces_average(traces)

	inverse_mean = trace_scale(mean,-1.0)

	mean_bs_sub = baseline_subtract(inverse_mean, b_start, b_end)
	
	return mean_bs_sub

def parameters ():
	Decimation = 1


    #print 'This platform calls itself', platform.system()

#would be better to have a class so that could be initialized with parameters.

def clean_bad_baselines(input_traces, baseline_range=[0,99]):
    # bad traces are removed from input
    ##get baseline variances and their statistics

    b_start = baseline_range[0]
    b_end = baseline_range[1]
    mean_sigma2_bs, rmsd_sigma2_bs, bs_variances = baselines_quality (input_traces, b_start, b_end)

    print('Mean baseline variance = ', mean_sigma2_bs)
    print('RMSD of baseline variance =', rmsd_sigma2_bs)
    print(bs_variances)

    ## discard any trace with excessive baseline noise - Sigma2Bs gt Mean + 4 RMSD
    ex_noise_traces_to_pop = []

    for i in range (len(bs_variances)):
        if bs_variances[i] > mean_sigma2_bs + 4 * rmsd_sigma2_bs:
            ex_noise_traces_to_pop.append(i)

    ## Reverse order so highest are popped first

    ex_noise_traces_to_pop.reverse()
    for x in ex_noise_traces_to_pop:
        input_traces.pop(x)

    message = str(len(ex_noise_traces_to_pop))+" trace(s) had excessive baseline noise- discarded "+ str(ex_noise_traces_to_pop)
    #print len(input_traces)
    return input_traces, message


def construct_diffs(input_traces, UNITARY_CURRENT=.5, baseline_range=[0,99]):
    ## Construct difference traces according to transform of Sigg et al 1994

              #Previously estimated, should be passed from GUI
    messages =""
    b_start = baseline_range[0]
    b_end = baseline_range[1]
    
    difference_traces = []
    for x in range(len(input_traces)-1):
        diff = []
        for y in range(len(input_traces[0])):
            diff.append((input_traces[x+1][y]-input_traces[x][y])/2)
        difference_traces.append(diff)

    print('Constructed ', len(difference_traces), ' difference traces')

    ## calculate mean current, invert and subtract baseline
    mean_I_inverted_bs_sub = mean_inverse_baseline_sub(input_traces, b_start, b_end)

    ##Recalculate mean baseline variance for remaining traces
    mean_sigma2_bs, rmsd_sigma2_bs, bs_variances = baselines_quality (input_traces, b_start, b_end)

    ##calculate theoretical noise limit for each point in the trace
    limits = []
    for point in range(len(difference_traces[0])):
        
            I = abs(mean_I_inverted_bs_sub[point])
            limit =  7 * sqrt(UNITARY_CURRENT * I + mean_sigma2_bs)
            limits.append(limit)

    print('Verifying variance of difference traces')

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
            message = "Trace {} contained {} points greater than the limit and was removed from set\n".format(i, len(excess_points[i]))
            messages += message
            print(message)
            print(list(zip(excess_limits[i],excess_differences[i])))
            difference_traces_to_pop.append(i)
            if input_traces_to_pop.count(i) == 0: 	#Check if this trace was already discarded last time
                input_traces_to_pop.append(i)
            input_traces_to_pop.append(i+1)
            failed_traces += 1						#At least one trace has failed
            header_line.append(str(i))				#write to the header

    if failed_traces == 0:
        messages += "None had excess variance over 7 x predicted S.D.\n"

    #must pop traces in right order (highest first) otherwise numbering will be buggered.

    difference_traces_to_pop.reverse()
    input_traces_to_pop.reverse()

    for x in difference_traces_to_pop:
        difference_traces.pop(x)

    for x in input_traces_to_pop:
        input_traces.pop(x)

    num_of_diff_traces = len (difference_traces)

    return input_traces, difference_traces, messages, header_line


def final_prep(input_traces, difference_traces, baseline_range):
    b_start = baseline_range[0]
    b_end = baseline_range[1]
   
    ## check positive or negative peak
    #calculate mean current, invert if needed and subtract baseline
    
    first_trace = input_traces[0]
    abs_trace = list(map(abs,first_trace))
    
    if max(abs_trace) == max(first_trace):
        print("Verify detected positive-going first trace.")
        final_mean_I_bs_sub = mean_baseline_sub(input_traces, b_start, b_end)
    else :
        print("Verify detected negative-going first trace.")
        final_mean_I_bs_sub = mean_inverse_baseline_sub(input_traces, b_start, b_end)
        


    final_ensemble_variance = []

    for isochronous_point in range(len(difference_traces[0])):
        isochrone =[]
        for d_trace in difference_traces:
            isochrone.append(d_trace[isochronous_point])
        
        mean_dZt_squared = mean (list(map (square, isochrone)))
        
        #factor of '2' because of dZt = 1/2 * {y(i+1)-y(i)}; Heinemann and Conti
        final_ensemble_variance.append(2 * mean_dZt_squared)
    
    ## Add Mean and Ensemble variances to output
    difference_traces.insert(0, final_mean_I_bs_sub)
    difference_traces.insert(1, final_ensemble_variance)

    return difference_traces
    
def write_output (difference_traces, header_line, filename='verified.txt'):
    
    output_lines = traces_into_lines (difference_traces)

    ## Finish constructing header line
    header_line.insert(0, '<I>')
    header_line.insert(1, '<Variance>')
    header_line.insert(2, 'Verified Difference Current Traces')
    header_line.insert(3, 'Traces removed ->')

    output_lines.insert(0, header_line)
    output_file = filename

    print('Writing {} difference traces to {} with mean and variance in first two columns...'.format(len(difference_traces), output_file))

    file_write (output_file,output_lines)
    print('Done')




