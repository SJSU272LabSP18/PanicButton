# cmpe272-spring18

## Panic button

A device with panic button, speaker and camera. Basically, the device connect to your mobile phone via bluetooth. When pushing the button once, the device sends a bluetooth signal to the mobile phone. After receiving the signal the mobile phone application will inform our location to other people such as family and friends. Pushing it twice the speaker will start to operate to inform people around you that you are in danger and also the camera will capture the places around and automatically send the photos to your family and friends.


## Motion sensing for library booking system

Adding Motion sensing to the current library booking system: The current library booking system limits booking the discussion rooms to 1 booking per day per id. This limitation was implemented because earlier people used to book the rooms for hours together and not use them. Adding a device which could detect if the room is currently occupied or not will make the availability chart real time. Users then see the live availability and book the rooms for use. If the users fail to occupy the booked room in a window of x minutes the booking is automatically cancelled and room is released back into the pool of available rooms.

## Text Book Sharing App

We can create web app for this. Landing screen can be simple with search button to search books by name and by author.
On clicking search we can show google map with pins of books in certain radius. If all copies of books are in use we can ask user to allow sending push notifications whenever book is available. There will be two more screens showing current books of users that are borrowed by someone and to add new books that user wants to share. Backend can be on Bluemix. Technologies we get to use

* Mobile development
* Cloud 
* Google Maps integration(for nearby-books feature)
* Push notifications (GCM) 
* Users can also add featured contents like previous years papers (of CMPE272 etc) and notes. If we have bandwidth we can integrate braintree / stripe API for payments. Idea is deceptively simple as a lot of work will go in implementation, it depends on us how we define its scope.

