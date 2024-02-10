from enum import Enum
import time
import json

# https://en.wikipedia.org/wiki/Modbus#Public_function_codes

class FunctionCode(Enum):
    ReadCoils = 1
    ReadDiscreteInputs = 2
    ReadMultipleHoldingRegisters = 3
    ReadInputRegisters = 4
    WriteSingleCoil = 5
    WriteSingleHoldingRegister = 6

    WriteMultipleCoils = 15
    WriteMultipleHoldingRegisters = 16

    ReadFileRecord = 20
    WriteFileRecord = 21
    MaskWriteRegister = 22
    ReadWriteMultipleHoldingRegisters = 23
    ReadFIFOQueue = 24

    ReadDeviceIdentification = 43

def bytify(input):
    return divmod(input, 256)
    
def flatten(xss):
    return [x for xs in xss for x in xs]

def chunkify(list, size):
    return [list[x:x+size] for x in range(0, len(list), size)]

def generate_mbap_header(length, transaction_id=0, protcol_id=0):
    # https://www.simplymodbus.ca/TCP.htm

    mbap = [
        *bytify(transaction_id),  # Split transaction id into 2 bytes
        *bytify(protcol_id),  # Split protocol id into 2 bytes
        *bytify(length)  # Split length into 2 bytes
    ]

    return mbap

def strip_mbap_header(bytes):
    # MBAP header is always 7 bytes
    # https://www.simplymodbus.ca/TCP.htm
    
    return bytes[7:]

def bitify(n):
    return "".join(reversed(list('{0:08b}'.format(n))))

def unbitify(byte_arr: list):
    index = 1
    total = 0

    for byte in byte_arr:
        total += int(byte) * 256 ** (len(byte_arr) - index)
        index += 1

    return total

def log(text):
    print(time.strftime("[%H:%M:%S] " + text))

def coerce_type(input):
    if (input == None): return None

    if (type(input) is str):
        if (input.isdigit()):
            return int(input)
        
        if (input.lower() in ["true", "false"]):
            return bool(input)
        
        try:
            return json.loads(input)
        except:
            pass
            

        return input

