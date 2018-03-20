import re
import argparse
import os

if __name__ == '__main__':

    # parse user inputs
    parser = argparse.ArgumentParser(description = 'Extracts barcode sequence from file name and appends it to sequence lines in file.')
    parser.add_argument('-i', '--in_directory', help ='Directory containing sequence data files.')
    parser.add_argument('-o', '--out_directory', help = 'Directory for re-barcoded output files.')
    parser.add_argument('-r', '--regex', default = '[ATGC]{8}\+[ATGC]{8}',  help = 'Regular expression for extracting sample barcodes.')

    opts = parser.parse_args()

    i = opts.in_directory
    o = opts.out_directory
    r = opts.regex
    
# function to find sample ID (barcode) in file name
# our regex: [ATGC]{8}\+[ATGC]{8}
def find_SampleID(fileline, regexSample):
	sampleID_match = re.match(".*("+regexSample+").*", fileline)
	if sampleID_match:
		sampleID = sampleID_match.groups()[0]
		barcodes = sampleID.split('+') # list of 2
		return barcodes
	else:
		return None

# function to add the sample ID (barcode) to each line of the file
def re_index(in_dir, out_dir, regex):
	
	files = os.listdir(in_dir)
	
	# make the output directory if it doesn't already exist
	if not os.path.exists(out_dir):
		os.makedirs(out_dir)
	
	for f in files:
		
		# get the inputs and outputs ready
		infile = os.path.join(in_dir + f)
		outfile = os.path.join((out_dir + f + '_rebarcoded'))
		
		# open the file
		with open(infile, 'r') as infile:
			lineNumber = 0 # set the counter to 0 for the first line
			for line in infile:
				if lineNumber == 0: # if first line, or every other line thereafter...
					
					# sample barcode from fasta header
					bcs = find_SampleID(line, regex)
					
					# check that the barcode was found
					if not bcs:
						raise ValueError('Did not find barcode in sample file name.')
					
					# get the first and second barcodes
					bc1 = bcs[0]
					bc2 = bcs[1]
					
					# rewrite the header line to the output file
					newline = line # doesn't seem to need new line 
					with open(outfile, 'a') as of:
						of.write(newline)
					lineNumber = 1 # advance the counter
				
				else:
					# parse line and write to file
					rm_new = line.rstrip() # get rid of trailing newline character
					newline = bc1 + rm_new + bc2 + '\r\n'
					with open(outfile, 'a') as of:
						of.write(newline)   
					
					lineNumber = 0 # reset the counter                

# run the file with the user inputs
re_index(i, o, r)
		