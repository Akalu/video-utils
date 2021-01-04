from __future__ import print_function
from pathlib import Path
import codecs
import argparse
import os
import sys
import subprocess

# method to run a command line
def execute(cmd):
    """
        Purpose  : executes a command and returns status
        Argument : cmd - command to execute
        Return   : exit_code
    """
    process = subprocess.Popen(cmd, shell=True)
    (result, error) = process.communicate()

    rc = process.wait()

    if rc != 0:
        print ("Error: failed to execute command")
    print ("process finished with code:", rc)
    return rc
# def

arg_parser = argparse.ArgumentParser()
arg_parser.version = '1.0'
arg_parser.add_argument('-tp', action='store', type=str, help='separated by comma list of transcoder parameters', required=True)
arg_parser.add_argument('-v', action='version')
arg_parser.add_argument('-i', action='store', type=str, help='path to input video file', required=True)
arg_parser.add_argument('-mask', action='store', type=str, help='path to masking png file', required=False)
arg_parser.add_argument('-o', action='store', type=str, help='path to transcoded video file', required=False)
args = arg_parser.parse_args()

print(vars(args))


# check the input files
inputf = args.i
if not os.path.isfile(inputf):
    print("Input video file {} does not exist".format(inputf))
    sys.exit()

maskf = args.mask
if maskf is not None:
    maskf = "mask.png"
if not os.path.isfile(maskf):
    print("Mask png file {} does not exist".format(maskf))
    sys.exit()

outputf = Path(inputf).stem + ".trans.mp4"
# If there is an option for output file
if args.o is not None:
    outputf = args.o

params = [s.strip() for s in args.tp.split(',')] 

paramMap = {}
for param in params:
    parts = [s.strip() for s in param.split('=')]
    paramMap[parts[0]]=parts[1]


# validate input
if paramMap.get('res') is None:
    print("input resolution in format w:h is not set")
    sys.exit()

# extract params
inputRes = [s.strip() for s in paramMap['res'].split(':')]
iw = int(inputRes[0])
ih = int(inputRes[1])
sw = int(iw)
sh = int(ih)
if paramMap.get('scale') is not None:
   scaleRes = [s.strip() for s in paramMap['scale'].split(':')]
   sw = int(scaleRes[0])
   sh = int(scaleRes[1])

offsetOrig = int((iw - ih) / 2)
offsetScaled = int((sw - sh) / 2)

filter0 = "[0:v]split [a][b];"
filter1 = "[a]transpose=1,crop={}:{}:0:{},scale={}:{},setdar={}/{}[crop];".format(ih, ih, offsetOrig, ih, ih, ih, ih)
filter2 = "[b]transpose=1,crop={}:{}:0:{},scale={}:{},setdar=16/9,avgblur=54[back];".format(ih, ih, offsetOrig, sw, sh)
filter3 = "[1:v]alphaextract [mask];"
filter4 = "[crop][mask]alphamerge [masked];"
filter5 = "[back][masked]overlay={}:0".format(offsetScaled)

filter = filter0 + filter1 + filter2 + filter3 + filter4 + filter5


command = "ffmpeg -i {} -loop 1 -i {} -filter_complex \"{}\" {}".format(inputf, maskf, filter, outputf) 

result = execute(command)
