RUN = __name__ == "__main__"

import time
from struct import unpack

if RUN:
    from errors import *
    from utils import *
else:
    from .utils import *
    from .errors import *

# implemented from
# https://www.simplymodbus.ca/FAQ.htm
# https://www.simplymodbus.ca/TCP.htm


class MBAPHeader:
    """
      0001 0000 0006 11 03 006B 0003

    0001: Transaction Identifier
    0000: Protocol Identifier
    0006: Message Length (6 bytes to follow)
    11: The Unit Identifier  (17 = 11 hex)
    03: The Function Code (read Analog Output Holding Registers)
    006B: The Data Address of the first register requested. (40108-40001 = 107 =6B hex)
    0003: The total number of registers requested. (read 3 registers 40108 to 40110)
    """

    def __init__(self, data):
        self.transaction_id = 0
        self.protocol_id = 0
        self.length = 0

        # UnitID / SlaveID
        self.address = 0


class GenericBinaryRead:
    """
    > Handles responses for Function Codes 1 & 2

    11 01 05 CD6BB20E1B 45E6

    11: The Slave Address (11 hex = address17 )
    01: The Function Code 1 (read Coil Status)
    05: The number of data bytes to follow (37 Coils / 8 bits per byte = 5 bytes)
    CD: Coils 27 - 20 (1100 1101)
    6B: Coils 35 - 28 (0110 1011)
    B2: Coils 43 - 36 (1011 0010)
    0E: Coils 51 - 44 (0000 1110)
    1B: 3 space holders & Coils 56 - 52 (0001 1011)

    The more significant bits contain the higher coil variables. This shows that coil 36 is off (0) and 43 is on (1). Due to the number of coils requested, the last data field1B contains the status of only 5 coils.  The three most significant bits in this data field are filled in with zeroes.
    """

    def __init__(self, start: int, bytes: bytes, size: int):
        self.start_time = start
        self.end_time = time.time()

        self.response_time = start - self.end_time

        response = unpack("%sB" % len(bytes), bytes)
        response = strip_mbap_header(response)

        self.function_code = response[0]

        self.data_bytes_size = response[1]
        self.data_bytes = response[2:]

        byte_arr = list(map(lambda byte: bitify(byte), self.data_bytes))
        
        self.data = "".join(byte_arr)

        self.data = self.data[:size]

        self.data = list(map(lambda bit: bool(int(bit)), self.data))


class GenericByteRead:
    """
    > Handles responses for Function Codes 3 & 4

    11 03 06 AE41 5652 4340

    11: The Slave Address (11 hex = address17 )
    03: The Function Code 3 (read Analog Output Holding Registers)
    06: The number of data bytes to follow (3 registers x 2 bytes each = 6 bytes)
    AE41: The contents of register 40108
    5652: The contents of register 40109
    4340: The contents of register 40110
    """

    def __init__(self, start: int, bytes: bytes, size: int):
        self.start_time = start
        self.end_time = time.time()

        self.response_time = start - self.end_time

        response = unpack("%sB" % len(bytes), bytes)
        response = strip_mbap_header(response)

        self.function_code = response[0]

        self.data_bytes_size = response[1]
        self.data_bytes = response[2:]

        self.data = list(map(unbitify, chunkify(self.data_bytes, 2)))

class GenericEcho:
    def __init__(self, start: int, data: tuple):
        self.start_time = start
        self.end_time = time.time()

        self.response_time = start - self.end_time

        response_bytes = data[0]
    
        response = unpack("%sB" % len(response_bytes), response_bytes)
        response = list(strip_mbap_header(response))
        request = strip_mbap_header(data[1])

        self.data = f"Echoed Correctly? {response == request} / {request}"

class GenericWriteSize:
    def __init__(self, start: int, data: tuple):
        self.start_time = start
        self.end_time = time.time()

        self.response_time = start - self.end_time

        response_bytes = data[0]
    
        response = unpack("%sB" % len(response_bytes), response_bytes)
        response = list(strip_mbap_header(response))
        request = strip_mbap_header(data[1])
        request = request[0:len(response)]

        self.data = f"Write Size Correctly? {response == request} / {request}"