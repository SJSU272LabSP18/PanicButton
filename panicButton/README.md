# cmpe272-spring18

## Team Name: We Fly High

## Student Names
Haoji Liu
Nrupa Chitley
Rachit Choksni
Watcharit Maharu Tainont

## Panic button

A portable panic button with phone app.

### When press once:
* notifies your friend(s) via text of a preset text message. location share once.

### When press twice:
* starts alarming, text friends with a different preset message, continue location sharing

### When press three or more times and hold for longer than 2 seconds:
* dials 911 on the phone, start real time location share with friend(s).

Tech stack:
* a small pcb board
* button
* speaker
* bluetooth/wifi
* android phone app
* ...

### Deliverable
*  a portable button device that's connected to phone with bluetooth or wifi
*  a phone app that does location streaming, text/phone, and user data customization. 

## Discarded ideas:

### Motion sensing for library booking system

Adding Motion sensing to the current library booking system for real time monitoring

If the users fail to occupy the booked room in a window of x minutes the booking is automatically cancelled and room is released back into the pool of available rooms.

The current library booking system limits booking the discussion rooms to 1 booking per day per id. This limitation was implemented because earlier people used to book the rooms for hours together and not use them. Adding a device which could detect if the room is currently occupied or not will make the availability chart real time. Users then see the live availability and book the rooms for use.

### Text Book Sharing App

Web app to share textbooks based on geographic locations

We can create web app for this. Landing screen can be simple with search button to search books by name and by author.
On clicking search we can show google map with pins of books in certain radius. If all copies of books are in use we can ask user to allow sending push notifications whenever book is available. There will be two more screens showing current books of users that are borrowed by someone and to add new books that user wants to share. Backend can be on Bluemix. Technologies we get to use

* Mobile development
* Cloud 
* Google Maps integration(for nearby-books feature)
* Push notifications (GCM) 
* Users can also add featured contents like sharing notes. If we have bandwidth we can integrate braintree / stripe API for payments. Idea is deceptively simple as a lot of work will go in implementation, it depends on us how we define its scope.

