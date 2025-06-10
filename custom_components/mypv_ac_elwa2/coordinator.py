from datetime import timedelta
import asyncio
import logging
from pymodbus.client import AsyncModbusTcpClient
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .const import (
    DOMAIN, DEFAULT_PORT, POWER_SET_REG, POWER_REG, TEMP_REG, MAX_W,
)

_LOGGER = logging.getLogger(__name__)


class ElwaCoordinator(DataUpdateCoordinator):
    def __init__(self, hass, host, scan_sec, resend_sec):
        self.host = host
        super().__init__(
            hass,
            _LOGGER,
            name=f"elwa2_{host}",
            update_interval=timedelta(seconds=scan_sec),
        )
        self._client = AsyncModbusTcpClient(host=host, port=DEFAULT_PORT)
        self._last_target = 0
        self._resend_sec = resend_sec
        # schedule resend loop
        hass.loop.create_task(self._resend_loop())

    async def _async_update_data(self):
        """Read temp & power in one round-trip."""
        await self._client.connect()
        # rr = await self._client.read_holding_registers(address=POWER_REG, count=2, slave=1)
        # power_target, temp_raw = rr.registers

        rr = await self._client.read_holding_registers(address=POWER_REG, slave=1)
        power = rr.registers[0] if rr.registers else 0
        rr = await self._client.read_holding_registers(address=TEMP_REG, slave=1)
        temp_raw = rr.registers[0] if rr.registers else 0

        return {
            "temperature": temp_raw * 0.1,
            "current_power": power,
        }

    async def write_target(self, watts: int):
        watts = max(0, min(MAX_W, watts))
        self._last_target = watts
        await self._client.write_register(address=POWER_SET_REG, value=watts, slave=1)

    async def _resend_loop(self):
        """Periodically resend non-zero target to overcome the ELWA timeout."""
        while True:
            await asyncio.sleep(self._resend_sec)
            if self._last_target:
                try:
                    await self.write_target(self._last_target)
                except Exception as exc:   # noqa: BLE001
                    _LOGGER.debug("ELWA resend failed: %s", exc)
