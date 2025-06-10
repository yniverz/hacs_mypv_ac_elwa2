from homeassistant.components.number import NumberEntity, NumberMode
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN, MAX_W

async def async_setup_entry(hass, entry, async_add_entities):
    coord = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([ElwaNumber(coord, entry.entry_id)])

class ElwaNumber(CoordinatorEntity, NumberEntity):
    _attr_name = "AC Elwa 2 Target Power"
    _attr_native_min_value = 0
    _attr_native_max_value = MAX_W
    _attr_native_step = 1
    _attr_unit_of_measurement = "W"
    _attr_mode = NumberMode.SLIDER

    def __init__(self, coordinator, entry_id):
        # self._coord = coordinator
        super().__init__(coordinator)
        self._attr_unique_id = f"{entry_id}_target_power"
        self._last_value = 0

    @property
    def native_value(self):
        return self._last_value

    async def async_set_native_value(self, value: float):
        self._last_value = value
        await self._coord.write_target(int(value))
