// Weareable Panic button
// Author: Haoji Liu
//
// Press:
// 1: considered a flute, do nothing
// 2: text one friend about the location
// 3: text multiple friends about the location, start blinking LEDs
// 4: streaming multiple friends about the location, starts the alarm
// 5: do nothing
// 6: call 911
// press for >5 seconds will reset everything
//
// I'm picturing this to be a Weareable where it will be sewed into a hoodie, and
// the LED strip will be sewed onto the hoodie as well.
// We are selling a tech hoodie instead of this device itself.

#include <SimbleeBLE.h>
// the pin that the pushbutton is attached to
// this overlaps with Button B on the RGB shield
// this is intentional for testing only, we are just
// going to not use that button for now
const int buttonPin = 5;
const int buzzerPin = 6; // the pin that links to the alarm
int ledGreen = 3;
int ledRed = 2;
int ledBlue = 4;

const int CONST_TEXT_SINGLE = 1;  // text one friend
const int CONST_TEXT_MULT = 2;  // text all friends in the list
const int CONST_PHONE_911 = 3;  // call 911

////////////////////////////////
int buttonPushCounter = 0;   // counter for the number of button presses
int buttonState = 0;         // current state of the button
int lastButtonState = 0;     // previous state of the button
unsigned long currentTime;
unsigned long lastPressedTime;
unsigned long buttonPressedFor;

int MAX_CLICK_INTERVAL = 1000;  // defines how fast for mutiple clicks to work as expected
int RESET_INTERVAL = 5000;  // defines how long to hold for reset
int LOCATION_STREAMING_INTERVAL = 30000; // location streaming every 30 sec
int LED_BLINK_INTERVAL = 500; // LED blink every .5 sec


// to control BLE
int bleSwitch = 1; // this is also used by Serial, so if connected to USB then we lose bleSwitch
int BLE_START_INTERVAL = 3000;  // defines how long to hold to start the device
bool isBleStarted = false;


// to control the location streaming
bool isLocationStreaming = false;
unsigned long lastLocationSentAt;

// to control the LED blink
bool shouldLedBlink = false;
bool isLedOn = false;
unsigned long lastLedUpdatedAt;

void setup() {
  // init vars
  lastPressedTime = 0;
  lastLocationSentAt = 0;
  // initialize the button pin as a input:
  pinMode(ledGreen, OUTPUT);
  pinMode(ledRed, OUTPUT);
  pinMode(ledBlue, OUTPUT);
  pinMode(buzzerPin,OUTPUT);//initialize the buzzer pin as an output
  pinMode(buttonPin, INPUT);
  digitalWrite(buzzerPin,LOW);
  digitalWrite(ledGreen,LOW);
  digitalWrite(ledRed,LOW);
  digitalWrite(ledBlue,LOW);

  // initialize serial communication:
  Serial.begin(9600);


  // The BLE part
  SimbleeBLE.advertisementData = "cmpe272hahaha";
  //SimbleeBLE.advertisementInterval = 500;
  //SimbleeBLE.iBeacon = true;  // TODO: should we do this???
  SimbleeBLE.deviceName = "cmpe272";
}

void sendIntToPhone(int myInt) {
  Serial.println("Sending an integer to phone!");
//  SimbleeBLE.sendInt(myInt); //Sends myByte
  SimbleeBLE.send('3'); //Sends myByte
}

void sendLocationSingle() {
  sendIntToPhone(CONST_TEXT_SINGLE);
  lastLocationSentAt = millis();
  Serial.println("Send text with location to one contact");
}

void sendLocationMult() {
  Serial.println("Send text with location to multiple contacts");
  sendIntToPhone(CONST_TEXT_MULT);
  lastLocationSentAt = millis();

}

void callNineOneOne() {
  sendIntToPhone(CONST_PHONE_911);
  Serial.println("Call 911");
}

void resetAll() {
  Serial.println("Hold for more than 5 sec, reset everything...");
  // Reset everything
  buttonPushCounter = 0;
  buttonState = 0;
  lastButtonState = 0;
  isLocationStreaming = false;
  shouldLedBlink = false;
  isLedOn = false;
  digitalWrite(buzzerPin,LOW);
  digitalWrite(ledGreen,LOW);
  digitalWrite(ledRed,LOW);
  digitalWrite(ledBlue,LOW);
  // turn off BLE stack
  SimbleeBLE.end();
  isBleStarted = false;
}

void startAlarm() {
  digitalWrite(buzzerPin,HIGH);
  Serial.println("Start the alarm");
}

void toggleLed(bool on) {
  // TODO: we are going to use our own LED strip instead of the built-in
  // LED on the button shield.
  if (on) {
//    Serial.println("Turn LED on!");
    digitalWrite(ledGreen,HIGH);
    digitalWrite(ledRed,HIGH);
    digitalWrite(ledBlue,HIGH);
  } else {
//    Serial.println("Turn LED off!");
    digitalWrite(ledGreen,LOW);
    digitalWrite(ledRed,LOW);
    digitalWrite(ledBlue,LOW);
  }
  lastLedUpdatedAt = millis();
}

void ongoingEventsCheck() {
  // check for location streaming
  if (isLocationStreaming == true && lastLocationSentAt != 0 && (currentTime - lastLocationSentAt) > LOCATION_STREAMING_INTERVAL) {
    sendLocationMult();
  }
  // check for LED light blinking
  if (shouldLedBlink == true && lastLedUpdatedAt != 0 && (currentTime - lastLedUpdatedAt) > LED_BLINK_INTERVAL) {
    toggleLed(!isLedOn);
    isLedOn = !isLedOn;
  }
}

void SimbleeBLE_onAdvertisement(bool start)
{
  // turn the green led on if we start advertisement, and turn it
  // off if we stop advertisement
  if (start) {
    Serial.println("Simblee starts advertising...");  
    digitalWrite(ledGreen, HIGH);
  } else {
    Serial.println("Simblee stops advertising...");  
    digitalWrite(ledGreen, LOW);
  }
}

void SimbleeBLE_onConnect()
{
  // what should we do here?
  Serial.println("Simblee connected!!!");
}

void SimbleeBLE_onDisconnect()
{
  // what should we do here?
  Serial.println("Simblee disconnected!!!");

}

void SimbleeBLE_onReceive(char *data, int len)
{
//  // if the first byte is 0x01 / on / true
//  if (data[0]) {
//    digitalWrite(ledRed, HIGH);
//  }
//  else {
//    digitalWrite(ledRed, LOW);
//  }
}

void onButtonClick(int buttonPushCounter) {
  Serial.print("number of button pushes: ");
  Serial.println(buttonPushCounter);

  if (!isBleStarted) {
    // do nothing if ble is off
    Serial.println("ble is off, do nothing...");
    return;
  }

  if (buttonPushCounter == 1) {
    Serial.println("Did you press it by acciddent..");
  } else if (buttonPushCounter == 2) {
    // send the location ONCE!
    sendLocationSingle();
  } else if (buttonPushCounter == 3) {
    sendLocationMult();
    // let the led blink
    shouldLedBlink = true;
    Serial.print("Blinking LED");
    toggleLed(true);
  } else if (buttonPushCounter == 4) {
    startAlarm();
    isLocationStreaming = true;
  } else if (buttonPushCounter == 5) {
    // 5 clicks don't do nothing, this is intentional,
    // to avoid unwanted calls to 911
  } else if (buttonPushCounter == 6) {
    // call 911
    callNineOneOne();
  } else {
    // ??
  }
}

void loop() {
  // read the pushbutton input pin:
  buttonState = digitalRead(buttonPin);
  currentTime = millis();
  ongoingEventsCheck();

  // compare the buttonState to its previous state
  if (buttonState != lastButtonState) {
    // pressed!
    if (buttonState == HIGH) {
      buttonPressedFor = currentTime;
      // first time click
      if (lastPressedTime == 0) {
        lastPressedTime = currentTime;
      }

      if (buttonPushCounter == 0 || (buttonPushCounter > 0 && (currentTime - lastPressedTime) > MAX_CLICK_INTERVAL)) {
        buttonPushCounter = 1;
      } else {
        buttonPushCounter++;
      }
      // update the last pressed time
      lastPressedTime = currentTime;
      onButtonClick(buttonPushCounter);
    } else {
      // if the current state is LOW then the button went from on to off:
      Serial.println("button released");
    }
    // Debounce time for the button
    delay(100);
  } else {
      // button state is the same as last round, and still pressed
      if (buttonState == HIGH) {
        if (!isBleStarted && (currentTime - buttonPressedFor) > BLE_START_INTERVAL) {
          Serial.println("ble going to start...");
          isBleStarted = true;
          // start the BLE stack
          SimbleeBLE.begin();
        } else if ((currentTime - buttonPressedFor) > RESET_INTERVAL) {
          resetAll();
        }
      }

  }
  // save the current state as the last state, for next time through the loop
  lastButtonState = buttonState;

}
