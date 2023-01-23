
#include <Arduino.h>
#include <stdint.h>

#define BLINK_TIME_MS_ (500)

enum pinout {
    BTN_1 = 2,
    BTN_2,
    BTN_3,
    BTN_4,
    BTN_5,
    BTN_MAX_,

    LED_1 = 7,
    LED_2,
    LED_3,
    LED_4,
    LED_5,
    LED_6,
    LED_7,
    LED_MAX_,
};

static void
a_tick(void)
{
    digitalWrite(LED_1, digitalRead(BTN_1));
}

static void
b_tick(void)
{
    digitalWrite(LED_2, !digitalRead(BTN_2));
}

static void
c_tick(void)
{
    static uint8_t mode = 0;
    static int64_t ms = 0;

    int64_t tmp = millis();

    if (digitalRead(BTN_3) && (tmp - ms) >= BLINK_TIME_MS_) {
        ms = tmp;
        digitalWrite(LED_3, mode = !mode);
        return;
    }

    digitalWrite(LED_3, HIGH);
}

/* d and e combined */
static void
de_tick(void)
{
    static uint8_t mode = 0, btn_state = 2;
    static int64_t ms = 0;

    uint8_t read = digitalRead(BTN_4);

    if (digitalRead(BTN_5)) {
        mode = 0;
        btn_state = 2;
        ms = 0;
    }

    switch (btn_state) {
    case 2:
        if (!read) {
            digitalWrite(LED_4, HIGH);
            return;
        }
        btn_state--;
    case 1: {

        if (!read) {
            btn_state--;
            break;
        }

        int64_t tmp = millis();
        if (tmp - ms > BLINK_TIME_MS_) {
            ms = tmp;
            digitalWrite(LED_4, mode = !mode);
            return;
        }

        return;
    }
    default:
        break;
    }

    digitalWrite(LED_4, LOW);
}

static void
f_tick(void)
{
    static uint8_t led_states[] = {0, 0, 0};

    uint8_t index = 0;

    String tmp = Serial.readString();
    tmp.trim();

    if (!tmp) {
        return;
    }

    switch (tmp[0]) {
    case 'R':
        break;
    case 'G':
        index = 1;
        break;
    case 'B':
        index = 2;
        break;
    default:
        Serial.println('Invalid character');
        return;
    }

    led_states[index] = !led_states[index];

    for (uint8_t i = 0; i < sizeof(led_states) / sizeof(*led_states); i++) {
        digitalWrite(LED_5 + index, led_states[index]);
    }
}

void
setup(void)
{
    for (uint8_t i = BTN_1; i < BTN_MAX_; i++) {
        pinMode(i, INPUT);
    }

    for (uint8_t i = LED_1; i < LED_MAX_; i++) {
        pinMode(i, OUTPUT);
    }

    Serial.begin(9600);
}

void
loop(void)
{
    a_tick();
    b_tick();
    c_tick();
    de_tick();
    f_tick();
}
