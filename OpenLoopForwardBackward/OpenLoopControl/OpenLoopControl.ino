// set pin numbers:
const int ledPin = 2;
const int ledPin2 = 3;
int state = 2;
int repeat = 0;
// Variable will change:
int ledState = LOW;
long previousMillis = 0;
byte incomingByte;

long interval = 1000;

void setup() {
  //set the digital pin as output:
  pinMode(ledPin, OUTPUT);
  pinMode(ledPin2, OUTPUT);
  Serial.begin(9600);
}

void loop()
{
  unsigned long currentMillis = millis();
  
  if(currentMillis - previousMillis > interval) {
    //save the last time you blinked the LED
    previousMillis = currentMillis;
    //if the LED is off turn it on and vice-versa
    if (state == 1) {
      digitalWrite(ledPin, HIGH);
      digitalWrite(ledPin2, LOW);
      //state = 2;
      
    }
    else if ( state == 2) {
      digitalWrite(ledPin, LOW);
      digitalWrite(ledPin2, LOW);
      //state = 3;
    }
    else if ( state == 3) {
      digitalWrite(ledPin, LOW);
      digitalWrite(ledPin2, HIGH);
      //state = 4;
    }
    else if ( state == 4) {
      digitalWrite(ledPin, LOW);
      digitalWrite(ledPin2, LOW);
      //state = 1;
    }
    else {
      digitalWrite(ledPin, LOW);
      digitalWrite(ledPin2, LOW);
      //state = 1;
    }

    if (Serial.available() > 0) {
    incomingByte = Serial.read(); // read the incoming byte:
    Serial.print(" I received:");
    Serial.println(incomingByte);
    state = incomingByte - 48;
  }
    
    
  }

}
