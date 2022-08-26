"""Constants for the Valve Index Basestation integration."""

DOMAIN = "basestation"
PWR_CHARACTERISTIC = "00001525-1212-efde-1523-785feabcd124"
PWR_ON = bytearray([0x01])
PWR_STANDBY = bytearray([0x00])