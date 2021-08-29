About
======

This is a collection of different utils/scripts written in different languages, mostly for stream data processing (videos and image sequencies).

All scripts are written in Python 3.9.1 (https://www.python.org/downloads/release/python-391/) and Bash, and in some cases require ffmpeg video utils installed (https://ffmpeg.org/download.html).

 
Overview
=========

## transcoder

transcoder.py - a utility for conversion of video shot in portrait mode into landscape one, with auto-cropping and background blurring

Quite often video is recorded in portrait mode (especially this is true for mobile devices).
transcoder allows to convert such video archives into ones convenient for viewing on normal 16:9 monitors.

The using of this utility is quite straightforward. 
For example, lets assuming the original video is shot in HD resolution in portrait mode, then the following command will transcode this video into landscape mode, cropping the central frame with size 1080x1080 and putting it into 1920x1080 frame, blurring the background:

python transcode.py -i orig.mp4 -mask mask.png -tp res=1920:1080,scale=1920:1080

transcoder/mask.png is a masking frame, representing the background of the central frame of future video and must be prepared for specific resolution (in this case it is 1080x1080). Note that this picture must be saved in png format with preserved alpha channel. I prepared one as an example.

The picture transcoder/london.mp4_snapshot_00.01.jpg demonstrates the snapshot from the final video.
