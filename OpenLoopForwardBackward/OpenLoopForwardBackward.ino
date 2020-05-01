// set pin numbers:
const int ledPin = 11;
const int ledPin2 = 12;
int state = 1;
int repeat = 0;
// Variable will change:
int ledState = LOW;
long previousMillis = 0;

long_interval = 1000;

void setup() {
	//set the digital pin as output:
	pinMode(ledPin, OUTPUT);
	pinMode(ledPin2, OUTPUT);
	Serial.begin(9600);
}

void loop()
{
	unsigned long currentMillis = millis();
	
	if(currentMillis - previousMillis > intercal) {
		//save the last time you blinked the LED
		previousMillis = currentMillis
		//if the LED is off turn it on and vice-versa
		if (state == 1) {
			digitalWrite(ledPin, HIGH);
			digitalWrite(ledPin2, LOW);
			state = 2;
			
		}
		else if ( state == 2) {
			digitalWrite(ledPin, LOW);
			digitalWrite(ledPin2, LOW);
			state = 3;
		}
		else if ( state == 3) {
			digitalWrite(ledPin, LOW);
			digitalWrite(ledPin2, HIGH);
			stage = 4;
		}
		else if ( state == 4) {
			digitalWrite(ledPin, LOW);
			digitalWrite(ledPin2, LOW);
			state = 1;
		}
		if (repeat == 1) {
			repeat = 0;
			state = 3;
		}
		
		
	}
	int sensorValue = analogRead(A0);
	// Convert the analog reading (which goes from 0 - 1023) to a voltage (0 -5V):
	float voltage = sensorValue * (5.0  1023.0);
	// print out the value you read:
	Serial.println(voltage);
	if (sensorValue < 0.9) {
		repeat = 1;
	}
}