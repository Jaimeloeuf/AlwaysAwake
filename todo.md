Optimization notes

- Use different processes
- See how to stop the video streaming bottle neck
- See if not rescaling the frame would be faster
- See if removing the shape drawing it would be faster
- Changing the ML algorithm to a faster one
- Only use the nearest "subject"'s eyes and discard the rest
- Remove the text writings on the screen and use a buzzer/LED on the GPIO instead
- In the headless version, stop displaying/drawing the frame captured out onto the screen and save GPU usage
	by just ouputting alerts through the GPIO
- Remove the key that stops the loop to check if user pressed q.

- Last resort is to rewrite this in another language
- Remove unneeded modules in the kernel / stopping unneeded services/apps running in the background





Create a new Docker image to run this program and edit the program by mounting the volume using Docker Compose
Learn how to modify the kernel, or how to not use Raspbian
Find a OS for raspberry pi that is super stripped down, or learn how to do it.

See if I can even use p5.JS for the img recog??



Start building a strip down version of this code with the purpose of running this program in a headless setting.
Create the soluton architect on how this will work and everything.
Design out what are the btns for:

Btns:
- Search face:
	- The "start" button that will search for the face in the frame, the moment the face is detected for more
		that 3 seconds or so, notify user to stop moving the camera and let it be
- Stop btn
	- to stop the app from running alr.
	- Send out a notif to the backend system.


The backend system should be built using Elixir
How should communication be done with the backend service>?

Comms should be
	- reliable!
	- Fast
	- fault tolerant, with specific message reciecived acknowledgement process.
	- The connection should not be a always connected one as that will drain batt??
		- Is battery a concern in this case?
		- Search up how does car and bus batteries work. Does the engine recharge it or?
	

	gRPC
		Does this need to maintain a always on connection
	WebHooks
		In this case, the app will act as the "server" and the server acts as the client waiting for new remote calls
	RESTful
		Is this too verbose?
	Message based protocols
		MQTT
		AMQP
		Kafka?
	
	How will the sim card module work? WIll it be ok? Can we use the wifi in the bus??