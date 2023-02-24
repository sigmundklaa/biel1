
#include "env.h"
#include <Arduino.h>
#include <WebServer.h>
#include <WiFi.h>

/*
Oppgave 1d)
- De sentrale forskjellene mellom ESP32 og Arduino Uno er at ESP32 er både et
  billigere og kraftigere alternativ til Arduino. ESP32 har bl.a. innebygd WiFi
  og bluetooth støtte, 2 kjerner og støtter en langt høyere klokkefrekvens.
- ESP32 har en maks klokkehastighet på 240MHz.
- Upload Speed er baud-raten som brukes for opplasting av binary-filen til
  ESP-en. Endring av denne endrer tiden det tar å laste opp denne filen.
*/

#define PIN_BLINK_ (32)
#define BLINK_INTERVAL_MS_ (500)

#define PIN_R_ (27)
#define PIN_G_ (26)
#define PIN_B_ (25)
#define LED_PWM_RESO_ (8)
#define LED_PWM_FREQ_ (5000)

#define PRINT_INTERVAL_MS_ (10000)

#define PIN_POT_ (35)
#define PIN_PHR_ (34)
#define SENSOR_UPDATE_INTERVAL_MS_ (5000)

static const uint8_t led_chan_ = 0;

static inline double
to_3v3(uint16_t val)
{
    return (static_cast<double>(map(val, 0, 4095, 0, 3300))) / 1000;
}

static class blinker__
{
  protected:
    uint8_t m_pin;
    uint8_t m_mode;
    uint64_t m_time_last_ms;

  public:
    inline blinker__(uint8_t pin) : m_pin(pin) { pinMode(m_pin, OUTPUT); }

    inline void
    blink()
    {
        uint64_t tmp = millis();
        if (tmp - m_time_last_ms >= BLINK_INTERVAL_MS_) {
            m_time_last_ms = tmp;
            m_mode = !m_mode;
        }

        digitalWrite(m_pin, m_mode);
    }
} blinker_{PIN_BLINK_};

static String
make_html(const String& body)
{
    String fmt{"<!DOCTYPE html><html><head><title>Sensordata</title><meta "
               "http-equiv='refresh' content='0.5'></head><body>"};
    fmt += body;
    fmt += "</body></html>";

    return fmt;
}

static class sensors__
{
  protected:
    uint8_t m_potpin;
    uint8_t m_phrpin;
    uint64_t m_time_last_ms;
    uint8_t buf[100];

    uint16_t m_readpot;
    uint16_t m_readphr;

  public:
    inline sensors__(uint8_t pot, uint8_t phr) : m_potpin(pot), m_phrpin(phr)
    {
        pinMode(m_potpin, INPUT);
        pinMode(m_phrpin, INPUT);
    }

    inline double
    phrval()
    {
        return to_3v3(m_readphr);
    }

    inline double
    potval()
    {
        return to_3v3(m_readpot);
    }

    inline void
    update()
    {
        uint64_t tmp = millis();

        if (tmp - m_time_last_ms < SENSOR_UPDATE_INTERVAL_MS_) {
            return;
        }

        m_time_last_ms = tmp;
        m_readphr = analogRead(m_phrpin);
        m_readpot = analogRead(m_potpin);

        Serial.println(
            "Voltage photoresistor: " + String(this->phrval()) +
            ", voltage potentiometer: " + String(this->potval())
        );
    }
} sensors_{PIN_POT_, PIN_PHR_};

static class pwmled__
{
  protected:
    uint8_t m_pins[3];
    uint8_t m_chan_offset;
    uint16_t m_values[3];

  public:
    inline pwmled__(uint8_t offset, uint8_t r, uint8_t g, uint8_t b)
        : m_chan_offset(offset), m_pins{r, g, b}
    {
        for (uint8_t i = 0; i < 3; i++) {
            ledcSetup(m_chan_offset + i, LED_PWM_FREQ_, LED_PWM_RESO_);
            ledcAttachPin(m_pins[i], m_chan_offset + i);
        }
    }

    inline void
    set(uint16_t r, uint16_t g, uint16_t b)
    {
        m_values[0] = r;
        m_values[1] = g;
        m_values[2] = b;
    }

    inline void
    write()
    {
        for (uint8_t i = 0; i < 3; i++) {
            ledcWrite(m_chan_offset + i, m_values[0]);
        }
    }
} pwmled_{0, PIN_R_, PIN_G_, PIN_B_};

static WebServer server(80);

static void
on_root()
{
    server.send(
        200, "text/html",
        make_html(
            String("<h1>Sensor 1: ") + String(sensors_.phrval()) +
            String(
                "</h1><h1>Sensor 2: " + String(sensors_.potval()) +
                String("</h1>")
            )
        )
    );
}

void
setup()
{
    // put your setup code here, to run once:
    Serial.begin(9600);

    WiFi.begin(WF_SSID, WF_PASS);
    while (WiFi.status() != WL_CONNECTED) {
        delay(1000);
        Serial.println("Establishing connection...");
    }
    Serial.println("Connected (IP: " + WiFi.localIP().toString() + ")");

    server.on("/", on_root);
    server.begin();
}

void
loop()
{
    static uint64_t time_print_ms = 0;
    uint64_t tmp = millis();

    if (tmp - time_print_ms >= PRINT_INTERVAL_MS_) {
        Serial.println("Hello World");
        time_print_ms = tmp;
    }

    sensors_.update();
    blinker_.blink();
    server.handleClient();

    pwmled_.set(0, 4095, 2090);
    pwmled_.write();
}