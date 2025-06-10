from homeassistant.components.number import NumberEntity, NumberMode
from .const import DOMAIN, MAX_W

async def async_setup_entry(hass, entry, async_add_entities):
    coord = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([ElwaNumber(coord, entry.entry_id)])

class ElwaNumber(NumberEntity):
    _attr_name = "AC Elwa 2 Target Power"
    _attr_native_min_value = 0
    _attr_native_max_value = MAX_W
    _attr_native_step = 1
    _attr_unit_of_measurement = "W"
    _attr_mode = NumberMode.SLIDER

    def __init__(self, coordinator, entry_id):
        self._coord = coordinator
        self._attr_unique_id = f"{entry_id}_target_power"

    @property
    def native_value(self):
        return self._coord.data.get("target_power")

    async def async_set_native_value(self, value: float):
        await self._coord.write_target(int(value))
