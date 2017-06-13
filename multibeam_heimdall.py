import multiprocessing
import os
import argparse
import subprocess
import time

parser = argparse.ArgumentParser(description='Get directory information and Heimdall flags')
parser.add_argument('-d', type=str, help='directory where beam files are located')
parser.add_argument('-name', type=str, help='directory where candidate files will be stored')
parser.add_argument('-dm_min', type=int, help='minimum DM')
parser.add_argument('-dm_max', type=int, help='maximum DM')
parser.add_argument('-parallel', type=int, help='enable parallel processing')

args = parser.parse_args()

source_directory = args.d
dest_directory = args.name
dm_min = args.dm_min
dm_max = args.dm_max
parallel = args.parallel
procs = []

time_start = time.clock()

def run_heimdall(input_file, output_directory, dm_min, dm_max, dm_tol=1.01, rfi_tolerance=3, boxcar_max=16):
    subprocess.call("heimdall -v -f " + input_file + " -output_dir " + output_directory + " -dm " + str(dm_min) + " " + str(dm_max) + " -dm_tol " + "1.01" + " -rfi_tol " + str(rfi_tolerance) + " -boxcar_max " + str(boxcar_max), shell = True)

def run_heimdall_on_directory(directory, folder_name):
    beams = os.listdir(directory)
    stored_in = os.getcwd() + "/" + folder_name + "_candidates"
    subprocess.call("mkdir " + stored_in, shell=True)
    if parallel:    
	for beam in beams:
           proc = multiprocessing.Process(target=run_heimdall, args=(directory + beam, stored_in, dm_min, dm_max))
           procs.append(proc)
           proc.start()
    	for proc in procs:
       	   proc.join()
    else:
	for beam in beams:
	   run_heimdall(directory + beam, stored_in, dm_min, dm_max)

if dest_directory is not None:
   run_heimdall_on_directory(source_directory, dest_directory)
   print("Total analysis time: " + time.clock()-time_start)
