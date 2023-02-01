
#include <Arduino.h>
#include <stdint.h>

#define READ_DEFAULT_INTERVAL_MS_ (1e3)
#define READ_ELEVATED_INTERVAL_MS_ (2e3)
#define BURST_INTERVAL_MS_ (100)
#define BUTTON_HOLD_MS_ (2e3)

#define READ_LIMIT_ (500)

enum fsm_state {
    BURST_5_,
    BURST_1_,
    READ_DEFAULT_,
    READ_BUTTON_,
    READ_ELEVATED_,
};

static struct fsm_ {
    uint8_t burst_count;
    uint8_t read_count;
    uint8_t burst_curmode;
    uint8_t led_pin;
    uint8_t read_pin;
    uint8_t button_pin;
    enum fsm_state state;

    uint64_t lastms; //, lastburst;
    uint16_t readbuf[10];
} fsm__ = {
    .burst_count = 0,
    .read_count = 0,
    .led_pin = LED_BUILTIN,
    .read_pin = A0,
    .button_pin = 2,
    .burst_curmode = 0,
    .state = READ_DEFAULT_,
    .lastms = 0,
    .readbuf = {0},
};

static uint16_t
avg_16_(uint16_t* mem, size_t size)
{
    uint16_t sum = 0;

    for (size_t i = 0; i < size; i++) {
        sum += mem[i];
    }

    return sum / ((uint16_t)size);
}

static void
transition_(struct fsm_* fsm, enum fsm_state new_state)
{
    switch (new_state) {
    case BURST_5_:
        fsm->burst_count = 5;
        break;
    case BURST_1_:
        fsm->burst_count = 1;
        break;
    case READ_ELEVATED_:
        fsm->read_count = 10;
        break;
    default:
        break;
    }

    fsm->state = new_state;
}

static void
tick_(struct fsm_* fsm)
{
    uint64_t tmp = millis();

    switch (fsm->state) {
    case BURST_5_:
    case BURST_1_:
        if (tmp - fsm->lastms < BURST_INTERVAL_MS_) {
            return;
        }

        if (!fsm->burst_count--) {
            transition_(fsm, READ_DEFAULT_);
        } else {
            digitalWrite(
                fsm->led_pin, fsm->burst_curmode = !fsm->burst_curmode
            );
        }

        break;
    case READ_ELEVATED_:
        if (tmp - fsm->lastms < READ_ELEVATED_INTERVAL_MS_) {
            return;
        }

        if (!--fsm->read_count) {
            transition(
                fsm,
                avg_16_(fsm->readbuf, 10) > READ_LIMIT_ ? BURST_5_ : BURST_1_
            );
        }

        break;
    case READ_DEFAULT_:
        if (tmp - fsm->lastms < READ_DEFAULT_INTERVAL_MS_) {
            return;
        }

        if (digitalRead(fsm->button_pin)) {
            transition_(fsm, READ_BUTTON_);
            break;
        }

        if (analogRead(fsm->read_pin) > READ_LIMIT_) {
            transition_(fsm, BURST_5_);
        } else {
            transition_(fsm, BURST_1_);
        }

        break;
    case READ_BUTTON_:
        if (!digitalRead(fsm->led_pin)) {
            transition_(fsm, READ_DEFAULT_);
            break;
        }

        if (tmp - fsm->lastms < BUTTON_HOLD_MS_) {
            return;
        }

        transition(fsm, READ_ELEVATED_);
        break;
    default:
        /* TODO: error */
        break;
    }

    fsm->lastms = tmp;
}

void
setup(void)
{
}

void
loop(void)
{
    tick_(&fsm__);
}