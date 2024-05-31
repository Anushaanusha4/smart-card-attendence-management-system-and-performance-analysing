import serial
import time

data = serial.Serial(
                  'COM3',
                  baudrate = 9600,
                  parity=serial.PARITY_NONE,
                  stopbits=serial.STOPBITS_ONE,
                  bytesize=serial.EIGHTBITS,                  
                  timeout=1
                  )

def read_data():
  datas = []
  for i in range(1, 11):
      d = data.read(12)
      d = d.decode('UTF-8', 'ignore')
      d = d.strip()
      print(d)
      if len(d) == 12:
        datas.append(d)
      time.sleep(1)
  return datas


def read_data1():
  while True:
      d = data.read(12)
      d = d.decode('UTF-8', 'ignore')
      d = d.strip()
      print(d)
      if len(d) == 12:
        break
      time.sleep(1)
  return d
