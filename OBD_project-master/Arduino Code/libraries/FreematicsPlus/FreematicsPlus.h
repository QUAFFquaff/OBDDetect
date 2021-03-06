/*************************************************************************
* Arduino library for Freematics ONE+ (ESP32)
* Distributed under BSD license
* Visit http://freematics.com for more information
* (C)2017 Developed by Stanley Huang <support@freematics.com.au>
*************************************************************************/

#include <Arduino.h>
#include <SPIFFS.h>
#include "esp_system.h"
#include "esp_partition.h"
#include "nvs_flash.h"
#include "nvs.h"
#include "esp_spi_flash.h"
#include "FreematicsBase.h"
#include "FreematicsNetwork.h"
#include "FreematicsMEMS.h"
#include "FreematicsDMP.h"
#include "FreematicsOBD.h"
#include "FreematicsSD.h"

#define PIN_XBEE_PWR 27
#define PIN_GPS_POWER 15
#define PIN_LED 4
#define PIN_SD_CS 5

#define BEE_UART_PIN_RXD  (16)
#define BEE_UART_PIN_TXD  (17)
#define BEE_UART_NUM UART_NUM_1

#define GPS_UART_PIN_RXD  (32)
#define GPS_UART_PIN_TXD  (33)
#define GPS_UART_NUM UART_NUM_2

#define UART_BUF_SIZE (256)

#define GPS_TIMEOUT 1000 /* ms */

typedef struct {
    uint32_t date;
    uint32_t time;
    int32_t lat;
    int32_t lng;
    int16_t alt;
    uint8_t speed;
    uint8_t sat;
    int16_t heading;
} GPS_DATA;

bool gps_decode_start();
void gps_decode_stop();
int gps_get_data(GPS_DATA* gdata);
int gps_write_string(const char* string);
void gps_decode_task(int timeout);
void bee_start();
int bee_write_string(const char* string);
int bee_write_data(uint8_t* data, int len);
int bee_read(uint8_t* buffer, size_t bufsize, unsigned int timeout);
void bee_flush();
uint8_t readChipTemperature();
int32_t readChipHallSensor();
uint16_t getFlashSize(); /* KB */

class Task
{
public:
    Task():xHandle(0) {}
    bool create(void (*task)(void*), const char* name, int priority = 0);
    void destroy();
    void suspend();
    void resume();
    bool running();
    void sleep(uint32_t ms);
private:
	void* xHandle = 0;
};

class Mutex
{
public:
  Mutex();
  void lock();
  void unlock();
private:
  void* xSemaphore;
};

class FreematicsESP32 : public CFreematics
{
public:
    void begin(int cpuMHz = CONFIG_ESP32_DEFAULT_CPU_FREQ_MHZ);
    // initialize GPS (set baudrate to 0 to power off GPS)
    bool gpsInit(unsigned long baudrate = 115200L);
    // get parsed GPS data (returns the number of data parsed since last invoke)
    int gpsGetData(GPS_DATA* gdata);
    // send command string to GPS
    void gpsSendCommand(const char* cmd);
	// start xBee UART communication
	bool xbBegin(unsigned long baudrate = 115200L);
	// read data to xBee UART
	int xbRead(char* buffer, int bufsize, unsigned int timeout = 1000);
	// send data to xBee UART
	void xbWrite(const char* cmd);
    // send data to xBee UART
	void xbWrite(const char* data, int len);
	// receive data from xBee UART (returns 0/1/2)
	int xbReceive(char* buffer, int bufsize, unsigned int timeout = 1000, const char** expected = 0, byte expectedCount = 0);
	// purge xBee UART buffer
	void xbPurge();
	// toggle xBee module power
	void xbTogglePower();
};

#define MAX_BLE_MSG_LEN 160

class GATTServer : public Print
{
public:
  bool begin(const char* deviceName = 0);
  bool send(uint8_t* data, size_t len);
  size_t write(uint8_t c);
  virtual size_t onRequest(uint8_t* buffer, size_t len)
  {
    // being requested for data
    buffer[0] = 'O';
    buffer[1] = 'K';
    return 2;
  }
  virtual void onReceive(uint8_t* buffer, size_t len)
  {
    // data received is in buffer
  }
private:
  static bool initBLE();
  String sendbuf;
};