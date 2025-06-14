from datetime import timedelta
import asyncio
import logging
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
import aiohttp

from .const import (
    DOMAIN, DEFAULT_PORT, POWER_SET_REG, POWER_REG, TEMP_REG, MAX_W,
)

_LOGGER = logging.getLogger(__name__)

async def fetch_json(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            response.raise_for_status()  # Optional: raise an error for bad status codes
            data = await response.json()
            return data
        
async def send_get(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            response.raise_for_status()  # Optional: raise an error for bad status codes
            return await response.text()

class ElwaCoordinator(DataUpdateCoordinator):
    def __init__(self, hass, host, scan_sec, resend_sec):
        self.host = host
        super().__init__(
            hass,
            _LOGGER,
            name=f"elwa2_{host}",
            update_interval=timedelta(seconds=scan_sec),
        )
        self._last_target = 0
        self._resend_sec = resend_sec
        
        hass.loop.create_task(self._resend_loop())

    async def _async_update_data(self):
        """Read temp & power in one round-trip."""
        _LOGGER.warning("Fetching data from %s", self.host)

        power = 0
        temp_raw = 0
        try:
            data = await fetch_json(f"http://{self.host}/data.jsn")
            power = data.get("power_elwa2", 0)
            temp_raw = data.get("temp1", 0)
        except Exception as e:
            _LOGGER.error("HTTP/JSON Error from %s: %s", self.host, e)
        
        return {
            "temperature": temp_raw * 0.1,
            "current_power": power,
        }

    async def write_target(self, watts: int):
        watts = max(0, min(MAX_W, watts))
        self._last_target = watts
        await send_get(f"http://{self.host}/control.html?power={watts}")

    async def _resend_loop(self):
        """Periodically resend non-zero target to overcome the ELWA timeout."""
        while True:
            await asyncio.sleep(self._resend_sec)
            # _LOGGER.warning("ELWA resend loop running for %s", self.host)
            if self._last_target:
                try:
                    await self.write_target(self._last_target)
                except Exception as exc:   # noqa: BLE001
                    _LOGGER.warning("ELWA resend failed: %s", exc)
