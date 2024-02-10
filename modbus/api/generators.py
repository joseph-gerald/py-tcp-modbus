RUN = __name__ == "__main__"

import math

if RUN:
    from errors import *
    from utils import *
else:
    from .utils import *
    from .errors import *

# implemented from
# https://www.simplymodbus.ca/FAQ.htm
# https://www.simplymodbus.ca/TCP.htm

def read_coils(kwargs):
    """
    This command is requesting the ON/OFF status of discrete coils # 20 to 56
    from the slave device with address 17.
    11 01 0013 0025

    11: The Slave Address (11 hex = address17 )
    01: The Function Code 1 (read Coil Status)
    0013: The Data Address of the first coil to read.
                ( 0013 hex = 19 , + 1 offset = coil #20 )
    0025: The total number of coils requested.  (25 hex = 37,  inputs 20 to 56 )
    """

    return [
        kwargs["address"],  # The Slave Address
        FunctionCode.ReadCoils.value,  # The Function Code
        *bytify(kwargs["start"]),  # Index of coil to start reading from
        *bytify(kwargs["size"]),  # How many coils to read
    ]


def read_discrete_inputs(kwargs):
    """
    This command is requesting the ON/OFF status of discrete inputs # 10197 to 10218
    from the slave device with address 17.

    11 02 00C4 0016

    11: The Slave Address (11 hex = address17 )
    02: The Function Code 2 (read Input Status)
    00C4: The Data Address of the first input to read.
                 ( 00C4 hex = 196 , + 10001 offset = input #10197 )
    0016: The total number of coils requested. (16 hex = 22,  inputs 10197 to 10218 )
    """

    return [
        kwargs["address"],
        FunctionCode.ReadDiscreteInputs.value,
        *bytify(kwargs["start"]),  # Index of input to start reading from
        *bytify(kwargs["size"]),  # How many inputs to read
    ]


def read_multiple_holding_registers(kwargs):
    """
    This command is requesting the content of analog output holding registers # 40108 to
     40110 from the slave device with address 17.

    11 03 006B 0003

    11: The Slave Address (11 hex = address17 )
    03: The Function Code 3 (read Analog Output Holding Registers)
    006B: The Data Address of the first register requested.
                 ( 006B hex = 107 , + 40001 offset = input #40108 )
    0003: The total number of registers requested. (read 3 registers 40108 to 40110)
    """

    return [
        kwargs["address"],
        FunctionCode.ReadMultipleHoldingRegisters.value,
        *bytify(kwargs["start"]),  # Index of register to start reading from
        *bytify(kwargs["size"]),  # How many registers to read
    ]


def read_input_registers(kwargs):
    """
    This command is requesting the content of analog input register # 30009
    from the slave device with address 17.

    11 04 0008 0001

    11: The Slave Address (11 hex = address17 )
    04: The Function Code 4 (read Analog Input Registers)
    0008: The Data Address of the first register requested.
                 ( 0008 hex = 8 , + 30001 offset = input register #30009 )
    0001: The total number of registers requested. (read 1 register)
    """

    return [
        kwargs["address"],
        FunctionCode.ReadInputRegisters.value,
        *bytify(kwargs["start"]),  # Index of register to start reading from
        *bytify(kwargs["size"]),  # How many registers to read
    ]


def write_single_coil(kwargs):
    """
    This command is writing the contents of discrete coil # 173 to ON
    in the slave device with address 17.

    11 05 00AC FF00

    11: The Slave Address (11 hex = address17 )
    05: The Function Code 5 (Force Single Coil)
    00AC: The Data Address of the coil. (coil# 173 - 1 = 172 = AC hex).
                 ( 00AC hex = 172 , + 1 offset = coil #173 )
    FF00: The status to write ( FF00 = ON,  0000 = OFF )
    """

    hex_status = 0xFF00 if kwargs["status"] else 0x0000
    address = kwargs["coil_address"]

    return [
        kwargs["address"],
        FunctionCode.WriteSingleCoil.value,
        *bytify(address),  # Coil address to write to
        *bytify(hex_status),  # Coil status to write
    ]


def write_single_holding_register(kwargs):
    """
    This command is writing the contents of analog output holding register # 40002
    to the slave device with address 17.

    11 06 0001 0003

    11: The Slave Address (11 hex = address17 )
    06: The Function Code 6 (Preset Single Register)
    0001: The Data Address of the register.
                 ( 0001 hex = 1 , + 40001 offset = register #40002 )
    0003: The value to write
    """

    return [
        kwargs["address"],
        FunctionCode.WriteSingleHoldingRegister.value,
        *bytify(kwargs["register_address"]),  # Data address to write to
        *bytify(kwargs["value"]),  # Value to write
    ]


def write_multiple_coils(kwargs):
    """
    This command is writing the contents of a series of 10 discrete coils from #20 to #29
    to the slave device with address 17.

    11 0F 0013 000A 02 CD01

    11: The Slave Address (11 hex = address17 )
    0F: The Function Code 15 (Force Multiple Coils, 0F hex  = 15 )
    0013: The Data Address of the first coil.
                 ( 0013 hex = 19 , + 1 offset = coil #20 )
    000A: The number of coils to write ( 0A hex  = 10 )
    02: The number of data bytes to follow (10 Coils / 8 bits per byte = 2 bytes)
    CD: Coils 27 - 20 (1100 1101)
    01: 6 space holders & Coils 29 - 28 (0000 0001)

    The more significant bits contain the higher coil variables. This shows that coil 20 is on (1) and 21 is off (0). Due to the number of coils requested, the last data field01 contains the status of only 2 coils.  The unused bits in the last data byte are filled in with zeroes.
    """

    if (len(kwargs["values"]) != kwargs["size"]): raise UnexpectedInputSize(f"Expected {kwargs['size']} values but received {len(kwargs['values'])}")

    # True + 0 = 1, False + 0 = 0, coerce from bool to int
    BIT_ARRAYS = list(map(lambda x: x + 0, kwargs["values"]))
    CHUNKS = list(map(lambda chunk: chunk[::-1], chunkify(BIT_ARRAYS, 8)))

    while (len(CHUNKS[-1]) % 8 != 0):
        CHUNKS[-1].insert(0, 0)

    BYTES = []

    for CHUNK in CHUNKS:
        STR_CHUNK = "".join(list(map(lambda bit: str(bit), CHUNK)))
        BYTES.append(int(STR_CHUNK, 2))

    return [
        kwargs["address"],
        FunctionCode.WriteMultipleCoils.value,
        *bytify(kwargs["start"]),
        *bytify(kwargs["size"]),
        math.ceil((kwargs["size"])/8),
        *BYTES
    ]


def write_multiple_holding_registers(kwargs):
    """
    This command is writing the contents of two analog output holding registers # 40002 & 40003 to the slave device with address 17.

    11 10 0001 0002 04 000A 0102

    11: The Slave Address (11 hex = address17 )
    10: The Function Code 16 (Preset Multiple Registers, 10 hex - 16 )
    0001: The Data Address of the first register.
                ( 0001 hex = 1 , + 40001 offset = register #40002 )
    0002: The number of registers to write
    04: The number of data bytes to follow (2 registers x 2 bytes each = 4 bytes)
    000A: The value to write to register 40002
    0102: The value to write to register 40003
    """

    if (len(kwargs["values"]) != kwargs["size"]): raise UnexpectedInputSize(f"Expected {kwargs['size']} values but received {len(kwargs['values'])}")

    return [
        kwargs["address"],
        FunctionCode.WriteMultipleHoldingRegisters.value,
        *bytify(kwargs["start"]),
        *bytify(kwargs["size"]),
        kwargs["size"] * 2,
        *flatten(map(bytify, kwargs["values"]))
    ]


def read_file_record():
    pass


def write_file_record():
    pass


def mask_write_register():
    pass


def read_write_multiple_holding_registers():
    pass


def read_fifo_queue():
    pass


def read_device_identification():
    pass

if RUN:
    pass