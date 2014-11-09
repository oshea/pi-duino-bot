import serial
import re

def parse_packet(p):
  p = p.strip()
  if re.match(r'\$.*!', p):
    # Data packet

    # Remove start/end chars
    p = p[1:-1]
    attrs = p.split(",")

    values = {}

    for a in attrs:
      attr_parts = a.split("=")
      values[attr_parts[0]] = attr_parts[1]

    return values

  else:
    print "Discarding packet: %s" % p
    return None

class SensorDevice:
  def __init__(self):
    self.id = "magnometer"
    self.has_sensors = True
    self.serial_number = None

  def read(self):
    #return { 'x': 0, 'y': 0, 'z': 0, 'timestamp': None }
    packet = self.serial.readline()
    return parse_packet(packet)


  def load(self):
    tty_path = "/dev/tty.usbserial-%s" % self.serial_number
    print "device path %s" % tty_path
    self.serial = serial.Serial(tty_path, 9600)

  def cleanup(self):
    print "Closing %s serial connection" % self.serial_number
    self.serial.close()
