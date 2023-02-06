
#include <Arduino.h>
#include <Servo.h>
#include <stdint.h>

#define SWIPE_DELAY_MS_ (1000)

static struct servo {
    uint8_t start_default, end_default;
    uint8_t pinout;
    int64_t last_write_ms;

    struct swipe_ {
        uint8_t start, end;
        uint8_t nswipes;
        uint8_t swiping;
        uint8_t at_end;
    } swipe;

    Servo srv_instance;
} servo__ = {
    .start_default = 0,
    .end_default = 180,
    .pinout = 3,
    .last_write_ms = 0,
    .swipe = {0},
};

static int
srv_set_swipe(struct servo* srv, uint8_t start, uint8_t end, uint8_t nswipes)
{
    if (start > 180 || end > 180) {
        return 1;
    }

    srv->swipe = (struct servo::swipe_){
        .start = start,
        .end = end,
        .nswipes = nswipes,
        .swiping = 1,
        .at_end = 0,
    };

    return 0;
}

static void
srv_swipe(struct servo* srv)
{
    if (!srv->swipe.at_end && !srv->swipe.nswipes--) {
        srv->swipe = {0};
        return;
    }

    srv->srv_instance.write(
        srv->swipe.at_end ? srv->swipe.start : srv->swipe.end
    );
    srv->swipe.at_end = !srv->swipe.at_end;
}

static void
srv_init(struct servo* srv)
{
    srv->srv_instance.attach(srv->pinout);
}

static void
srv_tick(struct servo* srv)
{
    if (!srv->swipe.swiping) {
        return;
    }

    int64_t tmp = millis();

    if (tmp - srv->last_write_ms >= SWIPE_DELAY_MS_) {
        srv_swipe(srv);
        srv->last_write_ms = tmp;
    }
}

static void
srv_toggle(struct servo* srv)
{
    srv->swipe.swiping = !srv->swipe.swiping;
}

static void
srv_clear(struct servo* srv)
{
    srv->swipe = {0};
}

static void
srv_goto(struct servo* srv, uint8_t ang)
{
    if (ang > 180) {
        return;
    }

    srv->srv_instance.write(ang);
}

/**
 * @brief Processes the string @p str recieved from serial
 *
 * Message format:
 * 1 - Swipe 0 - 180 one time
 * 2 - Toggle continued swiping
 * 3 [ANGLE] - Goto angle
 * 4 [START] [END] [NSWIPES] - Swipe from START to END NSWIPES times. Each
 * argument must be specified with exactly 3 digits
 *
 * @param str
 */
static void
process(String str)
{
    enum command {
        SWIPE_ONE = 1,
        TOGGLE_SWIPE,
        GOTO_ANG,
        SWIPE_MANY,
    };

    switch (str.toInt()) {
    case SWIPE_ONE:
        srv_set_swipe(&servo__, 0, 180, 1);
        Serial.println("swiping 0-180");
        break;
    case TOGGLE_SWIPE:
        Serial.println("toggling swipe");
        srv_toggle(&servo__);
        break;
    case GOTO_ANG:
        Serial.println("going to");
        srv_clear(&servo__);
        srv_goto(&servo__, str.substring(2, str.length()).toInt());
        break;
    case SWIPE_MANY:
        /* I am FAR too lazy to parse this properly */
        Serial.println("swiping custom");
        srv_set_swipe(
            &servo__, str.substring(2, 5).toInt(), str.substring(6, 9).toInt(),
            str.substring(10, 13).toInt()
        );
        break;
    default:
        break;
    }
}

void
setup()
{
    srv_init(&servo__);
    srv_set_swipe(&servo__, 45, 145, 10);

    Serial.begin(9600);
    Serial.println("Serial initialized");

    pinMode(LED_BUILTIN, OUTPUT);
}

void
loop()
{
    srv_tick(&servo__);

    if (Serial.available()) {
        String s = Serial.readString();
        Serial.print("echo: ");
        Serial.println(s);

        process(s);
    }
}