const int MAX = 8;
int i = 0;
unsigned int b[MAX];
unsigned int value;
unsigned char nv;


void setup()
{ 
  analogReference(INTERNAL);
  Serial.begin(230400);

}

void loop()  {
    if (i < MAX) {
     
      value = analogRead(0);
      b[i++] = value;
      delayMicroseconds(380);
      
    } else {
      i = 0;
        for(int j=0; j<MAX; j++)  {
        nv =  b[j]/256;
        Serial.write(0);
        Serial.write(nv&0xff); 
        nv = b[j]%256;
        Serial.write(nv&0xff);
      }
    }

}
