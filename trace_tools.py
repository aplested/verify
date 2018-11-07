from math import sqrt

def mean(data):
	"""Take the mean of a list of floats"""
	sum = 0.0
	for value in data:
		sum += value

	return sum/len(data)

def variance(data):
	"""Take the variance of a list of floats"""
	
	sum = 0.0
	m = mean (data)
	for value in data:
		sum += (value - m)**2

	return sum / (len(data) - 1)

def rmsd(data):
	"""Take the R.M.S.D of a list of floats"""
	n = len(data)	
	mean_sq_dev = variance(data) * (n-1) / n

	return sqrt(mean_sq_dev)


def baseline_subtract (trace,start=0,end=99):
	"""Subtract the mean of first 100 points (default) from a trace to correct leak"""
	
	mean_bs = mean (trace[start:end])			

	trace_bs_subtracted = []
	for point in trace:
		trace_bs_subtracted.append(point-mean_bs)
	
	return trace_bs_subtracted

def baselines_quality (traces,start=0,end=99):
	"""Calculate the mean and RMSD of baseline variance for a set of traces"""
	bs_var_of_traces = []	

	for trace in traces:
		bs_variance = variance (trace[start:end])
		bs_var_of_traces.append(bs_variance)

	mean_variance = mean (bs_var_of_traces)
	rmsd_variance = rmsd (bs_var_of_traces)
	
	return mean_variance,rmsd_variance,bs_var_of_traces

def traces_average (traces):
	"""Calculate average of a set of traces"""
	
	average = []

	for isochronous_point in range(len(traces[0])):				#use the length of first trace
		isochrone =[]
		for trace in traces:
			isochrone.append(trace[isochronous_point])
		isochrone_mean = mean(isochrone)

		average.append(isochrone_mean) 
	
	return average

def traces_scale (traces,gain=1):
	"""Scale a set of traces"""
	scaled_traces =[]
	for trace in traces:
		x = trace_scale(trace,gain)
		scaled_traces.append(x)		
	return scaled_traces

def trace_scale (trace,gain=1):
	"""Scale trace"""
	scaled = []
	for point in trace:
		scaled.append(point * gain)
	return scaled

def decimate_traces(traces,decimation=1):
	decimated_traces = []
	for trace in traces:
		decimated = []
		for point in range(0,len(trace),decimation):
			decimated.append(trace[point])
		
		decimated_traces.append(decimated)
	
	return decimated_traces

def chop_traces(traces,begin,end):
	"""Remove junk from beginning and end of trace """
	
	chopped_traces = []
	for trace in traces:
		
		chopped = trace [begin:end]
		chopped_traces.append(chopped)

	return chopped_traces