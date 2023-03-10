#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <Wire.h>
int X;
int Y;
bool Ba=true;
bool Bb=true;
bool Bc=true;
bool Bd=true;
bool Be=true;
bool Bf=true;
bool Bg=true;
bool Bh=true;
int xd=0;


#define OLED_RESET 4
Adafruit_SSD1306 display(OLED_RESET);


void setup() {
display.begin(SSD1306_SWITCHCAPVCC, 0x3C); // Inicializar el display OLED
display.clearDisplay(); // Limpiar el display
Serial.begin(9600);
}

void loop() {
X=analogRead(A1);
Y=analogRead(A2);
display.clearDisplay(); // Limpiar el display antes de mostrar la imagen
// Definir la imagen
setLed();
setON()
display.display();

if (Y>=0 && Y<280 && X>=0 && X<280 and Ba==true){
  Serial.print ("B\n");
 Ba=false;
 Bb=true;
 Bc=true;
 Bd=true;
 Be=true;
 Bf=true;
 Bg=true;
 Bh=true;
 arrowLU();
}
else if (Y>720 && Y<=1023 && X>=0 && X<280 and Bb==true){
  Serial.print ("H\n");
 Bb=false;
 Ba=true;
 Bc=true;
 Bd=true;
 Be=true;
 Bf=true;
 Bg=true;
 Bh=true;
 arrowLD();
}
else if (Y>=0 && Y<280 && X>720 && X<=1023 and Bc==true){
  Serial.print ("D\n");
 Bc=false;
 Bb=true;
 Ba=true;
 Bd=true;
 Be=true;
 Bf=true;
 Bg=true;
 Bh=true;
 arrowRU();
}
else if (Y>720 && Y<=1023 && X>720 && X<=1023 and Bd==true){
  Serial.print ("F\n");
 Bd=false;
 Bb=true;
 Bc=true;
 Ba=true;
 Be=true;
 Bf=true;
 Bg=true;
 Bh=true;
 arrowRD();
}
else if (X>=0 && X<280 && Y>280 && Y<720 and Be==true){
  Serial.print ("A\n");
 Be=false;
 Bb=true;
 Bc=true;
 Bd=true;
 Ba=true;
 Bf=true;
 Bg=true;
 Bh=true;
 arrowLC();
}

else if (X>720 && X<=1023 && Y>280 && Y<620 and Bf==true){
  Serial.print ("E\n");
 Bf=false;
 Bb=true;
 Bc=true;
 Bd=true;
 Be=true;
 Ba=true;
 Bg=true;
 Bh=true;
 arrowRC();
}
else if (Y>=0 && Y<280 && X>280 && X<720 and Bg==true){
  Serial.print ("C\n");
 Bg=false;
 Bb=true;
 Bc=true;
 Bd=true;
 Be=true;
 Bf=true;
 Ba=true;
 Bh=true;
 arrowUC();
}
else if (Y>720 && Y<=1023 && X>280 && X<720 and Bh==true){
  Serial.print ("G\n");
 Bh=false;
 Bb=true;
 Bc=true;
 Bd=true;
 Be=true;
 Bf=true;
 Bg=true;
 Ba=true;
 arrowDC();
}

else {

  delay (100);

  
  }



  
