import logging
from datetime import timedelta
import async_timeout

from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)
from homeassistant.helpers.aiohttp_client import async_get_clientsession

_LOGGER = logging.getLogger(__name__)

class SolaxUpdateCoordinator(DataUpdateCoordinator):
    """Třída pro stahování dat ze střídače přes lokální API."""

    def __init__(self, hass, ip, pwd, scan_interval):
        super().__init__(
            hass, _LOGGER, name="Solax Data",
            update_interval=timedelta(seconds=scan_interval),
        )
        self.ip = ip
        self.pwd = pwd
        self.session = async_get_clientsession(hass)

    async def _async_update_data(self):
        """Načtení dat z API."""
        url = f"http://{self.ip}/"
        payload = f"optType=ReadRealTimeData&pwd={self.pwd}"
        
        try:
            async with async_timeout.timeout(10):
                async with self.session.post(url, data=payload) as response:
                    if response.status != 200:
                        raise UpdateFailed(f"Chyba střídače: {response.status}")
                    
                    data = await response.json(content_type=None)
                    if not data or "Data" not in data:
                        raise UpdateFailed("Neúplná data ze střídače")
                    return data
        except Exception as err:
            raise UpdateFailed(f"Chyba komunikace: {err}")