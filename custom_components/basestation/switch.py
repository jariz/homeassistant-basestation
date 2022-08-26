"""The basestation switch."""

from bleak import BleakClient

from homeassistant.components.switch import SwitchEntity

from .const import (
    PWR_CHARACTERISTIC,
    PWR_ON,
    PWR_STANDBY,
)

def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the sensor platform."""
    mac = config.get("mac")
    name = config.get("name")
    device = BleakClient(mac)
    add_entities([BasestationSwitch(device, name)])


class BasestationSwitch(SwitchEntity):
    """The basestation switch implementtion."""

    def __init__(self, device, name):
        """Initialize the switch."""
        self._device = device
        self._name = name
        self._is_on = False

    @property
    def icon(self):
        """Return the icon."""
        return "mdi:virtual-reality"

    @property
    def is_on(self):
        """If the switch is currently on or off."""
        return self._is_on

    def turn_on(self, **kwargs):
        """Turn the switch on."""
        await self._device.connect()
        await self._device.write_gatt_char(PWR_CHARACTERISTIC, PWR_ON)
        await self._device.disconnect()

    def turn_off(self, **kwargs):
        """Turn the switch off."""
        await self._device.connect()
        await self._device.write_gatt_char(PWR_CHARACTERISTIC, PWR_STANDBY)
        await self._device.disconnect()

    @property
    def name(self):
        """Return the name of the switch."""
        if self._name is not None:
            return self._name

        return "Valve Basestation"

    def update(self):
        """Fetch new state data for the sensor."""
        await self._device.connect()
        self._is_on = await self._device.read_gatt_char(PWR_CHARACTERISTIC) != PWR_STANDBY
        await self._device.disconnect()
