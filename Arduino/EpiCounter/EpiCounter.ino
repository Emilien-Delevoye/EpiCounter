const byte TRIGGER_PIN_A = 2;
const byte TRIGGER_PIN_B = 12;

const byte ECHO_PIN_A = 3;
const byte ECHO_PIN_B = 13;

const unsigned long MEASURE_TIMEOUT = 25000UL;

const float SOUND_SPEED = 340.0 / 1000;

unsigned long previous_a = 0;
unsigned long previous_b = 0;
bool previous_state_a = false;
bool previous_state_b = false;

void setup() {
    Serial.begin(9600);

    pinMode(TRIGGER_PIN_A, OUTPUT);
    pinMode(TRIGGER_PIN_B, OUTPUT);
    digitalWrite(TRIGGER_PIN_A, LOW);
    digitalWrite(TRIGGER_PIN_B, LOW);
    pinMode(ECHO_PIN_A, INPUT);
    pinMode(ECHO_PIN_B, INPUT);
    pinMode(4, OUTPUT);
    pinMode(11, OUTPUT);
    pinMode(5, OUTPUT);
    pinMode(10, OUTPUT);
}

float calc_distance(const byte trigger, const byte echo)
{
    long measure = 0;
    float distance_mm = 0;

    digitalWrite(trigger, HIGH);
    delayMicroseconds(10);
    digitalWrite(trigger, LOW);

    measure = pulseIn(echo, HIGH, MEASURE_TIMEOUT);
    distance_mm = measure / 2.0 * SOUND_SPEED;
    delay(20);
    return (distance_mm / 10.0);
}

void serial_print(float distance_mm_a, float distance_mm_b)
{
    Serial.print("Distance A : ");
    Serial.print(distance_mm_a, 2);
    Serial.println(" cm.");
    Serial.print("Distance B : ");
    Serial.print(distance_mm_b, 2);
    Serial.println(" cm.");
    Serial.println("=============================================");
}

void loop() {
    const unsigned long current_time = millis();
    float distance_cm_a = calc_distance(TRIGGER_PIN_A, ECHO_PIN_A);
    float distance_cm_b = calc_distance(TRIGGER_PIN_B, ECHO_PIN_B);
    static byte pos = 0;
    static int nb = 10;

    if (distance_cm_a < 100 /*&& previous_state_a == false*/) {
        digitalWrite(4, HIGH);
        previous_a = current_time;
        previous_state_a = true;
    } else if (current_time - previous_a > 600) {
        previous_state_a = false;
        previous_a = 0;
        digitalWrite(4, LOW);
    }
    if (distance_cm_b < 100 /*&& previous_state_b == false*/) {
        digitalWrite(11, HIGH);
        previous_b = current_time;
        previous_state_b = true;
    } else if (current_time - previous_b > 600) {
        previous_state_b = false;
        previous_b = 0;
        digitalWrite(11, LOW);
    }

    //==============================================\\

    if (previous_state_a && previous_state_b) {
        if (previous_a < previous_b && pos != 1) {
            digitalWrite(5, HIGH);
            digitalWrite(10, LOW);
            pos = 1;
            nb += 1;
            Serial.println(nb);
        } else if (previous_a > previous_b && pos != 2) {
            digitalWrite(10, HIGH);
            digitalWrite(5, LOW);
            pos = 2;
            nb -= 1;
            Serial.println(nb);
        }
    } else {
        pos = 0;
    }
}
