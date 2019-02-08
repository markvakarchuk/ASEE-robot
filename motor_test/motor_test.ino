

int BIN_1 = 11;
int BIN_2 = 10;
int AIN_1 = 6;
int AIN_2 = 9;
int MAX_PWM_VOLTAGE = 250 ;
int spd = 1;

void setup() {
    pinMode(BIN_1, OUTPUT);
    pinMode(BIN_2, OUTPUT);
    pinMode(AIN_1, OUTPUT);
    pinMode(AIN_2, OUTPUT);

  Serial.begin(9600);
}

void loop() {
    
    digitalWrite(BIN_2, LOW);
    digitalWrite(AIN_2, LOW);
    analogWrite(BIN_1, MAX_PWM_VOLTAGE);
    analogWrite(AIN_1, MAX_PWM_VOLTAGE);
    delay(1000);
    
    digitalWrite(BIN_1, LOW);
    digitalWrite(AIN_2, LOW);
    analogWrite(BIN_2, MAX_PWM_VOLTAGE);
    analogWrite(AIN_1, MAX_PWM_VOLTAGE);
    delay(1000);
    
    digitalWrite(BIN_2, LOW);
    digitalWrite(AIN_1, LOW);
    analogWrite(BIN_1, MAX_PWM_VOLTAGE);
    analogWrite(AIN_2, MAX_PWM_VOLTAGE);
    delay(1000);
    
    digitalWrite(BIN_1, LOW);
    digitalWrite(AIN_1, LOW);
    analogWrite(BIN_2, MAX_PWM_VOLTAGE);
    analogWrite(AIN_2, MAX_PWM_VOLTAGE);
    delay(1000);
/*
analogWrite(BIN_1,LOW);
analogWrite(AIN_1,LOW);
Serial.print("starting");
if (spd < 100) {
  while (spd < 100){
  spd ++;
  Serial.print(spd);
  Serial.print("up");
  analogWrite(BIN_1, spd);
  analogWrite(AIN_1, spd);
  delay(10);
  }
}
analogWrite(BIN_1,LOW);
analogWrite(AIN_1,LOW);
if (spd >= 100) {
  while(spd > 1){
  spd --;
  Serial.print(spd);
  Serial.print("DOWN");
  analogWrite(BIN_1, spd);
  analogWrite(AIN_1, spd);
  delay(10);
  }
}
*/

    
}
