from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.const import CONF_HOST, CONF_PASSWORD, CONF_SCAN_INTERVAL

# Importujeme seznam platforem a doménu
from .const import DOMAIN, PLATFORMS, DEFAULT_SCAN_INTERVAL
# Importujeme náš nový koordinátor
from .coordinator import SolaxUpdateCoordinator

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Nastavení integrace z konfiguračního záznamu v UI."""
    hass.data.setdefault(DOMAIN, {})

    # Načtení konfiguračních dat
    ip = entry.data[CONF_HOST]
    pwd = entry.data[CONF_PASSWORD]
    scan_interval = entry.data.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL)

    # Vytvoření instance koordinátora
    coordinator = SolaxUpdateCoordinator(hass, ip, pwd, scan_interval)

    # --- ZMĚNA: Optimistický start ---
    # Zkusíme stáhnout data. Pokud střídač spí (neodpovídá), 
    # chybu ignorujeme (pass), aby se integrace i tak načetla 
    # a vytvořily se senzory (budou zatím 'Nedostupné').
    try:
        await coordinator.async_config_entry_first_refresh()
    except Exception:
        pass

    # Uložení koordinátora do globálních dat (klíčové pro select.py)
    hass.data[DOMAIN][entry.entry_id] = coordinator
    
    # Načtení všech platforem (Senzory i Select)
    # Zde se využívá seznam PLATFORMS z const.py, který musí obsahovat ["sensor", "select"]
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Odstranění integrace z Home Assistanta."""
    # Odstranění všech platforem
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id, None)
    
    return unload_ok