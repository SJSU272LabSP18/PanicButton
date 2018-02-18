# cmpe272-spring18


## IoT idea: Cheap ForgetMeNot LCD screen with face recognition

Basically a device hangs on your front door or garage. Whenever you are closeby the camera recognizes your face and yells at you don’t forget to bring the key.

Personally I have many times forgotten to bring keys/phone/wallet/trash bag/misc. Stuff when leaving home. And sometimes I have to drive all the way back to grab it.

* Why create this when we have a reminder app on our phones:
This is for a niche scenario where you enters/leaves your home.
You don’t need to do anything to see the reminder, which is important because you might as well forget to bring your phone

* Why it’s better than a piece of sticky note:
It’s bigger and it changes brightness/color when you approaches, which brings up your awareness, for sticky note you will just as well ignore it like anything else around your door entrance.
You can update through your phone, so that you don’t need to walk downstairs to write with a sharpie.
It supports multiple person and looks cool!


## Text Book Sharing App

We can create web app for this. Landing screen can be simple with search button to search books by name and by author.
On clicking search we can show google map with pins of books in certain radius. If all copies of books are in use we can ask user to allow sending push notifications whenever book is available. There will be two more screens showing current books of users that are borrowed by someone and to add new books that user wants to share. Backend can be on Bluemix. Technologies we get to use

* Mobile development
* Cloud 
* Google Maps integration(for nearby-books feature)
* Push notifications (GCM) 
* Users can also add featured contents like previous years papers (of CMPE272 etc) and notes. If we have bandwidth we can integrate braintree / stripe API for payments. Idea is deceptively simple as a lot of work will go in implementation, it depends on us how we define its scope.


## Motion sensing for library booking system

Adding Motion sensing to the current library booking system: The current library booking system limits booking the discussion rooms to 1 booking per day per id. This limitation was implemented because earlier people used to book the rooms for hours together and not use them. Adding a device which could detect if the room is currently occupied or not will make the availability chart real time. Users then see the live availability and book the rooms for use. If the users fail to occupy the booked room in a window of x minutes the booking is automatically cancelled and room is released back into the pool of available rooms.


## Blockchain for classifieds

Applying blockchain to local classifieds and enable trusted transactions: The current classifieds system is vulnerable to a lot of frauds 



## Panic button

A device with panic button, speaker and camera. Basically, the device connect to your mobile phone via bluetooth. When pushing the button once, the device sends a bluetooth signal to the mobile phone. After receiving the signal the mobile phone application will inform our location to other people such as family and friends. Pushing it twice the speaker will start to operate to inform people around you that you are in danger and also the camera will capture the places around and automatically send the photos to your family and friends.


## Opinion Mining with Node-RED
