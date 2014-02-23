/**
 *
 *
 *
 */

int ledDemarrage = 7;
int ledWarning = 6;
int ledLimiteAcceleration = 5;
int ledFrein = 4;
int speaker = 8;

void setup()
{
  pinMode(ledDemarrage, OUTPUT);
  pinMode(ledWarning,OUTPUT);
  pinMode(ledLimiteAcceleration,OUTPUT);
  pinMode(ledFrein,OUTPUT);
  
  /** allumage des LEDs pendant 2 secondes pour
   *  verifier leur fonctionnement
   */ 
  digitalWrite(ledDemarrage,HIGH);
  digitalWrite(ledWarning,HIGH);
  digitalWrite(ledLimiteAcceleration,HIGH);
  digitalWrite(ledFrein,HIGH);
  
  delay(2000);
  
  digitalWrite(ledDemarrage,LOW);
  digitalWrite(ledWarning,LOW);
  digitalWrite(ledLimiteAcceleration,LOW);
  digitalWrite(ledFrein,LOW);
  
  /** emet un son pour signifier que le systeme est
   *  operationnel
   */
  tone(speaker, 666, 1000);
}

void loop()
{
  
}
