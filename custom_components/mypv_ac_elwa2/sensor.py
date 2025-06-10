from homeassistant.components.sensor import SensorEntity
from homeassistant.const import UnitOfTemperature, UnitOfPower
from .const import DOMAIN

SENSORS = (
    ("temperature", "Boiler Temperature", UnitOfTemperature.CELSIUS, "temperature"),
    ("target_power", "Target Power", UnitOfPower.WATT, "power"),
)

async def async_setup_entry(hass, entry, async_add_entities):
    coord = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(
        [ElwaSensor(coord, *args) for args in SENSORS]
    )

class ElwaSensor(SensorEntity):
    def __init__(self, coordinator, key, name, unit, device_class):
        self._coord = coordinator
        self._attr_name = f"AC Elwa 2 {name}"
        self._attr_unit_of_measurement = unit
        self._attr_device_class = device_class
        self._key = key

    @property
    def available(self):
        return self._coord.last_update_success

    @property
    def native_value(self):
        return self._coord.data.get(self._key)
