/**
 * ooooooooooo  ooooo  oooooooooo ooooooooooo     o      oooooooooo  oooooooo8
 *  88 888  88   888   888    888 888            888      888   888 888
 *     888       888   888oooo88  888ooo8       8  88     888oooo88  888oooooo
 *     888       888   888        888          8oooo88    888               888
 *    o888o     o888o o888o      o888ooo8888 o88o  o888o o888o      o88oooo888
 */

int pinEngine = 7;
int pinWarning = 6;
int pinAccelerationLimit = 5;
int pinBrake = 4;
int pinSound = 8;

boolean engine = false;
boolean warning = false;
boolean accelerationLimit = false;
boolean brake = false;
boolean sound = false;

char command = 0;

void Engine()
{
  if(!engine)
    digitalWrite(pinEngine, HIGH);
  else
    digitalWrite(pinEngine, LOW);
  engine = !engine;
}

void Warning()
{
  if(!warning)
    digitalWrite(pinWarning, HIGH);
  else
    digitalWrite(pinWarning, LOW);
  warning = !warning;
}

void AccelerationLimit()
{
  if(!accelerationLimit)
    digitalWrite(pinAccelerationLimit, HIGH);
  else
    digitalWrite(pinAccelerationLimit, LOW);
  accelerationLimit = !accelerationLimit;
}

void Brake()
{
  if(!brake)
    digitalWrite(pinBrake, HIGH);
  else
    digitalWrite(pinBrake, LOW);
  brake = !brake;
}

void Sound()
{
  if(!sound)
    tone(pinSound, 666);
  else
    noTone(pinSound);
  sound = !sound;
}

void setup()
{
  pinMode(pinEngine, OUTPUT);
  pinMode(pinWarning,OUTPUT);
  pinMode(pinAccelerationLimit,OUTPUT);
  pinMode(pinBrake,OUTPUT);
  
  Serial.begin(9600); //On demarre la connexion serie
  while(!Serial){} // on attend que la connexion serie demarre
  
  /** 
   *  verification du fonctionnement des systemes
   *  (1/2 seconde)
   */ 
  Engine();
  Warning();
  AccelerationLimit();
  Brake();
  Sound();
  
  delay(500);
  
  Engine();
  Warning();
  AccelerationLimit();
  Brake();
  Sound();
}

void loop()
{
  if(Serial.available() > 0) //si on recoit une donnee sur le port serie
  {
    command = Serial.read();
    switch(command)
    {
      case 'e':
        Engine();
      break;
      case 'w':
        Warning();
      break;
      case 'b':
        Brake();
      break;
      case 'a':
        AccelerationLimit();
      break;
      case 's':
        Sound();
      break;
    }
  }
}
