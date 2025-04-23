import sys
import os


def file_read(file):
    """Strip lines of ASCII text from file"""
    print('Reading ' + file + '....')
    with open(file, 'r') as f:
        block_lines = f.read()
    # Divide the file content into lines using newline characters
    lines_of_file = block_lines.split('\n')
    # Remove header (first line) and last line if blank
    if lines_of_file:
        if len(lines_of_file) > 0:
            del lines_of_file[0]  # Remove header
        if lines_of_file and lines_of_file[-1] == '':
            del lines_of_file[-1]
    print(lines_of_file[0])
    return lines_of_file


def file_write(file, data):
    """Write lines of data to ASCII file"""
    with open(file, "w") as f:
        for each_line in data:
            joined_line = '\t'.join(each_line)  # Use tab as separator
            f.write(joined_line)
            f.write('\r')  # Write a carriage return
    return


def addFilenamePrefix(path, prefix=""):
    # Take a path and add a prefix to the filename (for example, a datestamp)
    directory, filename = os.path.split(path)
    filename = prefix + filename
    return os.path.join(directory, filename)


def lines_into_traces(lines):
    """Convert a list of ASCII text lines into traces (a list of lists of floats)"""
    split_lines = []
    for line in lines:
        values = line.split('\t')  # Divide lines into values at tabs
        split_lines.append(values)
    traces = []
    num_of_traces = len(split_lines[0])  # Number of columns determines number of traces

    # Create empty lists for each trace
    for i in range(num_of_traces):
        traces.append([])

    # Transpose lines into traces (each column becomes a trace)
    for line in split_lines:
        for i in range(num_of_traces):
            traces[i].append(float(line[i]))

    return traces


def traces_into_lines(traces):
    """Convert traces (a list of lists of floats) into a list of ASCII text lines"""
    lines_of_output = len(traces[0])

    # Create an empty list for each line
    lines = []
    for i in range(lines_of_output):
        lines.append([])

    # Transpose the traces into lines
    for point in range(lines_of_output):
        for trace in traces:
            lines[point].append(str(trace[point]))

    return lines
