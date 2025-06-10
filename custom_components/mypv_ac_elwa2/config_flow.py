from __future__ import annotations
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_HOST, CONF_NAME
from .const import DOMAIN, CONF_SCAN_INTERVAL, CONF_RESEND, DEFAULT_SCAN_INTERVAL, DEFAULT_RESEND

class ElwaFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title=user_input[CONF_HOST], data=user_input)

        schema = vol.Schema({
            vol.Required(CONF_HOST): str,
            vol.Optional(CONF_SCAN_INTERVAL, default=DEFAULT_SCAN_INTERVAL): vol.All(int, vol.Range(min=5)),
            vol.Optional(CONF_RESEND, default=DEFAULT_RESEND): vol.All(int, vol.Range(min=10)),
        })
        return self.async_show_form(step_id="user", data_schema=schema)
