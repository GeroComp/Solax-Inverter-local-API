from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from .const import DOMAIN

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Nastavení integrace z konfiguračního záznamu v UI."""
    
    # Inicializujeme úložiště dat pro doménu
    hass.data.setdefault(DOMAIN, {})
    
    # Uložíme konfigurační data pod unikátní ID této instance
    # To umožní sensor.py snadno přistupovat k IP a heslu konkrétního zařízení
    hass.data[DOMAIN][entry.entry_id] = entry.data
    
    # Předání nastavení do platformy 'sensor'
    await hass.config_entries.async_forward_entry_setups(entry, ["sensor"])
    
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Odstranění integrace z Home Assistanta."""
    
    # Korektní ukončení platformy sensor
    # Poznámka: u async_forward_entry_setups (množné) se obvykle v unload 
    # používá async_unload_platforms (množné) pro konzistenci
    unload_ok = await hass.config_entries.async_unload_platforms(entry, ["sensor"])
    
    # Po úspěšném odstranění vyčistíme data konkrétní instance z paměti
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id, None)
    
    return unload_ok