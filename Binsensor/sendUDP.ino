#include <MKRNB.h>

NB nbAccess(true);
NBUDP udp;
GPRS gprs;
char apn[] = "mda.lab5e"; // replace with your APN name
char server_address[] = "172.16.15.14"; // replace with your server's IP address
int server_port = 1234; // replace with your server's port number
char pin[] = "1111";
void setup() {
  Serial.begin(9600);
  while (!Serial) {}

  // connection state
  boolean connected = false;
  //Serial.println("AT+CGDCONT=1,\"IP\",\"mda.lab5e\"");

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
  //Serial.println("AT+CGDCONT=1,\"IP\",\"mda.lab5e\"");
  udp.begin(1232);
  if (udp.beginPacket(server_address, server_port)) {
    Serial.println("Sending UDP packet");
    udp.write("Hello from Arduino!");
    udp.endPacket();
    Serial.println("Packet sent");
  } else {
    Serial.println("Unable to send UDP packet");
  }
  udp.stop();

  delay(10000); // wait for 10 seconds before sending the next packet
}
