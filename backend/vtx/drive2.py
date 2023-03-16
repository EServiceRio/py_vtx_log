from pymodbus.client.sync import ModbusSerialClient as ModbusSerial

radio = ModbusSerial(method="rtu", port="COM10", timeout=1, boudrate=19200)

radio.connect()

res = radio.read_holding_registers(33,1,unit=1).registers[0]

print(res)



