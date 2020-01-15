void setup() {
    Serial.begin(9600);
}

void loop() {
    unsigned char confirm_byte;
    confirm_byte = Serial.read();
    if (confirm_byte == 0xFF)
        Serial.println("hello");
}
