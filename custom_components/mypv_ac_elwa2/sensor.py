from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.const import UnitOfTemperature, UnitOfPower
from .const import DOMAIN

SENSORS = (
    ("temperature", "Boiler Temperature", UnitOfTemperature.CELSIUS, "temperature"),
    ("current_power", "Current Power", UnitOfPower.WATT, "power"),
)

async def async_setup_entry(hass, entry, async_add_entities):
    coord = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(
        [ElwaSensor(coord, entry.entry_id, *args) for args in SENSORS]
    )

class ElwaSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator, entry_id, key, name, unit, device_class):
        super().__init__(coordinator)
        self._attr_name = f"AC Elwa 2 {name}"
        self._attr_unit_of_measurement = unit
        self._attr_native_unit_of_measurement = unit
        self._attr_device_class = device_class
        self._key = key
        self._attr_unique_id = f"{entry_id}_{key}"

    @property
    def available(self):
        return self.coordinator.last_update_success

    @property
    def native_value(self):
        return self.coordinator.data.get(self._key)
