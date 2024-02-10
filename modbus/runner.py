import argparse
from api.modbus import Modbus
from api.generators import FunctionCode
from api.errors import MissingArgument
from api.utils import log, coerce_type

from threading import Thread

import time

parser = argparse.ArgumentParser(prog="Modbus CLI")
parser.add_argument("-ip", "-ip_address", type=str, dest="ip", default="127.0.0.1")
parser.add_argument("-port", type=int, dest="port", default="502")
parser.add_argument("-v", "-verbose", dest="verbose", type=bool, default=False)

args = parser.parse_args()

input_data = open("input.csv", "r").read()
log_verbose = args.verbose

modbus = Modbus(args.ip, args.port)
modbus.connect()

FUNCTIONS = {
    1: modbus.functions.read_coils,
    2: modbus.functions.read_discrete_inputs,
    3: modbus.functions.read_multiple_holding_registers,
    4: modbus.functions.read_input_registers,

    5: modbus.functions.write_single_coil,
    6: modbus.functions.write_single_holding_register,

    15: modbus.functions.write_multiple_coils,
    16: modbus.functions.write_multiple_holding_registers
}

def handle_line(line: str, worker_index: int):
    parts = line.split(":")
    VERBOSE_INSN = bool(int(parts.pop(0)))

    FUNCTION_CODE = FunctionCode(int(parts[0]))
    SLAVE_ADDRESS = int(parts[1])

    STARTUP_DELAY = int(parts[2])

    POLL_SIZE = int(parts[3])
    POLL_FREQUENCY = int(parts[4])

    # Leave only arguments left
    args = map(coerce_type, parts[5:])

    functions_args = [SLAVE_ADDRESS, *args]
    FUNCTION = FUNCTIONS[FUNCTION_CODE.value]

    index = 0

    time.sleep(STARTUP_DELAY/1000)

    while (POLL_SIZE >= index or POLL_SIZE == -1):
        res = FUNCTION(*functions_args)
        if (not VERBOSE_INSN or log_verbose): log(f"[Slave #{SLAVE_ADDRESS} / {FUNCTION_CODE.name} @ Worker-{worker_index}] {res.data}")

        time.sleep(POLL_FREQUENCY/1000)
        index += 1

index = 0

threads = []

for line in input_data.splitlines():
    if ("#" in line and line.index("#") == 0 or len(line) == 0):
        continue

    thread = Thread(target=handle_line, args=[line, index])
    threads.append(thread)

    thread.start()
    index += 1

for thread in threads:
    thread.join()
