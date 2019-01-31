# Installation guide for this program. Mainly targetting the Raspberry Pi board.

### Dependencies
For the main program:
- imutils

For the alert system:
- eSpeak


### Installation
For the main program:
- imutils

For the alert system:
- Install eSpeak with the package manager
	- sudo apt-get install espeak
- 



### Tests
For the alert system:
- Test if the audio is working via the 3.5mm output
	- aplay /usr/share/sounds/alsa/*
- Test the Text To Speech synthesizer eSpeak after the installation
	- espeak "Hello World" 2>/dev/null


#### References
- [eSpeak installation and usage guide](https://www.dexterindustries.com/howto/make-your-raspberry-pi-speak/)