#include <LiquidCrystal.h>
#include <TimeLib.h>

#define TIME_HEADER  "T"   // Header tag for serial time sync message
#define TIME_REQUEST  7    // ASCII bell character requests a time sync message 


// initialize the library by associating any needed LCD interface pin
// with the arduino pin number it is connected to

// button connected to pin 2 
const int button = 2;
const int rs = 12, en = 11, d4 = 4, d5 = 5, d6 = 6, d7 = 7;

// button state (0 LOW, 1 HIGH).
int buttonState = 1;
int variavel = 0;

unsigned int VSF = 60;
String info;
char data[100];
int pctime;
String timeStamp;
String temp;
String skyState;
String humState;


LiquidCrystal lcd(rs, en, d4, d5, d6, d7);

void setup() {
  // set up the LCD's number of columns and rows:
  lcd.begin(16, 2);
  Serial.begin(9600);
  pinMode(13, OUTPUT);
  
  // Synchronize the time of arduino with the external 
  setSyncProvider(requestSync);  
  
  // setting button pin (2) as input
  pinMode(button,INPUT);
}

void loop() {
  if (Serial.read()) {
    processSyncMessage();
  }
  
  buttonState = digitalRead(button);
  if (buttonState == HIGH && variavel == 0){
    variavel = 1;
    digitalClockDisplay();  
  }
  else if (buttonState == HIGH && variavel == 1){
    variavel = 0;
    chupa();
  }

  if(variavel == 0)
    chupa();
  else
    digitalClockDisplay();
  
  
  delay(1000);
}

void chupa(){
    lcd.clear();

    // Display time on first row   
    lcd.setCursor(0, 0);
    lcd.print(temp);
    lcd.print(" / ");
    lcd.setCursor(0, 1);
    lcd.print(skyState);
 
}
void digitalClockDisplay(){
    lcd.clear();

    // Display time on first row   
    lcd.setCursor(0, 0);
//    
    lcd.print("Time ");
    lcd.print(hour());
    printDigits(minute());
    printDigits(second());

    // Display date on second row
    lcd.setCursor(0, 1);
    lcd.print("Date ");
    lcd.print(day());
    lcd.print("/");
    lcd.print(month());
    lcd.print("/");
    lcd.print(year()); 
}

void printDigits(int digits){
  // utility function for digital clock display: prints preceding colon and leading 0
  lcd.print(":");
  if(digits < 10)
    lcd.print('0');
  lcd.print(digits);
}


void processSyncMessage() {
  unsigned long pctime;
  const unsigned long DEFAULT_TIME = 1534600000; // Jan 1 2013
  
  if(Serial.find(TIME_HEADER)) {
    info = Serial.readString();
    info.toCharArray(data, sizeof(data));
    timeStamp = strtok(data, ";");
    temp = strtok(NULL, ";");
    skyState = strtok(NULL, ";");
    humState = strtok(NULL, ";");
    
    pctime = timeStamp.toInt();
     if( pctime >= DEFAULT_TIME) { // check the integer is a valid time (greater than Jan 1 2013)
       setTime(pctime); // Sync Arduino clock to the time received on the serial port
     }
  }
}

time_t requestSync()
{
  Serial.write(TIME_REQUEST);  
  return 0; // the time will be sent later in response to serial mesg
}
