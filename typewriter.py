"""
	Prereqs: 
		Linux system with dev/input/event access (may require sudo)
		Determine which event number corresponds with your keyboard
			- ` ls -l /dev/input/by-path/ `
			- Determine which symbolic link file resembles your 
				keyboard and the corresponding event number
			-
			
		pygame installed for that system/user executing the script
	
	WARNING:
		the code below can be slightly modified to act as a keylogger
		and even without code modification, it's possible for someone
		to determine which characters were pressed based on the time
		gaps between keypress sounds. Use at your own risk and I am
		not responsible if you misuse this script and any information 
		you leak with this. Python files should rarely if ever be 
		executed with broad sudo permissions.
		
	
	Directions:
		in the directory the file is located, execute the script with 
		the wav files in the same directory and with a system argument
		of the event number this script should subscribe to (keyboard
		event handler)
		
		` python typewriter.py <event number>`
		ex. ` python typewriter.py 4`


"""


import os
import struct
import sys
import pygame



def is_desired_audio_file(f):
	return os.path.isfile(os.path.join(f)) and f.endswith(".wav")

def get_audio_files():
	return [f for f in os.listdir() if is_desired_audio_file(f)]
	
	
if __name__ == '__main__':
	pygame.mixer.init()
	cwd = os.getcwd()
	audio_filenames = get_audio_files()
	print("audio files: " , audio_filenames)

	keystrokes = [pygame.mixer.Sound(f) for f in audio_filenames]
	sound_index = 0
	infile_path = "/dev/input/event" + (sys.argv[1] if len(sys.argv) > 1 else "0")

	FORMAT = "llHHI"

	event_size = struct.calcsize(FORMAT)

	with open(infile_path, "rb") as in_file:
		event = in_file.read(event_size)
		while event:
			(tv_sec, tv_usec, keytype, _, value) = struct.unpack(FORMAT, event) # scrubs which key was
			# (tv_sec, tv_usec, keytype, code, value) = struct.unpack(FORMAT, event) # (doesn't scrub which key was pressed)
			if keytype != 0:
				#print("Event type:  {}, code: {}, value: {}, time: {}".format(keytype, code, value, tv_sec))
				if value == 1:
					assert sound_index >= 0 and sound_index < len(keystrokes)
					keystrokes[sound_index].play()
					sound_index = (sound_index + 1) % len(keystrokes)
				

			event = in_file.read(event_size)
		
