# Py Modbus


|Python TCP client/CLI for [Modbus TCP](https://www.simplymodbus.ca/TCP.htm)|
|-|
|![adu_pdu](https://github.com/joseph-gerald/py-tcp-modbus/assets/73967013/8453c242-effa-4b31-a63d-2c8ad6bade46)|
|![tcpip](https://github.com/joseph-gerald/py-tcp-modbus/assets/73967013/104529ac-7b15-4a99-9dc3-6f5dcea37801)|




## Example Usage of Modbus API
```py
from api.modbus import Modbus

modbus = Modbus("localhost", 502)
print("Sucesfully established connection!")

print("Reading coils from Slave #1 from index 0 -> 20 (0 + 20)")
coil_data = modbus.functions.read_coils(1, 0, 16).data
print("Coils:", coil_data)

print("Writing to coils #1 -> #100 to False/OFF")
modbus.functions.write_multiple_coils(1, 0, 100, [True]*100)
```

Look at all the functions python usage [here](https://github.com/joseph-gerald/py-tcp-modbus/blob/main/modbus/api/function_wrapper.py)

## CSV Runner *(runner.py)*
Run and schedule various commands simultaneously

### Example
```cs
# is_verbose,f_code:address:startup_delay_ms:poll_size:poll_frequency_ms:args...

1:15:1:0:-1:1000:0:8:[1,0,1,0,1,0,1,0]
1:15:1:500:-1:1000:0:8:[0,1,0,1,0,1,0,1]

0:1:1:0:-1:500:0:16
```
#### What this does:
1. The script will start by writing the first 8 coils to this configuration [1,0,1,0,1,0,1,0] and will be set to this every 1000ms
2. The script will print the current coils (last instruction is read before second due to the second having a 500ms startup delay)
3. The script will then wait 500 seconds before setting the coils to this configuration [0,1,0,1,0,1,0,1] and will be set to this every 1000ms
4. The script will log the coils again (every 500ms)
5. The 500ms offset from the first coil write will result in it alternating between the two configurations every 500ms

### Format (by order)

| Name | Description |
|-----|-----|
| Verbose | Whether to print the response to console (0 = print / 1 = do not print) |
| Function Code | Function Code to send ([view function codes](https://www.simplymodbus.ca/FC01.htm)) |
| Address | Slave address recipient |
| Delay | Time to wait from script startup to start polling |
| Poll Size | How many times to send command (-1 is infinite) |
| Poll Frequency | How often to send a poll (in milliseconds) |
| *Args | Arguments e.g. 1,1,1,0,-1,1000,**19,37** (example poll for [FC01](https://www.simplymodbus.ca/FC01.htm)) |

1. Write instructions to CSV
2. Run "python runner.py ***\**args***"
   - ***-ip*** or -ip_address to set destination IP / DEFAULT: 127.0.0.1
   - ***-port*** to define target port / DEFAULT: 502
   - ***-v*** to set verbose override (print all responses) / DEFAULT: FALSE

---
  
## CLI

### Examples
#### Read Coil Status ([FC01](https://www.simplymodbus.ca/FC01.htm))
```r
$ python main.py -a 1 -fc 1 -start 0 -size 1

[22:08:09] Slave Response: [True, True, False]

**Arguments

-a 1
  "Recipient slave address 1"

-fc 1
  "Function Code 1 (Read Coil Status)"

-start 0
  "Set coil read pointer to 0"

-size 3
  "Read the 3 consecutive coils"
```

#### Read Holding Registers ([FC03](https://www.simplymodbus.ca/FC03.htm))
```r
$ python main.py -a 1 -fc 3 -start 0 -size 16

[22:55:16] Slave Response: [100, 200, 400, 1000, 50, 125, 0, 1, 2, 3, 0, 0, 0, 0, 0, 0]

**Arguments

-a 1
  "Recipient slave address 1"

-fc 3
  "Function Code 3 (Read Holding Registers)"

-start 0
  "Set holding register read pointer to 0"

-size 16
  "Read the 16 consecutive holding register"
```

#### Force Single Coil ([FC05](https://www.simplymodbus.ca/FC05.htm))
```r
$ python main.py -a 1 -fc 5 -coil-address 5 -status 1

[22:21:46] Slave Response: Echoed Correctly? True / [5, 0, 5, 255, 0]

**Arguments

-a 1
  "Recipient slave address 1"

-fc 5
  "Function Code 5 (Write Single Coil)"

-coil-address 5
  "Coil to write to"

-status 1
  "Status to write 0/OFF or 1/ON"
```

#### Force Multiple Coils ([FC15](https://www.simplymodbus.ca/FC15.htm))
```r
$ python main.py -a 1 -fc 15 -start 3 -size 10 -values 1,1,1,1,1,0,0,0,0,0

[22:48:49] Slave Response: Write Size Correctly? True / [15, 0, 0, 0, 10]

**Arguments

-a 1
  "Recipient slave address 1"

-fc 15
  "Function Code 15 (Write Multiple Coils)"

-start 3
  "Start writing from coil #4 (3+1)"

-size
  "Write to the next 10 consecutive coils"

-values
  "The values to write the to the coils seperated by a comma (can also be True or False instead of 0s and 1s)"
```

#### Preset Multiple Registers ([FC16](https://www.simplymodbus.ca/FC16.htm))
```r
$ python main.py -a 1 -fc 16 -start 0 -size 10 -values 100,200,400,1000,50,125,0,1,2,3

[22:52:29] Slave Response: Write Size Correctly? True / [16, 0, 0, 0, 10]

**Arguments

-a 1
  "Recipient slave address 1"

-fc 16
  "Function Code 16 (Write Multiple Registers)"

-start 0
  "Start writing from the first coil / #1 (0+1)"

-size
  "Write to the next 10 consecutive coils"

-values
  "The values to write the to the coils seperated by a comma (i32)"
```



### Arguments
| Argument | Name | Description |
|-----|-----| ---- |
| -ip, -ip_address | IP | Destination IP address |
| -port | Port | Target port |
| -v, -verbose | Verbose | Whether to print response or no |
| | |
| | |
| -a, -address | Address | Slave Address |
| -fc, -code | Function Code | Function code to send |
| | |
| | |
| -n | Poll Size | Polling size (-1 is infinite) |
| -i, -interval | Poll Interval | Polling interval (in milliseconds) |
| | |
| | |
| -st, -start | Start | The Data Address of the initial index to read |
| -si, -size | Size | The total number of entries to read from initial index |
| | |
| | |
| -ca, -coil-address | Coil Address | The coil address for single coil writing ([FC05](https://www.simplymodbus.ca/FC05.htm)) |
| -s, -status | Status | The status (ON/OFF) status to write for ([FC05](https://www.simplymodbus.ca/FC05.htm)) |
| | |
| | |
| -ra, -register-address | Holding Register Address | The holding register address for single coil writing ([FC06](https://www.simplymodbus.ca/FC06.htm)) |
| -val, -value | Value | The value to write to a holding register ([FC06](https://www.simplymodbus.ca/FC06.htm)) |
| | |
| | |
| -vals, -values | Values | Values to write when writing to multiple addresses; seperated by a comma (,) |
