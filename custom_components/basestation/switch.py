"""The basestation switch."""

from bleak import BleakClient
from homeassistant.components.switch import SwitchEntity
from homeassistant.components import bluetooth
import asyncio

from .const import (
    PWR_CHARACTERISTIC,
    PWR_ON,
    PWR_STANDBY,
)


def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the sensor platform."""
    mac = config.get("mac")
    name = config.get("name")
    add_entities([BasestationSwitch(hass, mac, name)])


class BasestationSwitch(SwitchEntity):
    """The basestation switch implementtion."""

    def __init__(self, hass, mac, name):
        """Initialize the switch."""
        self._hass = hass
        self._mac = mac
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
        asyncio.run(self.async_turn_on())

    def turn_off(self, **kwargs):
        """Turn the switch off."""
        asyncio.run(self.async_turn_off())

    @property
    def name(self):
        """Return the name of the switch."""
        if self._name is not None:
            return self._name

        return "Valve Basestation"

    def update(self):
        """Fetch new state data for the sensor."""
        asyncio.run(self.async_update())

    async def async_turn_on(self):
        async with BleakClient(self.get_ble_device()) as client:
            await client.write_gatt_char(PWR_CHARACTERISTIC, PWR_ON)

    async def async_turn_off(self):
        async with BleakClient(self.get_ble_device()) as client:
            await client.write_gatt_char(PWR_CHARACTERISTIC, PWR_STANDBY)

    async def async_update(self):
        async with BleakClient(self.get_ble_device()) as client:
            self._is_on = await client.read_gatt_char(PWR_CHARACTERISTIC) != PWR_STANDBY

    def get_ble_device(self):
        return bluetooth.async_ble_device_from_address(self._hass, str(self._mac))
