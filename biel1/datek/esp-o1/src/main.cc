
#include <Arduino.h>

/*
Oppgave 1d)
- De sentrale forskjellene mellom ESP32 og Arduino Uno er at ESP32 er både et
  billigere og kraftigere alternativ til Arduino. ESP32 har innebygd WiFi og
  bluetooth støtte, 2 kjerner og en langt høyere klokkefrekvens.
- ESP32 har en maks klokkehastighet på 240MHz.
- Upload Speed er baud-raten som brukes for opplasting av binary-filen til
  ESP-en. Endring av denne endrer tiden det tar å laste opp denne filen.
-
*/

#define PIN_BLINK_ (35)
#define BLINK_INTERVAL_MS_ (500)

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
            Serial.println("Hello World!");
        }

        digitalWrite(m_pin, HIGH);
    }
} blinker_{PIN_BLINK_};

void
setup()
{
    // put your setup code here, to run once:
    pinMode(PIN_BLINK_, OUTPUT);
    Serial.begin(9600);
}

void
loop()
{
    blinker_.blink();
}