
/*NOT DONE DON'T TOUCH YET*/

// Pin definitions
#define linesensor 1
#define MOTORL 3
#define MOTORR 2


void setup() {
  // put your setup code here, to run once:
  pinMode(LINESENSOR, INPUT);
  pinMode(MOTORL,OUTPUT);
  pinMode(MOTORR,OUTPUT);
}

void loop() {
 
}

//-------SENSOR READING CODE----------
void readLFMSensors()
{
  LFMSensor[0] = digitalRead(LFMSensor0);
  LFMSensor[1] = digitalRead(LFMSensor1);
  LFMSensor[2] = digitalRead(LFMSensor2);
  LFMSensor[3] = digitalRead(LFMSensor3);
  LFMSensor[4] = digitalRead(LFMSensor4);
  LFMSensor[5] = digitalRead(LFMSensor5);
  LFMSensor[6] = digitalRead(LFMSensor6);
  LFMSensor[7] = digitalRead(LFMSensor7);
  
  if((   ((LFMSensor[0]== 0 )&&(LFMSensor[1]== 0 )&&(LFMSensor[2]== 0 )&&(LFMSensor[3]== 0 )&&(LFMSensor[4]== 0 )&&(LFMSensor[5]== 0 )&&(LFMSensor[6]== 0 )&&(LFMSensor[7]== 1 ))  {mode = FOLLOWING_LINE; error = 7;}
  else if((LFMSensor[0]== 0 )&&(LFMSensor[1]== 0 )&&(LFMSensor[2]== 0 )&&(LFMSensor[3]== 0 )&&(LFMSensor[4]== 0 )&&(LFMSensor[5]== 0 )&&(LFMSensor[6]== 1 )&&(LFMSensor[7]== 1 ))  {mode = FOLLOWING_LINE; error = 6;}
  else if((LFMSensor[0]== 0 )&&(LFMSensor[1]== 0 )&&(LFMSensor[2]== 0 )&&(LFMSensor[3]== 0 )&&(LFMSensor[4]== 0 )&&(LFMSensor[5]== 0 )&&(LFMSensor[6]== 1 )&&(LFMSensor[7]== 0 ))  {mode = FOLLOWING_LINE; error = 5;}
  else if((LFMSensor[0]== 0 )&&(LFMSensor[1]== 0 )&&(LFMSensor[2]== 0 )&&(LFMSensor[3]== 0 )&&(LFMSensor[4]== 0 )&&(LFMSensor[5]== 1 )&&(LFMSensor[6]== 1 )&&(LFMSensor[7]== 0 ))  {mode = FOLLOWING_LINE; error = 4;}
  else if((LFMSensor[0]== 0 )&&(LFMSensor[1]== 0 )&&(LFMSensor[2]== 0 )&&(LFMSensor[3]== 0 )&&(LFMSensor[4]== 0 )&&(LFMSensor[5]== 1 )&&(LFMSensor[6]== 0 )&&(LFMSensor[7]== 0 ))  {mode = FOLLOWING_LINE; error = 3;}
  else if((LFMSensor[0]== 0 )&&(LFMSensor[1]== 0 )&&(LFMSensor[2]== 0 )&&(LFMSensor[3]== 0 )&&(LFMSensor[4]== 1 )&&(LFMSensor[5]== 1 )&&(LFMSensor[6]== 0 )&&(LFMSensor[7]== 0 ))  {mode = FOLLOWING_LINE; error = 2;}
  else if((LFMSensor[0]== 0 )&&(LFMSensor[1]== 0 )&&(LFMSensor[2]== 0 )&&(LFMSensor[3]== 0 )&&(LFMSensor[4]== 1 )&&(LFMSensor[5]== 0 )&&(LFMSensor[6]== 0 )&&(LFMSensor[7]== 0 ))  {mode = FOLLOWING_LINE; error = 1;}
  else if((LFMSensor[0]== 0 )&&(LFMSensor[1]== 0 )&&(LFMSensor[2]== 0 )&&(LFMSensor[3]== 1 )&&(LFMSensor[4]== 1 )&&(LFMSensor[5]== 0 )&&(LFMSensor[6]== 0 )&&(LFMSensor[7]== 0 ))  {mode = FOLLOWING_LINE; error =- 0;}
  else if((LFMSensor[0]== 0 )&&(LFMSensor[1]== 0 )&&(LFMSensor[2]== 0 )&&(LFMSensor[3]== 1 )&&(LFMSensor[4]== 0 )&&(LFMSensor[5]== 0 )&&(LFMSensor[6]== 0 )&&(LFMSensor[7]== 0 ))  {mode = FOLLOWING_LINE; error = -1;}
  else if((LFMSensor[0]== 0 )&&(LFMSensor[1]== 0 )&&(LFMSensor[2]== 1 )&&(LFMSensor[3]== 1 )&&(LFMSensor[4]== 0 )&&(LFMSensor[5]== 0 )&&(LFMSensor[6]== 0 )&&(LFMSensor[7]== 0 ))  {mode = FOLLOWING_LINE; error = -2;}
  else if((LFMSensor[0]== 0 )&&(LFMSensor[1]== 0 )&&(LFMSensor[2]== 1 )&&(LFMSensor[3]== 0 )&&(LFMSensor[4]== 0 )&&(LFMSensor[5]== 0 )&&(LFMSensor[6]== 0 )&&(LFMSensor[7]== 0 ))  {mode = FOLLOWING_LINE; error = -3;}
  else if((LFMSensor[0]== 0 )&&(LFMSensor[1]== 1 )&&(LFMSensor[2]== 1 )&&(LFMSensor[3]== 0 )&&(LFMSensor[4]== 0 )&&(LFMSensor[5]== 0 )&&(LFMSensor[6]== 0 )&&(LFMSensor[7]== 0 ))  {mode = FOLLOWING_LINE; error = -4;}
  else if((LFMSensor[0]== 0 )&&(LFMSensor[1]== 1 )&&(LFMSensor[2]== 0 )&&(LFMSensor[3]== 0 )&&(LFMSensor[4]== 0 )&&(LFMSensor[5]== 0 )&&(LFMSensor[6]== 0 )&&(LFMSensor[7]== 0 ))  {mode = FOLLOWING_LINE; error = -5;}
  else if((LFMSensor[0]== 1 )&&(LFMSensor[1]== 1 )&&(LFMSensor[2]== 0 )&&(LFMSensor[3]== 0 )&&(LFMSensor[4]== 0 )&&(LFMSensor[5]== 0 )&&(LFMSensor[6]== 0 )&&(LFMSensor[7]== 0 ))  {mode = FOLLOWING_LINE; error = -6;}
  else if((LFMSensor[0]== 1 )&&(LFMSensor[1]== 0 )&&(LFMSensor[2]== 0 )&&(LFMSensor[3]== 0 )&&(LFMSensor[4]== 0 )&&(LFMSensor[5]== 0 )&&(LFMSensor[6]== 0 )&&(LFMSensor[7]== 0 ))  {mode = FOLLOWING_LINE; error = -7;}
  else if((LFMSensor[0]== 0 )&&(LFMSensor[1]== 0 )&&(LFMSensor[2]== 0 )&&(LFMSensor[3]== 1 )&&(LFMSensor[4]== 1 )&&(LFMSensor[5]== 0 )&&(LFMSensor[6]== 0 )&&(LFMSensor[7]== 0 ))  {mode = STOPPED; error = 0;}
  else if((LFMSensor[0]== 0 )&&(LFMSensor[1]== 0 )&&(LFMSensor[2]== 0 )&&(LFMSensor[3]== 1 )&&(LFMSensor[4]== 1 )&&(LFMSensor[5]== 0 )&&(LFMSensor[6]== 0 )&&(LFMSensor[7]== 0 ))  {mode = NO_LINE; error = 0;}
}

//-------SENSOR TESTING-------------
void testLFMSensors()
{
     int LFMS0 = digitalRead(LFMSensor0);
     int LFMS1 = digitalRead(LFMSensor1);
     int LFMS2 = digitalRead(LFMSensor2);
     int LFMS3 = digitalRead(LFMSensor3);
     int LFMS4 = digitalRead(LFMSensor4);
     int LFMS5 = digitalRead(LFMSensor5);
     int LFMS6 = digitalRead(LFMSensor6);
     int LFMS7 = digitalRead(LFMSensor7);
     
     Serial.print ("LFMS: L  0 1 2 3 4 5 6 7  R --> "); 
     Serial.print (LFMS0); 
     Serial.print (" ");
     Serial.print (LFMS1); 
     Serial.print (" ");
     Serial.print (LFMS2); 
     Serial.print (" ");
     Serial.print (LFMS3); 
     Serial.print (" ");
     Serial.print (LFMS54); 
     Serial.print (" ");
     Serial.print (LFMS5);
     Serial.print (" ");
     Serial.print (LFMS6);
     Serial.print (" ");
     Serial.print (LFMS7);   
     Serial.print ("  --> ");
    
     Serial.print (" P: ");
     Serial.print (P);
     Serial.print (" I: ");
     Serial.print (I);
     Serial.print (" D: ");
     Serial.print (D);
     Serial.print (" PID: ");
     Serial.println (PIDvalue);
}
