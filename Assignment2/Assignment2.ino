//Sean Nishi
//Assignment 2 code

#define BUTTON D2
#define LED D1

bool buttonState;
bool clickedFlag = LOW;
bool light = LOW;

void setup() {
  //pin that has led is 01
  pinMode(LED, OUTPUT);
  //pin that has burron is 02
  pinMode(BUTTON, INPUT);
}

void loop() {
  //is the button pressed?
  buttonState = digitalRead(BUTTON);

  //if the button is clicked and it wasn't clicked previously
  if (buttonState and not clickedFlag){
    //set the clicked flag
    clickedFlag = HIGH;
  }
  //if the button is not clicked now and it was clicked previously (a completed
  //click has now happened)
  if (not buttonState and clickedFlag){
    //set clicked flag
    clickedFlag = LOW;

    //set the light
    if (light == LOW){
      digitalWrite(LED, HIGH);
      light = HIGH;
    }
    else if (light == HIGH){
      digitalWrite(LED, LOW);
      light = LOW;
    }
  }
}
