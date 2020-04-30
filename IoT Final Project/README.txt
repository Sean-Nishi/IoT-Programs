Sean Nishi's final IoT Project

base code done by me, files in streaming folder are modified from miguel grinberg's blog
Don't want to plagerize!

Tried to have one program that does everything but was too much of a strain for the pi4...

What AlwaysWatching.py does:

recording video in real time
when an unrecognized face is detected, will save frame
will not save image/frame if known person is detected
highlights all faces on current frame

pictures are saved in pics dir
output.mp4 is saved recording at increased fps

to view feed from browser, go into streaming dir and run 'python app.py'
