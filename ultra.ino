unsigned long time;

void setup() {
    Serial.begin(9600);
}

void loop() {
    Serial.print("Time: ");
    time = micros();
    
    Serial.println(time);
    delay(1000);
}