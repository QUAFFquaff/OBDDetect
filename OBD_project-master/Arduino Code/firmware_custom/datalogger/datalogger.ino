
/*************************************************************************
* Vehicle Telemetry Data Logger for Freematics ONE+
*
* Developed by Stanley Huang <stanley@freematics.com.au>
* Distributed under BSD license
* Visit https://freematics.com/products/freematics-one-plus for more info
*
* THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
* IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
* FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
* AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
* LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
* OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
* THE SOFTWARE.
*************************************************************************/

#include <FreematicsPlus.h>
// #include <httpd.h>
// #include "datalogger.h"
#include "config.h"
#include "BluetoothSerial.h"

#if !defined(CONFIG_BT_ENABLED) || !defined(CONFIG_BLUEDROID_ENABLED)
#error Bluetooth is not enabled! Please run `make menuconfig` to and enable it
#endif

// states
#define STATE_STORE_READY 0x1
#define STATE_OBD_READY 0x2
#define STATE_GPS_FOUND 0x4
#define STATE_GPS_READY 0x8
#define STATE_MEMS_READY 0x10
#define STATE_FILE_READY 0x20
#define STATE_STANDBY 0x40

// void executeCommand();

// uint16_t MMDD = 0;
// uint32_t UTC = 0;
// uint32_t startTime = 0;
unsigned long startTime = 0;
//time_t t=now();
uint32_t pidErrors = 0;
float accBias[3];
char buf[50];
// uint32_t fileid = 0;
// live data
char vin[18] = {0};
// int16_t batteryVoltage = 0;

 typedef struct {
    byte pid;
    byte tier;
    int16_t value;
    uint32_t ts;
 } PID_POLLING_INFO;

// PID_POLLING_INFO obdData[]= {
//    {PID_SPEED, 1},
//   {PID_RPM, 1},
//   {PID_THROTTLE, 1},
//   {PID_ENGINE_LOAD, 1},
// };



#if MEMS_MODE
float acc[3] = {0};
float gyr[3] = {0};
float mag[3] = {0};
ORIENTATION ori = {0};
#endif

//#if USE_GPS
//GPS_DATA gd = {0};
//#endif

// char command[16] = {0};

COBDSPI obd;
BluetoothSerial SerialBT;
FreematicsESP32 sys;

// class DataOutputter : public NullLogger {
class DataOutputter {
public:
   void print(const char* str) {
      Serial.print(str);
      SerialBT.print(str);
   }
   void println(const char* str) {
      Serial.println(str);
      SerialBT.println(str);
   }
};

DataOutputter printer;
MPU9250_9DOF mems;

void calibrateMEMS()
{
      // MEMS data collected while sleeping
      accBias[0] = 0;
      accBias[1] = 0;
      accBias[2] = 0;
      int n;
      for (n = 0; n < 100; n++) {
         float acc[3] = {0};
         mems.read(acc);
         accBias[0] += acc[0];
         accBias[1] += acc[1];
         accBias[2] += acc[2];
         delay(10);
      }
      accBias[0] /= n;
      accBias[1] /= n;
      accBias[2] /= n;
      Serial.print("ACC Bias:");
      Serial.print(accBias[0]);
      Serial.print('/');
      Serial.print(accBias[1]);
      Serial.print('/');
      Serial.println(accBias[2]);

      // Serial.print("Device accel bias:");
      // Serial.print(mems.accelBias[0]);
      // Serial.print('/');
      // Serial.print(mems.accelBias[1]);
      // Serial.print('/');
      // Serial.println(mems.accelBias[2]);
}

class DataLogger
{
public:
      void init()
      {
         Serial.print("OBD...");
         if (obd.init()) {
            Serial.println("OK");
            pidErrors = 0;
         } else {
            Serial.println("NO");
            // standby();
         }
         setState(STATE_OBD_READY);
//
//#if USE_GPS
//         if (!checkState(STATE_GPS_FOUND)) {
//            Serial.print("GPS...");
//            if (sys.gpsInit(GPS_SERIAL_BAUDRATE)) {   
//               setState(STATE_GPS_FOUND);
//               Serial.println("OK");
//               //waitGPS();
//            } else {
//               Serial.println("NO");
//            }
//         }
//#endif

         startTime = millis();
      } // end of init()

//#if USE_GPS
//      void printGPSData()
//      {
//            // issue the command to get parsed GPS data
//            if (checkState(STATE_GPS_FOUND) && sys.gpsGetData(&gd)) {
//                  // store.setTimestamp(millis());
//                  // if (gd.time && gd.time != UTC) {
//                  //    byte day = gd.date / 10000;
//                  //    if (MMDD % 100 != day) {
//                  //       store.log(PID_GPS_DATE, gd.date);
//                  //    }
//                     // store.log(PID_GPS_TIME, gd.time);
//                     // store.log(PID_GPS_LATITUDE, gd.lat);
//                     // store.log(PID_GPS_LONGITUDE, gd.lng);
//                     // store.log(PID_GPS_ALTITUDE, gd.alt);
//                     // store.log(PID_GPS_SPEED, gd.speed);
//                     // store.log(PID_GPS_SAT_COUNT, gd.sat);
//                  //    // save current date in MMDD format
//                  //    unsigned int DDMM = gd.date / 100;
//                  //    UTC = gd.time;
//                  //    MMDD = (DDMM % 100) * 100 + (DDMM / 100);
//                  //    // set GPS ready flag
//                  //    setState(STATE_GPS_READY);
//                  // }
//               // sprintf(buf, " LAT=%d LON=%d SAT=%d", gd.lat, gd.lng, gd.sat);
//               sprintf(buf, ",%d,%d", gd.lat, gd.lng);
//               printer.print(buf); 
//            }
//            else {
//               printer.print(",NOGPS,NOGPS");
//            }
//      }
//      // void waitGPS()
//      // {
//      //       int elapsed = 0;
//      //       GPS_DATA gd = {0};
//      //       for (uint32_t t = millis(); millis() - t < 300000;) {
//      //          int t1 = (millis() - t) / 1000;
//      //          if (t1 != elapsed) {
//      //             Serial.print("Waiting for GPS (");
//      //             Serial.print(elapsed);
//      //             Serial.println(")");
//      //             elapsed = t1;
//      //          }
//      //          // read parsed GPS data
//      //          if (sys.gpsGetData(&gd) && gd.sat != 0 && gd.sat != 255) {
//      //             Serial.print("SAT:");
//      //             Serial.println(gd.sat);
//      //             break;
//      //          }
//      //       }
//      // }
//#endif

      void standby()
      {
         // store.close();
//#if USE_GPS
//         if (checkState(STATE_GPS_READY)) {
//            Serial.print("GPS:");
//            sys.gpsInit(0); // turn off GPS power
//            Serial.println("OFF");
//         }
//#endif // USE_GPS
         clearState(STATE_OBD_READY | STATE_GPS_READY | STATE_FILE_READY);
         setState(STATE_STANDBY);
         Serial.println("Standby");
         SerialBT.println("Standby");
#if MEMS_MODE
         if (checkState(STATE_MEMS_READY)) {
            calibrateMEMS();
            while (checkState(STATE_STANDBY)) {
               // calculate relative movement
               float motion = 0;
               for (byte n = 0; n < 10; n++) {
                  mems.read(acc);
                  for (byte i = 0; i < 3; i++) {
                     float m = (acc[i] - accBias[i]);
                     motion += m * m;
                  }

                  //delay(100);
               }
               // check movement
               if (motion > WAKEUP_MOTION_THRESHOLD * WAKEUP_MOTION_THRESHOLD) {
                  Serial.print("Motion:");
                  Serial.println(motion);
                  break;
               }
            }
         }
#else
         while (!obd.init()) Serial.print('.');
#endif // MEMS_MODE
         Serial.println("Wakeup");
         SerialBT.println("Wakeup");
         // ESP.restart();
      }
      bool checkState(byte flags) { return (m_state & flags) == flags; }
      void setState(byte flags) { m_state |= flags; }
      void clearState(byte flags) { m_state &= ~flags; }
private:
      byte m_state = 0;
};

DataLogger logger;
char buffer[128];

void setup()
{
      delay(1000);

      // initialize USB serial
      Serial.begin(115200);

      // initialize Bluetooth classic serial (SPP)
      SerialBT.begin("Freematics"); //Bluetooth device name
      Serial.println("The device started, now you can pair it with bluetooth!");
      Serial.print("ESP32 ");
      Serial.print(ESP.getCpuFreqMHz());
      Serial.print("MHz ");
      Serial.print(getFlashSize() >> 10);
      Serial.println("MB Flash");

      sys.begin();

      // init LED pin
      pinMode(PIN_LED, OUTPUT);
      pinMode(PIN_LED, HIGH);
      byte ver = obd.begin();
      Serial.print("Firmware Ver. ");
      Serial.println(ver);

      obd.getVIN(buffer, sizeof(buffer));

#if MEMS_MODE
      Serial.print("MEMS...");
      byte ret = mems.begin(ENABLE_ORIENTATION);
      if (ret) {
         logger.setState(STATE_MEMS_READY);
         if (ret == 2) Serial.print("9-DOF ");
         Serial.println("OK");
         calibrateMEMS();
      } else {
         Serial.println("NO");
      }
#endif

      pinMode(PIN_LED, LOW);
      logger.init();
}

unsigned long count = 0;
boolean obdConnected = true;


void loop() {
  Serial.print("loop start");
Serial.println((millis()));
#if USE_OBD
   if (!obdConnected) {
      sprintf(buf, "packets sent before OBD fail: %d", count);
      printer.println(buf);
      sprintf(buf, "resetting SPI interface", count);
      printer.println(buf);
      obd.end();
      //delay(50);
      obd.begin();
      sprintf(buf, "re-init OBD connection", count);
      printer.println(buf);
      while (!obd.init()) {
         printer.print(".");
      }
      printer.println("");
      obdConnected = true;
   }

   // Serial.print('[');
   // Serial.print(millis());
   // Serial.print("] #");
   // Serial.print(count++);
   
   int value;
   // retrieve VIN
   //char buffer[128];
   //obd.getVIN(buffer, sizeof(buffer));
   String vinstring = String(buffer); 
   Serial.print("VIN ");
   Serial.println((millis() ));
   vinstring.replace(" ","");
   vinstring.replace("490201000000","");
   vinstring.replace("490202","");
   vinstring.replace("490203","");
   vinstring.replace("490204","");
   vinstring.replace("490205","");
   vinstring.replace("\r","");
    Serial.print("+++++++++++++VIN:");
    Serial.println(vinstring);
   char vinbuf[34];
   vinstring.toCharArray(vinbuf,34);
   
//   strncpy(vin, buffer, sizeof(vin) - 1);
   printer.print(vinbuf);
   Serial.print("VIN BUF");
    Serial.println( (millis()));

   if (obd.readPID(PID_SPEED,value)) { 
      // sprintf(buf, " SPEED:%d", value);
      sprintf(buf, ",%d,", value);
      printer.print(buf);
   }else {
      pidErrors++;
      // sprintf(buf, "PID errors: %d", pidErrors);
      printer.print(buf);
      // obd.reset();
      // while (!obd.init()) {
      //    printer.print(".");
      //    obd.reset();
      // }
      // do {
      //    obd.reset();
      // } while(!obd.init());
      // while (true) {
      //    sprintf(buf, "packets sent before OBD fail: %d", count);
      //    delay(1000);
      // }
      // ESP.restart();
      obdConnected = false;
      return;
   }
    Serial.print("SPEED BUF");
    Serial.println( (millis()));
#endif

#if MEMS_MODE
   if (true) {
      if (mems.read(acc, gyr, mag)) {
         // sprintf(buf, " ACC x:%.2f y:%.2f z:%.2f", acc[0]-accBias[0],acc[1]-accBias[1],acc[2]-accBias[2]);
         // sprintf(buf, " ACC x:%.2f y:%.2f z:%.2f", acc[0],acc[1],acc[2]);
         sprintf(buf, "%.3f,%.3f,%.3f", acc[0],acc[1],acc[2]);
         printer.print(buf);
         // delay(5);
         sprintf(buf, ",%.2f,%.2f,%.2f", gyr[0],gyr[1],gyr[2]);
         printer.print(buf);
      }
   }
   Serial.print("ACC ");
      Serial.println( (millis() ));
#endif
//#if USE_GPS
////strncpy(vin, buffer, sizeof(vin) - 1);
////printer.print(vin)
//#endif

//#if USE_GPS
//   // logger.logGPSData();
//   logger.printGPSData();
//#endif
   printer.println("");
   // delay(100);
   // executeCommand();
}
