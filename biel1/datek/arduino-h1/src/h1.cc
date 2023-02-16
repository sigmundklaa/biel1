
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <Arduino.h>
#include <SPI.h>
#include <Wire.h>
#include <stdint.h>

#define PIN_INT1_ (2)
#define PIN_INT2_ (3)

#define PIN_MOTPIN1_ (8)
#define PIN_MOTPIN2_ (7)

#define SCREEN_WIDTH_ 128
#define SCREEN_HEIGHT_ 64
#define OLED_RESET_ -1
#define SCREEN_ADDRESS_ 0x3C

#define PIN_MOTENABLE_ (A3)

enum direction_ {
    RIGHT = 0,
    LEFT,
};

static class motor__
{
  public:
    volatile uint8_t m_state;
    enum direction_ m_dir;

    uint8_t m_dirpin1;
    uint8_t m_dirpin2;
    uint8_t m_enablepin;

    uint64_t m_time_total_ms;
    uint64_t m_time_tmp_ms;

  protected:
    uint8_t
    state_to_speed()
    {
        switch (m_state) {
        case 0:
            return 0;
        case 1:
            return 130;
        case 2:
            return 200;
        case 3:
            return 255;
        default:
            return 0;
        }
    }

    void
    reset_timer()
    {
        m_time_total_ms += millis() - m_time_tmp_ms;
    }

    void
    update_state(uint8_t new_state)
    {
        if (!m_state && new_state) {
            m_time_tmp_ms = millis();
        } else if (m_state && !new_state) {
            this->reset_timer();
        }

        m_state = new_state;
    }

  public:
    motor__(uint8_t motpin1, uint8_t motpin2, uint8_t enablepin)
        : m_dirpin1(motpin1), m_dirpin2(motpin2), m_enablepin(enablepin)
    {
    }

    void
    init()
    {
        pinMode(m_dirpin1, OUTPUT);
        pinMode(m_dirpin2, OUTPUT);
        pinMode(m_enablepin, OUTPUT);
    }

    void
    state_increase()
    {
        this->update_state(min(m_state + 1, 3));
    }

    void
    state_decrease()
    {
        this->update_state(max(m_state - 1, 0));
    }

    void
    write_speed(uint8_t speed)
    {
        digitalWrite(m_dirpin1, m_dir);
        digitalWrite(m_dirpin2, !m_dir);
        analogWrite(m_enablepin, speed);
    }

    void
    update_speed()
    {
        uint8_t speed = this->state_to_speed();
        this->write_speed(speed);
    }

} motor_(PIN_MOTPIN1_, PIN_MOTPIN2_, PIN_MOTENABLE_);

static Adafruit_SSD1306
    display(SCREEN_WIDTH_, SCREEN_HEIGHT_, &Wire, OLED_RESET_);

static void
speed_up_()
{
    motor_.state_increase();
    motor_.update_speed();
}

static void
speed_down_()
{
    motor_.state_decrease();
    motor_.update_speed();
}

static void
printdisp_(const String& str)
{
    display.clearDisplay();
    display.setCursor(0, 0);
    display.setTextColor(SSD1306_WHITE);
    display.setTextSize(3);
    display.println(str);
    display.display();
}

static void
setup_oled_()
{
    display.begin(SSD1306_SWITCHCAPVCC, SCREEN_ADDRESS_);
    display.display();
    delay(2000);
}

void
setup(void)
{
    Serial.begin(9600);

    pinMode(PIN_INT1_, INPUT_PULLUP);
    pinMode(PIN_INT2_, INPUT_PULLUP);

    attachInterrupt(digitalPinToInterrupt(PIN_INT1_), speed_up_, CHANGE);
    attachInterrupt(digitalPinToInterrupt(PIN_INT2_), speed_down_, CHANGE);

    motor_.init();
    setup_oled_();
}

void
loop(void)
{
#if 0
    Serial.print(digitalRead(PIN_INT1_));
    Serial.print(" ");
    Serial.println(motor_.m_state);
    Serial.print(" ");
    Serial.println(motor_.m_time_total_ms);
#endif

    printdisp_(
        String(motor_.m_state) + "   " +
        String(static_cast<int>(motor_.m_time_total_ms / 1e3))
    );
}