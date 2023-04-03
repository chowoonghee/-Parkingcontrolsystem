// #define TRIG 6 //TRIG 핀 설정 (초음파 보내는 핀)
// #define ECHO 7 //ECHO 핀 설정 (초음파 받는 핀)
// #define BUZZER 2

#include <Keypad.h>
#include <Servo.h>
#define SERVOPIN 3
#include <LiquidCrystal_I2C.h>
LiquidCrystal_I2C lcd(0x27,16,2);

#define Rows 4
#define Cols 4

char keys[Rows][Cols]={
{'1','2','3','A'},
{'4','5','6','B'},
{'7','8','9','C'},
{'*','0','#','D'}
};

byte RowPinTbl[Rows]={8,11,12,13};
byte ColPinTbl[Cols]={7,6,5,4};

Keypad keypad = Keypad( makeKeymap(keys), RowPinTbl, ColPinTbl, Rows, Cols );



// int note = 1000; 

Servo myservo;
int pos = 0; //각도

int b= 0;

char rx;

void down(){
  for(pos=0; pos<=90; pos+=1){
    // 1도씩 이동
    delay(20);
    myservo.write(pos);
  }
}
void up(){
   for (pos=90;pos>=0;pos-=1){
    delay(20);
    myservo.write(pos);
  }
  for(int i=0; i <Rows;i++){
    pinMode(RowPinTbl[i],INPUT_PULLUP);
  }

  for(int j=0; j<Cols; j++){
    pinMode(ColPinTbl[j],OUTPUT); //초기값 HIGH
    digitalWrite(ColPinTbl[j],HIGH);
  }

}


void setup() {

  pinMode(2, OUTPUT);
  pinMode(10, OUTPUT);
  pinMode(9, OUTPUT);


  lcd.init();
  lcd.backlight();
  lcd.print("LCD start");
  delay(1000);
  lcd.clear();

  myservo.attach(SERVOPIN);
  Serial.begin(9600);

 for(int i=0; i <Rows;i++){
    pinMode(RowPinTbl[i],INPUT_PULLUP);
  }

  for(int j=0; j<Cols; j++){
    pinMode(ColPinTbl[j],OUTPUT); //초기값 HIGH
    digitalWrite(ColPinTbl[j],HIGH);
  }
  // pinMode(TRIG,OUTPUT);
  // pinMode(ECHO,INPUT);
  //pinMode(BUZZER,OUTPUT);
}

void loop() {
  // long duration, distance;

  // digitalWrite(TRIG,LOW);
  // delayMicroseconds(2);
  // digitalWrite(TRIG,HIGH);
  // delayMicroseconds(10);
  // digitalWrite(TRIG,LOW);
  
  // duration = pulseIn(ECHO,HIGH);

  // distance=duration * 17 / 1000; // pulsein * 340 /10000/2
  
  // Serial.println(duration);
  // Serial.print("\n Distance :");
  // Serial.print(distance);
  // Serial.println(" Cm");
  // delay(500);
  
  
  // if(distance <40 ){
  //   if(b == 0){
  //     analogWrite(11, 255);
  //     analogWrite(10, 0);
  //     analogWrite(9, 0);
  //     lcd.print("OPEN");
  //     delay(1000);
  //     tone(BUZZER,note,500);
  //     up();
  //     b=2;
  //     lcd.clear();
  //     }
  //  }
    
  // else if(distance>40){
  //   if (b==2){
  //     analogWrite(11, 0);
  //     analogWrite(10, 255);
  //     analogWrite(9, 0);
  //     lcd.print("CLOSE");
  //     delay(1000);
  //     tone(BUZZER,note,500);
  //     down();
  //     b=0;
  //     lcd.clear();
  //   }
  // }

  // for(int j=0; j<Cols; j++){
  //   digitalWrite(ColPinTbl[j],LOW); // Col 라인 Active Low
  //   for(int i =0; i<Rows; i++){
  //     if(digitalRead(RowPinTbl[i])==LOW){ // check Row 라인
  //       Serial.print("row=");
  //       Serial.print(i);
  //       Serial.print(", Column=");
  //       Serial.println(j);
  //       Serial.print(", Key Number=");
  //       Serial.println(keys[i][j]);
  //     }
  //   }
  //   digitalWrite(ColPinTbl[j],HIGH); // Col 라인 다시 High
  // }


  char key = keypad.getKey();

  if (key) {
    switch(key) {
      case 'A': 
        analogWrite(11, 0);
        analogWrite(10, 0);
        analogWrite(2, 255);
        up();
        break;
      case 'B': 
        analogWrite(11, 0);
        analogWrite(10, 255);
        analogWrite(2, 0);
        down();
        break;
      case '1':
        Serial.println('1');
        break;
      case '2':
        Serial.println('2');
        break;
      case '3':
        Serial.println('3');
        break;
      case '4':
        Serial.println('4');
        break;
      case '5':
        Serial.println('5');
        break;
      case '6':
        Serial.println('6');
        break;
      case '7':
        Serial.println('7');
        break;
      case '8':
        Serial.println('8');
        break;
      case '9':
        Serial.println('9');
        break;
      case '0':
        Serial.println('0');
        break;
      case 'C':
        Serial.println('clear');
        break;
      case 'D':
        Serial.println('del');
        break;
      
      case '*':
        Serial.println('carin');
        break;

    }
  }


  if(Serial.available()){
    rx=Serial.read();
    if(rx=='a'){
      b=3;
      analogWrite(11, 0);
      analogWrite(10, 0);
      analogWrite(2, 255);
      lcd.print("TEST OPEN");
      //delay(1000);
      // tone(BUZZER,note,500);
      up();
      //lcd.clear();
      delay(3000);
      lcd.clear();
      analogWrite(11, 0);
      analogWrite(10, 255);
      analogWrite(2, 0);
      down();
      lcd.print("TEST CLOSE");
      lcd.clear();
      //Serial.print("OPEN TEST");
    }
    else if(rx=='s'){
      analogWrite(11, 0);
      analogWrite(10, 255);
      analogWrite(2, 0);
      lcd.print("TEST CLOSE");
      delay(1000);
      // tone(BUZZER,note,500);
      down();
      b=3;
      lcd.clear();
      Serial.print("CLOSE TEST");
    }

    else if(rx=='d'){
      lcd.print("TEST clear");
      delay(1000);
      lcd.clear();
      // tone(BUZZER,note,500);
      b=0;
      Serial.print("OPEN TEST");
    }
  }
}




