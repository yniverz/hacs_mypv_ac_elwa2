import logging
from homeassistant.core import HomeAssistant

from .const import DOMAIN
from .coordinator import ElwaCoordinator

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry):
    """Set up one AC Elwa 2."""
    hass.data.setdefault(DOMAIN, {})
    conf = entry.data
    coord = ElwaCoordinator(
        hass,
        host=conf["host"],
        scan_sec=conf.get("scan_interval", 10),
        resend_sec=conf.get("resend_seconds", 30),
    )
    await coord.async_config_entry_first_refresh()
    hass.data[DOMAIN][entry.entry_id] = coord

    # register platforms
    hass.config_entries.async_setup_platforms(entry, ["sensor", "number"])
    return True

async def async_unload_entry(hass, entry):
    await hass.config_entries.async_unload_platforms(entry, ["sensor", "number"])
    hass.data[DOMAIN].pop(entry.entry_id)
    return True
