import logging
import importlib.resources
LOG = logging.getLogger(f"sap1.{__name__}")

EEPROM_A = importlib.resources.read_binary('sap1.firmware', 'eeprom_a.bin')
EEPROM_B = importlib.resources.read_binary("sap1.firmware", 'eeprom_b.bin')

