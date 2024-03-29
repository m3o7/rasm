// Adafruit Motor shield library
// copyright Adafruit Industries LLC, 2009
// this code is public domain, enjoy!

// Download @ https://github.com/adafruit/Adafruit-Motor-Shield-library
#include <AFMotor.h>

// Connect a stepper motor with 200 steps per revolution (1.8 degree)
// to motor port #2 (M1 and M2)
AF_Stepper motor1(200, 1);
// to motor port #2 (M3 and M4)
AF_Stepper motor2(200, 2);
char current;
String message = String("");

void setup() {
    // set up Serial library at [bits per second] 9600 bps / 8 bit = 1200 cps [characters per second]
    Serial.begin(9600);
    Serial.println("Booting");
    Serial.print("FORWARD: ");
    Serial.println(FORWARD);
    Serial.print("BACKWARD: ");
    Serial.println(BACKWARD);
    Serial.print("SINGLE: ");
    Serial.println(SINGLE);
    Serial.print("DOUBLE: ");
    Serial.println(DOUBLE);
    Serial.print("INTERLEAVE: ");
    Serial.println(INTERLEAVE);
    Serial.print("MICROSTEP: ");
    Serial.println(MICROSTEP);


    motor1.setSpeed(100);  // 10 rpm  
    motor2.setSpeed(100);  // 10 rpm
    motor1.step(50,FORWARD,1);
    motor2.step(50,FORWARD,1);

    // motor1.step(50,BACKWARD,1);
    // motor2.step(50,BACKWARD,1);

    // motor1.step(50,FORWARD,1);
    // motor2.step(50,FORWARD,1);

    // motor1.step(50,BACKWARD,1);
    // motor2.step(50,BACKWARD,1);

}

// convert arduino String to int
int __stringToInt__(String string){
  
  char char_string[string.length()+1];
  string.toCharArray(char_string, string.length()+1);
  
  return atoi(char_string);
}

int __getCommaCount__(String txt){
    int commas = 0;
    for (int i = 0; i < txt.length(); ++i){
        if (txt.charAt(i) == ',') commas++;
    }
    return commas;
}

void runMessage(String message){

    // check commas
    int cc = __getCommaCount__(message);
    // <motor>,<speed>,<steps>,<direction>,<style>
    if (cc != 4){
        Serial.println("invalid argument count! 5 arguments needed!");
        Serial.println("<motor>,<speed>,<steps>,<direction>,<style>");
    }

    // parse
    int current_index = 0;
    int values[cc+1];
    String current_num = String();
    for (int i = 0; i < message.length(); ++i){
        char current = message.charAt(i);
        if (current == ','){
            Serial.print(current_num);
            Serial.print(" - ");
            values[current_index++] = __stringToInt__(current_num);
            current_num = String();
        } else {
            // add to current number
            current_num = current_num + String(current);
        }
    }

    Serial.print(current_num);
    Serial.print(" - ");
    values[current_index++] = __stringToInt__(current_num);
    current_num = String();

    // motor
    AF_Stepper motor = (values[0] == 1) ? motor1 : motor2;

    // speed
    motor.setSpeed(values[1]);

    // step
    motor.step(values[2], values[3], values[4]);

}

void serialEvent(){
    current = Serial.read();

    if(current == ';'){
        // start processing
        message.trim();
        Serial.print("received: ");
        Serial.println(message);
        runMessage(message);
        Serial.println("done");
        message = String("");
    } else {
        // append
        message = message + String(current);
    }

    // error state
    if (message.length() > 100){
        message = String();
        Serial.println("Message is too big! Max buffer is 100 characters!");
    }


}

void loop() {
    // send data only when you receive data:
    // if (Serial.available() > 0) {
    //         // read the incoming byte:
            
    // }

    // music();
    // Serial.println("Single coil steps");
    // motor1.step(100, FORWARD, SINGLE); 
    // motor2.step(100, FORWARD, SINGLE); 
    // motor1.step(100, BACKWARD, SINGLE); 
    // motor2.step(100, BACKWARD, SINGLE); 

    // Serial.println("Double coil steps");
    // motor1.step(100, FORWARD, DOUBLE); 
    // motor1.step(100, BACKWARD, DOUBLE);
    // motor2.step(100, FORWARD, DOUBLE); 
    // motor2.step(100, BACKWARD, DOUBLE);

    // Serial.println("Interleave coil steps");
    // motor1.step(100, FORWARD, INTERLEAVE); 
    // motor1.step(100, BACKWARD, INTERLEAVE); 
    // motor2.step(100, FORWARD, INTERLEAVE); 
    // motor2.step(100, BACKWARD, INTERLEAVE); 

    // Serial.println("Micrsostep steps");
    // motor1.step(100, FORWARD, MICROSTEP); 
    // motor1.step(100, BACKWARD, MICROSTEP); 
    // motor2.step(100, FORWARD, MICROSTEP); 
    // motor2.step(100, BACKWARD, MICROSTEP); 
}

