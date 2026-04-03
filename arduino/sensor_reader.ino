// Air Purification + Water Generation System
// Arduino Uno Sensor Integration

// Pin Definitions
#define MQ135_PIN A0      // MQ-135 Gas Sensor
#define FC28_PIN A1       // FC-28 Water Tank Level Sensor
#define TDS_PIN A2        // TDS Sensor
#define DHT_PIN 2         // DHT22 Sensor

// Libraries (Install these via Arduino IDE Library Manager)
// #include <DHT.h>
// #include <PMS.h>
// #include <SoftwareSerial.h>

// DHT22 Setup
// DHT dht(DHT_PIN, DHT22);

// PMS5003 Setup (RX=10, TX=11)
// SoftwareSerial pmsSerial(10, 11);
// PMS pms(pmsSerial);
// PMS::DATA pmsData;

void setup() {
  Serial.begin(9600);
  
  // Initialize sensors
  // dht.begin();
  // pmsSerial.begin(9600);
  
  pinMode(MQ135_PIN, INPUT);
  pinMode(FC28_PIN, INPUT);
  pinMode(TDS_PIN, INPUT);
  
  delay(2000); // Warm-up time
}

void loop() {
  // Read MQ-135 (Air Quality)
  int mq135Raw = analogRead(MQ135_PIN);
  float mq135Value = map(mq135Raw, 0, 1023, 0, 500); // Convert to ppm
  
  // Read DHT22 (Temperature & Humidity)
  // float temperature = dht.readTemperature();
  // float humidity = dht.readHumidity();
  float temperature = 25.5; // Simulated value
  float humidity = 60.0;    // Simulated value
  
  // Read PMS5003 (Particulate Matter)
  // if (pms.read(pmsData)) {
  //   float pm25 = pmsData.PM_AE_UG_2_5;
  //   float pm10 = pmsData.PM_AE_UG_10_0;
  // }
  float pm25 = 15.0;  // Simulated value
  float pm10 = 25.0;  // Simulated value
  
  // Read FC-28 (Water Tank Level)
  int fc28Raw = analogRead(FC28_PIN);
  float fc28Value = map(fc28Raw, 0, 1023, 0, 100); // Convert to percentage (0% = empty, 100% = full)
  
  // Read TDS Sensor (Water Quality)
  int tdsRaw = analogRead(TDS_PIN);
  float tdsValue = map(tdsRaw, 0, 1023, 0, 1000); // Convert to ppm
  
  // Send JSON data via Serial
  Serial.print("{");
  Serial.print("\"mq135\":");
  Serial.print(mq135Value);
  Serial.print(",\"temperature\":");
  Serial.print(temperature);
  Serial.print(",\"humidity\":");
  Serial.print(humidity);
  Serial.print(",\"pm25\":");
  Serial.print(pm25);
  Serial.print(",\"pm10\":");
  Serial.print(pm10);
  Serial.print(",\"fc28\":");
  Serial.print(fc28Value);
  Serial.print(",\"tds\":");
  Serial.print(tdsValue);
  Serial.println("}");
  
  delay(2000); // Read every 2 seconds
}
