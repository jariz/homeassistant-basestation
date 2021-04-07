"""The basestation switch."""

from basestation.device import BasestationDevice

from homeassistant.components.switch import SwitchEntity


def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the sensor platform."""
    mac = config.get("mac")
    name = config.get("name")
    device = BasestationDevice(mac)
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
        self._device.connect()
        self._device.turn_on()
        self._device.disconnect()

    def turn_off(self, **kwargs):
        """Turn the switch off."""
        self._device.connect()
        self._device.turn_off()
        self._device.disconnect()

    @property
    def name(self):
        """Return the name of the switch."""
        if self._name is not None:
            return self._name

        return "Valve Basestation"

    def update(self):
        """Fetch new state data for the sensor."""
        self._device.connect()
        self._is_on = self._device.is_turned_on()
        self._device.disconnect()
