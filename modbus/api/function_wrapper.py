from .parsers import *
from .utils import *

import time

class Functions:
    def __init__(self, modbus):
        self.modbus = modbus

    def read_coils(self, address: int, start: int, size: int) -> GenericBinaryRead:
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

        return GenericBinaryRead(time.time(), self.modbus.pass_function(FunctionCode.ReadCoils, address=address, start=start, size=size)[0], size)

    def read_discrete_inputs(self, address: int, start: int, size: int) -> GenericBinaryRead:
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

        return GenericBinaryRead(time.time(), self.modbus.pass_function(FunctionCode.ReadDiscreteInputs, address=address, start=start, size=size)[0], size)
    
    def read_multiple_holding_registers(self, address: int, start: int, size: int) -> GenericByteRead:
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

        return GenericByteRead(time.time(), self.modbus.pass_function(FunctionCode.ReadMultipleHoldingRegisters, address=address, start=start, size=size)[0], size)

    def read_input_registers(self, address: int, start: int, size: int) -> GenericByteRead:
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

        return GenericByteRead(time.time(), self.modbus.pass_function(FunctionCode.ReadInputRegisters, address=address, start=start, size=size)[0], size)

    def write_single_coil(self, address: int, coil_address: int, status: bool):
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

        return GenericEcho(time.time(), self.modbus.pass_function(FunctionCode.WriteSingleCoil, address=address, coil_address=coil_address, status=status))

    def write_single_holding_register(self, address: int, register_address: int, value: int):
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

        return GenericEcho(time.time(), self.modbus.pass_function(FunctionCode.WriteSingleHoldingRegister, address=address, register_address=register_address, value=value))

    def write_multiple_coils(self, address: int, start: int, size: int, values: list):
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

        return GenericWriteSize(time.time(), self.modbus.pass_function(FunctionCode.WriteMultipleCoils, address=address, start=start, size=size, values=values))

    def write_multiple_holding_registers(self, address: int, start: int, size: int, values: list):   
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

        return GenericWriteSize(time.time(), self.modbus.pass_function(FunctionCode.WriteMultipleHoldingRegisters, address=address, start=start, size=size, values=values))