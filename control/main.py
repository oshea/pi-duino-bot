import serial
import logging
import json
import atexit
import time
import os
import json

import devices
from web import start_web_app

def run():
  # Create session id using linux timestamp
  session_id = int(time.time())

  # Create session directory
  session_dir = "../sessions/%s" % session_id
  print "Session directory: %s" % session_dir

  if not os.path.exists(session_dir):
    os.makedirs(session_dir)

  # Create log file
  log_path = session_dir + "/events.log"
  log = open(log_path, 'a')

  config = ConfigManager()
  config.load()

  devices = DeviceManager(config)
  devices.load()

  brain = Brain(config)
  brain.load()

  # Setup handler for cleanup on script exit
  def exit_handler():
    print "Cleaning up resources..."
    devices.cleanup()
    log.close()

  atexit.register(exit_handler)

  # Start web interface
  if config["web"]: start_web_app()

  # Start main control loop
  control_loop(brain, devices, log_path)

def control_loop(brain, devices, log_file):
  logging.debug("Starting control loop")

  while True:
    inputs = devices.read()
    log.write(json.dumps(inputs))

    actions = brain.process_inputs(inputs)

    devices.perform(actions)


class ConfigManager:
  def __init__(self):
    json_data = open("config.json")
    self.config = json.load(json_data)
    json_data.close()

    print self.config

  def __getitem__(self, attr):
    return self.config[attr]

  def load(self):
    logging.debug("Loading config")

class DeviceManager:
  def __init__(self, config):
    self.config = config
    self.devices = []
    self.sensors = []

    for device_config in self.config['devices']:
      device_class = getattr(devices, device_config['className'])
      device = device_class()
      device.serial_number = device_config['serialNumber']
      self.devices.append(device)

      print "Device"
      print device


  def load(self):
    logging.debug("Loading devices")
    for device in self.devices:
      device.load()


  def read(self):
    values = {}
    for device in self.devices:
      d = device.read()
      if d: values.update(d)

    return values

  def perform(self, actions):
    pass

  def cleanup(self):
    for device in self.devices:
      device.cleanup()

class Brain:
  def __init__(self, config):
    self.config = config

  def load(self):
    logging.debug("Loading brain")

  def process_inputs(self, inputs):
    return {}


if __name__ == "__main__":
  run()
