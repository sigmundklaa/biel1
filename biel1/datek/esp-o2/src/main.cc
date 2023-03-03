
#include <Arduino.h>
#include <SPIFFS.h>
#include <WebServer.h>
#include <WiFi.h>

#define PIN_POT_ (4)

#define SSID_ "MidjoSkyen"
#define PASS_ "123456789"

static struct {
    IPAddress local, gateway, subnet;
} ip_{{192, 168, 1, 2}, {192, 168, 1, 2}, {255, 255, 255, 0}};

static WebServer server{81};

static struct __attribute__((packed)) housekeeping_ {
    uint16_t potval;
} hk_;

static void
hk_init_(void)
{
    File fp = SPIFFS.open("/store/hk", FILE_WRITE);

    if (!fp) {
        return;
    }

    fp.write((uint8_t*)(&hk_), sizeof(hk_));
    fp.close();
}

static void
hk_save_(void)
{
    File fp = SPIFFS.open("/store/hk", FILE_READ);

    if (!fp) {
        return;
    }

    fp.read((uint8_t*)(&hk_), sizeof(hk_));
    fp.close();
}

static void
handle_root_(void)
{
    server.send(200, "text/html", "");
}

void
setup()
{
    Serial.begin(9600);

    if (!SPIFFS.begin(true)) {
        Serial.println("cant initialize fs");
        return;
    }

    File fp = SPIFFS.open("/file.txt");
    if (fp) {
        while (fp.available()) {
            Serial.write(fp.read());
        }

        fp.close();
    }

    WiFi.softAP(SSID_, PASS_);
    WiFi.softAPConfig(ip_.local, ip_.gateway, ip_.subnet);

    server.on("/", handle_root_);

    pinMode(PIN_POT_, INPUT);
    hk_init_();

    Serial.println("housekeeping data: " + String(hk_.potval));
}

void
loop()
{
    static uint64_t last_save_ms = 0;
    uint64_t tmp = millis();

    if (tmp - last_save_ms >= 500) {
        hk_save_();
    }

    hk_.potval = analogRead(PIN_POT_);
    server.handleClient();
}

void
background_loop(void)
{
}