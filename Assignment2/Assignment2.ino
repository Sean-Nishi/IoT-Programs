//Sean Nishi
//Assignment 2 code

#define BUTTON D2
#define LED D1

bool buttonState;
bool led = LOW;
bool changed = LOW;

void setup() {
  //pin that has led is 01
  pinMode(LED, OUTPUT);
  //pin that has burron is 02
  pinMode(BUTTON, INPUT);
}

void loop() {
  //is the button pressed?
  buttonState = digitalRead(BUTTON);
  
  if (buttonState == LOW){
    changed = LOW;
  }

   if (changed == LOW) {

    //if the button is pressed and the light is off,
    //turn light on and save its state
    if (buttonState == HIGH && led == LOW){
      digitalWrite(LED, HIGH);
      led = HIGH;
      changed = HIGH;
    }
    //if the button is pressed and the light is on,
    //turn the light off and save its state
    else if (buttonState == HIGH && led == HIGH){
      digitalWrite(LED, LOW);
      led = LOW;
      changed = HIGH;
    }
   }
}
