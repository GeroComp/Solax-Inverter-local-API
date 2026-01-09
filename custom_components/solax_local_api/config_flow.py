import asyncio
import logging
import aiohttp
import async_timeout
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.components import dhcp
from homeassistant.const import CONF_HOST, CONF_PASSWORD, CONF_SCAN_INTERVAL
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import DOMAIN, DEFAULT_SCAN_INTERVAL

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema({
    vol.Required(CONF_HOST): str,
    vol.Required(CONF_PASSWORD): str,
    vol.Optional(CONF_SCAN_INTERVAL, default=DEFAULT_SCAN_INTERVAL): int,
})

class SolaxConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Konfigurační flow pro SolaX."""
    
    VERSION = 1

    def __init__(self):
        self._discovered_host = None

    async def _verify_pocket_wifi(self, ip_address):
        """Ověří zařízení kontrolou stránky /login."""
        session = async_get_clientsession(self.hass)
        url = f"http://{ip_address}/login"
        
        try:
            async with async_timeout.timeout(5):
                response = await session.get(url)
                if response.status == 200:
                    text = await response.text()
                    if "Pocket Wi-Fi" in text:
                        _LOGGER.debug("SolaX Pocket Wi-Fi potvrzen na %s", ip_address)
                        return True
        except (aiohttp.ClientError, asyncio.TimeoutError):
            return False
        return False

    async def async_step_dhcp(self, discovery_info: dhcp.DhcpServiceInfo):
        """Automatický záchyt z DHCP."""
        hostname = (discovery_info.hostname or "").lower()
        
        # Filtrujeme pouze zařízení od Espressif
        if "espressif" not in hostname:
            return self.async_abort(reason="not_solax_device")

        # Ověříme, že na nalezené IP adrese skutečně běží SolaX login
        if not await self._verify_pocket_wifi(discovery_info.ip):
            return self.async_abort(reason="not_solax_device")

        await self.async_set_unique_id(discovery_info.macaddress)
        self._abort_if_unique_id_configured()

        self._discovered_host = discovery_info.ip

        self.context.update({
            "title_placeholders": {"name": "SolaX Power"}
        })

        return await self.async_step_user()

    async def async_step_user(self, user_input=None):
        """Manuální zadání údajů."""
        errors = {}

        if user_input is not None:
            if await self._verify_pocket_wifi(user_input[CONF_HOST]):
                return self.async_create_entry(
                    title=f"SolaX {user_input[CONF_HOST]}",
                    data=user_input
                )
            errors["base"] = "cannot_connect"

        return self.async_show_form(
            step_id="user",
            data_schema=self.add_suggested_values_to_schema(
                STEP_USER_DATA_SCHEMA, 
                user_input or {CONF_HOST: self._discovered_host or ""}
            ),
            errors=errors,
        )