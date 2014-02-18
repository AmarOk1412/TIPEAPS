#include "tones.h"

int ledDemarrage = 7;
int ledWarning = 6;
int ledLimiteAcceleration = 5;
int ledFrein = 4;
int speaker = 8;

void sevenNationArmy()
{
  int melody[]={NOTE_E4, NOTE_E4, NOTE_G4, NOTE_E4, NOTE_D4, NOTE_C4, NOTE_B3, /**/ NOTE_E4, NOTE_E4, NOTE_G4, NOTE_E4, NOTE_D4, NOTE_C4, NOTE_D4, NOTE_C4, NOTE_B3};
  float duration[]={1.5,0.5,0.6,0.6,0.6,2,2, /**/ 1.5,0.5,0.6,0.6,0.6,0.6,0.6,0.6,2};
  
  for(int note = 0; note < 16; note++)
  {
    int noteDuration = (60000/120) * duration[note];
    tone(speaker,melody[note],noteDuration);
    int pause = noteDuration * 1.2;
    delay(pause);
    
    noTone(speaker);
  }
}

void setup()
{
  pinMode(ledDemarrage, OUTPUT);
  pinMode(ledWarning,OUTPUT);
  pinMode(ledLimiteAcceleration,OUTPUT);
  pinMode(ledFrein,OUTPUT);
  
  digitalWrite(ledDemarrage,HIGH);
  digitalWrite(ledWarning,HIGH);
  digitalWrite(ledLimiteAcceleration,HIGH);
  digitalWrite(ledFrein,HIGH);
  
  delay(2000);
  
  digitalWrite(ledDemarrage,LOW);
  digitalWrite(ledWarning,LOW);
  digitalWrite(ledLimiteAcceleration,LOW);
  digitalWrite(ledFrein,LOW);
  
  sevenNationArmy();
}

void loop()
{
  
}
