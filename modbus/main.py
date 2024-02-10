import argparse
from api.modbus import Modbus
from api.generators import FunctionCode
from api.errors import MissingArgument
from api.utils import log, coerce_type

import time

parser = argparse.ArgumentParser(prog="Modbus CLI")
parser.add_argument("-ip", "-ip_address", type=str, dest="ip", default="127.0.0.1")
parser.add_argument("-port", type=int, dest="port", default="502")

parser.add_argument("-a", "-address", type=int, dest="address", required=True)
parser.add_argument("-fc", "-code", type=int, dest="function_code", required=True)
parser.add_argument("-n", dest="poll_size", type=int, default=1)
parser.add_argument("-i", "-interval", dest="polling_interval", type=int, default=0)
parser.add_argument("-v", "-verbose", dest="verbose", type=bool, default=False)

# Read functions
parser.add_argument("-st", "-start", type=int, dest="start")
parser.add_argument("-si", "-size", type=int, dest="size")

# Write fucntions
parser.add_argument("-ca", "-coil-address", type=int, dest="coil_address")
parser.add_argument("-ra", "-register-address", type=int, dest="register_address")

parser.add_argument("-s", "-status", type=int, dest="status")

parser.add_argument("-vals", "-values", type=str, dest="values_string")
parser.add_argument("-val", "-value", type=str, dest="value_string")

args = parser.parse_args()

ARG_MAP = {
    "address": args.address,
    "start": args.start,
    "size": args.size,
    "value": coerce_type(args.value_string),
    "values": None if args.values_string == None else list(map(coerce_type, args.values_string.split(","))),
    "coil_address": args.coil_address,
    "register_address": args.register_address,
    "status": bool(args.status)
}

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

index = 0
poll_size = args.poll_size
verbose = args.verbose
fc = args.function_code

function_code = FunctionCode(fc)

if fc not in FUNCTIONS: exit(print(f"Function code ({fc}:{function_code}) not implemented"))
    
function = FUNCTIONS[function_code.value] 

function_arguments_identifiers = function.__code__.co_varnames[1:]
function_arguments = list(map(lambda arg: ARG_MAP[arg], function_arguments_identifiers))

print(
    "\n",
    f"Function Code {fc}: {function_code.name}",
    "\n"
)

# Check for missing arguments
for identifier, value in zip(function_arguments_identifiers, function_arguments):
    if (value == None): raise MissingArgument(f"{identifier} was not present in arguments")

while (poll_size > index or poll_size == -1):
    res = function(*function_arguments)
    log("Slave Response: " + str(res.data))

    index += 1

    time.sleep(args.polling_interval / 1000)