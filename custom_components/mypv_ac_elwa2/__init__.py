import logging
from homeassistant.core import HomeAssistant

from .const import DOMAIN, CONF_SCAN_INTERVAL, CONF_RESEND
from .coordinator import ElwaCoordinator

_LOGGER = logging.getLogger(__name__)

PLATFORMS = ["sensor", "number"]      # keep this in one place

async def async_setup_entry(hass: HomeAssistant, entry):
    """Set up one AC Elwa 2 unit."""
    hass.data.setdefault(DOMAIN, {})

    _LOGGER.debug(f"Setting up entry for {conf.get(CONF_SCAN_INTERVAL, 10)} seconds scan interval and {conf.get(CONF_RESEND, 10)} seconds resend interval.")

    conf = entry.data
    coord = ElwaCoordinator(
        hass,
        host=conf["host"],
        scan_sec=conf.get(CONF_SCAN_INTERVAL, 10),
        resend_sec=conf.get(CONF_RESEND, 10),
    )
    await coord.async_config_entry_first_refresh()
    hass.data[DOMAIN][entry.entry_id] = coord

    # ← FIX: forward the entry to the platforms
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass, entry):
    await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    hass.data[DOMAIN].pop(entry.entry_id)
    return True
