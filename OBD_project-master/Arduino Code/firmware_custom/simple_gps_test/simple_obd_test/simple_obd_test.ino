/******************************************************************************
* Simple OBD-II test sketch for Freematics ONE/ONE+
* Written by Stanley Huang https://www.facebook.com/stanleyhuangyc
* Distributed under BSD license
* Visit http://freematics.com/products for hardware information
*
* THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
* IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
* FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
* AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
* LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
* OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
* THE SOFTWARE.
******************************************************************************/

#include <FreematicsPlus.h>

#define PIN_LED 4

COBDSPI obd;
FreematicsESP32 sys;
bool gps_found = false;
unsigned long count = 0;
GPS_DATA gd = {0};

void setup() {
   // put your setup code here, to run once:
   pinMode(PIN_LED, OUTPUT);
   digitalWrite(PIN_LED, HIGH);
   delay(1000);
   digitalWrite(PIN_LED, LOW);
   Serial.begin(115200);
   byte ver = obd.begin();
   Serial.print("OBD Firmware Version ");
   Serial.println(ver);

   sys.begin();

   Serial.print("GPS...");
   if (sys.gpsInit(115200L)) {
      Serial.println("OK");
      gps_found = true;
   } else {
      Serial.println("NO");
   }
}

void loop() {
   char buf[50];
   // put your main code here, to run repeatedly:
   if (gps_found && sys.gpsGetData(&gd)) {
      sprintf(buf, " LAT=%d LON=%d SAT=%d", gd.lat, gd.lng, gd.sat);
      Serial.println(buf);
   }
   else {
      Serial.println("NO GPS.");
   }
   delay(100);
}
