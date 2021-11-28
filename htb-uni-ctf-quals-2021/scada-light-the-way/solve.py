from pymodbus.client.sync import ModbusTcpClient
import time

client = ModbusTcpClient('10.129.227.149')
junction = 6

res = client.write_registers(0,[ord(x) for x in "auto_mode:false\x00\x00"],unit=junction)

#res = client.write_registers(0,[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],unit=1)

for i,j in enumerate("001001001100"):
 client.write_coil(886+i,int(j),unit=junction)

#for i in range(880,890):
# print(i)
# client.write_coil(i,1,unit=junction)
# time.sleep(5)

hold_reg = client.read_holding_registers(0,99,unit=junction)
print("Holding Register:",''.join([chr(x) for x in (hold_reg.registers)]))
print(hold_reg.registers)

input_reg = client.read_input_registers(0,99,unit=junction)
print("Input Register:",input_reg.registers)

discrete_inputs = client.read_discrete_inputs(0,99,unit=junction)
print("Discrete Input:",discrete_inputs.bits)

coils = client.read_coils(0,100,unit=junction)
print("Coils:",[int(x) for x in coils.bits])


client.close()


#Junction 1 starts at coil 571     we want 001001001100
#Junction 2 starts at coil 1920 we want 100001001001
#Junction 4 starts at coil 1266 we want 001001001100
#Junction 6 starts at coil 886    we want 001001001100
