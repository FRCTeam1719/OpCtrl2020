#include <Joystick.h>

Joystick_ Joystick(0x03, JOYSTICK_TYPE_JOYSTICK, //ID of HID device, type of joystick,
                   6, 0, //Button count, Hat switch count,
                   false, false, true, //has X axis, has Y axis, has Z axis,
                   false, false, false, // has rotational X axis, has rotational Y axis, has rotational Z axis,
                   false, false, //has rudder, has throttle,
                   false, false, false); //hass accelerator, has break, has steering.

const int buttonCount = 6;

void setup() {
  // READING
  Serial.begin(9600);
//  Serial.setTimeout(2147483647);

  // Buttons
//  pinMode(0, INPUT_PULLUP);
//  pinMode(2, INPUT_PULLUP);
//  pinMode(4, INPUT_PULLUP);
//  pinMode(6, INPUT_PULLUP);
//  pinMode(8, INPUT_PULLUP);
//  pinMode(10, INPUT_PULLUP);

  for (int i=0; i<buttonCount; i++) {
    pinMode(i*2+1, INPUT_PULLUP); // Set button
    pinMode(i*2, OUTPUT); // Set LED
  }

  Joystick.begin(false);
  Joystick.setZAxisRange(0, 680);
}

char deviceId;
char deviceValue;

void doSerial() {
  deviceId = Serial.read();
  deviceValue = Serial.read();

  // dev 1, val 1
  //ÿ dev 1, val 255

  if (deviceId == 0x00) {
    Serial.write(buttonCount);
    return;
  }

  digitalWrite((deviceId-1)*2+1, deviceValue > 128 ? HIGH : LOW);
}

void loop() {
  if (Serial.available()) {
    doSerial();
  }

  for (int i=0; i<=buttonCount; i++)
    Joystick.setButton(i, digitalRead(i*2));

//  Serial.println(analogRead(A1));
  //Joystick.setZAxis(analogRead(A1));
   
  Joystick.sendState();
}
