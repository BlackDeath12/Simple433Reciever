from machine import Pin
import time

rcv = Pin(13, Pin.IN, Pin.PULL_DOWN)
led = Pin(25, Pin.OUT)

while True:

    arrTime = [[],[]]
    
    arrInput = []
    MAX_DURATION = 100000 #1s in micro-seconds
    short_delay = 380 	#380us
    long_delay = 680	#680us
    lower_bound = 100
    upper_bound = 100
    message_size = 8
    total_time = MAX_DURATION

    if rcv.value():
        total_time = 0
        print("start recording \n")


    start_time = time.ticks_us()
    while total_time < MAX_DURATION:
            
        delta_time = time.ticks_diff(time.ticks_us(), start_time)
        arrTime[0].append(delta_time)
        arrTime[1].append(rcv.value())
        
        total_time = time.ticks_diff(time.ticks_us(), start_time)


    if total_time > MAX_DURATION:
        print("done recording \n")
        
    first = 0
    second = 0
    for i in range(len(arrTime[0])):
        
        if first == 0:
            if arrTime[1][i] == 1:
                first = i
                
        elif first != 0:
            if arrTime[1][i] == 1:
                second = i
                
        if first != 0 and second != 0:
            x = arrTime[0][second] - arrTime[0][first]
            if x <= short_delay + upper_bound and x >= short_delay - lower_bound:
                arrInput.append(1)
            elif x <= long_delay + upper_bound and x >= long_delay - lower_bound:
                arrInput.append(0)
            
            first = second
            second = 0
        
    if len(arrTime[0]) > 0:
        print(arrTime[0])
        print("\n")
        print(arrTime[1])
        print("\n")
        print(arrInput)
        
    if len(arrTime[0]) > 0:
        
        read_message = []
        expected = [0,1,1,0,1,0,1,0]
        for i in range(0, len(arrInput) - message_size):
            
            for j in range(i, i + message_size):
                read_message.append(arrInput[j])
            
            if len(read_message) == message_size:
                if read_message == expected:
                    print("message found!!!")
                    led.toggle()
                    break;
                read_message.clear()
            
        
            
