/**
 * ooooooooooo  ooooo  oooooooooo ooooooooooo     o      oooooooooo  oooooooo8
 *  88 888  88   888   888    888 888            888      888   888 888
 *     888       888   888oooo88  888ooo8       8  88     888oooo88  888oooooo
 *     888       888   888        888          8oooo88    888               888
 *    o888o     o888o o888o      o888ooo8888 o88o  o888o o888o      o88oooo888
 */

int ledDemarrage = 7;
int ledWarning = 6;
int ledLimiteAcceleration = 5;
int ledFrein = 4;
int speaker = 8;
int incomingbyte = 0;

void setup()
{
  pinMode(ledDemarrage, OUTPUT);
  pinMode(ledWarning,OUTPUT);
  pinMode(ledLimiteAcceleration,OUTPUT);
  pinMode(ledFrein,OUTPUT);
  
  Serial.begin(9600); //On demarre la connexion serie
  while(!Serial){} // on attend que la connexion serie demarre
  
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
  if(Serial.available > 0) //si on recoit une donnee sur le port serie
  {
    incomingbyte = Serial.read();
  }
}
