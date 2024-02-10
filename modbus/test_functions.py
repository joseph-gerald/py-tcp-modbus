from api.modbus import Modbus
import unittest

modbus = Modbus("localhost", 502)

class TestModbus(unittest.TestCase):
    def test_connection(self):
        print("Establishing connection with Modbus...")
        modbus.connect()
        print("Sucesfully established connection!")

    def test_read_write_coils(self):
        print("\nReading coils from Slave #1 from index 0 -> 20 (0 + 20)")
        coil_data = modbus.functions.read_coils(1, 0, 16).data
        
        print("\nCoils:", coil_data)
    
        print("\nWriting to coil #1 on Slave #1 to True")
        res = modbus.functions.write_single_coil(1, 0, True)

        print("\nWriting to coil #3 on Slave #1 to True")
        res = modbus.functions.write_single_coil(1, 2, True)

        print("\nWriting to coils #9, #10, #12 on Slave #1 to True")
        res = modbus.functions.write_multiple_coils(1, 8, 4, [
            True,
            True,
            False,
            True
        ])

        print("\nReading coils from Slave #1 from index 0 -> 20 (0 + 20)")
        print("Expecting for coils # 1, 3, 9, 10, 12 to be True")
        
        coil_data = modbus.functions.read_coils(1, 0, 16).data
        
        print("\nCoils:", coil_data)

        self.assertTrue(coil_data[0])
        self.assertTrue(coil_data[2])
        self.assertTrue(coil_data[8])
        self.assertTrue(coil_data[9])
        self.assertTrue(coil_data[1])

        print("Coils were as expected!")

    def test_read_input_registers(self):
        print("\nAttemping to Read Input Registers:")
        res = modbus.functions.read_input_registers(1, 4, 21)

        print("\nInput Registers:", res.data)
    
    def test_set_coils_to_zero(self):
        print("\nWriting to coils #1 -> #100 to False/OFF")
        res = modbus.functions.write_multiple_coils(1, 0, 100, [True]*100)

    def test_read_write_holding_registers(self):
        print("\nWriting to holding registers #1 -> #4 to [100, 200, 300, 500]")

        modbus.functions.write_multiple_holding_registers(1, 0, 4, [
            100,
            200,
            300,
            500
        ])

        print("Reading holding registers #1 -> #8")

        res = modbus.functions.read_multiple_holding_registers(1, 0,8)

        print(res.data)

if __name__ == '__main__':
    unittest.main(exit=False)

