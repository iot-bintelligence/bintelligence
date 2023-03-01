#include <MKRNB.h>

// Define sensor pin numbers
#define TRIG_PIN 13
#define ECHO_PIN 14

#define SAMPLING_PERIOD_M 15
#define SAMPLING_PERIOD_MS (SAMPLING_PERIOD_M * 60 * 1000)

#define SOUND_VELOCITY_M_PER_S 343

NB nbAccess;
NBUDP udp;
GPRS gprs;
char apn[] = "mda.lab5e";                // replace with your APN name
char server_address[] = "172.16.15.14";  // replace with your server's IP address
uint16_t server_port = 1234;               // replace with your server's port number
char pin[] = "1111";
uint16_t localUdpPort = 1232;

void transmit(uint16_t distance) {
  udp.begin(localUdpPort);
  if (udp.beginPacket(server_address, server_port)) {
    Serial.println("Sending UDP packet");
    udp.write(distance);
    udp.endPacket();
    Serial.println("Packet sent");
  } else {
    Serial.println("Unable to send UDP packet");
  }
  udp.stop();
}

void setup() {
  // Init serial communication with PC, if one is connected
  Serial.begin(115200);

  // Set sensor pin modes
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);

  // connection state
  bool connected = false;

  Serial.println("Starting connecting");

  // After starting the modem with NB.begin()
  // attach to the GPRS network with the APN, login and password
  while (!connected) {
    if ((nbAccess.begin(pin, apn) == NB_READY) && (gprs.attachGPRS() == GPRS_READY)) {
      Serial.println("Attached to gprs");
      connected = true;
    } else {
      Serial.println("Not connected");
      delay(1000);
    }
  }

  Serial.println("Connected to the GPRS network");
}

void loop() {
  // Create wave
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);

  // Receive return wave, measure time, calculate distance
  uint32_t duration_us = pulseIn(ECHO_PIN, HIGH);
  uint16_t distance_mm = (uint16_t)(duration_us * SOUND_VELOCITY_M_PER_S / 2 / 1000);

  // Transmit measurement to PC
  Serial.print("Distance: ");
  Serial.print(distance_mm);
  Serial.println(" mm");

  // Transmit measurement to cloud
  transmit(distance_mm);

  // Wait for next measurement
  delay(SAMPLING_PERIOD_MS);
}
