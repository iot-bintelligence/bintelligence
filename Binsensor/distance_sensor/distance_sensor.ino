
// Define sensor pin numbers
#define TRIG_PIN 7
#define ECHO_PIN 8

#define SAMPLING_FREQUENCY_HZ 10.0F
#define SAMPLING_PERIOD_MS (1000 / SAMPLING_FREQUENCY_HZ)

unsigned long next_measurement;



void setup() {
  // Init serial communication with PC
  Serial.begin(115200);

  // Set sensor pin modes
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
}

void loop() {
  // Will overflow and stop working after approximately 50 days
  while (next_measurement > millis())
  {
    delay(1);
  }
  next_measurement += SAMPLING_PERIOD_MS;
  
  // Create wave
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);

  // Receive return wave, measure time, calculate distance
  long duration = pulseIn(ECHO_PIN, HIGH);
  float distance = duration * 0.034 / 2;

  // Transmit measurment to PC
  Serial.print("Distance: ");
  Serial.print(distance);
  Serial.println(" cm");
}
