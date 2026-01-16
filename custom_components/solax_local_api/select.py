from homeassistant.components.select import SelectEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.const import EntityCategory, CONF_SCAN_INTERVAL
from datetime import timedelta

from .const import DOMAIN

# Definice intervalů
INTERVAL_OPTIONS = {
    "6 sekund (Agresivní)": 6,
    "10 sekund": 10,
    "15 sekund": 15,
    "20 sekund": 20,
    "30 sekund": 30,
    "40 sekund": 40,
    "50 sekund": 50,
    "1 minuta": 60,
    "2 minuty": 120,
    "3 minuty": 180,
    "4 minuty": 240,
    "5 minut": 300,
}

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    coordinator = hass.data[DOMAIN][entry.entry_id]
    # Předáváme i "entry", abychom do něj mohli ukládat a brát ID
    async_add_entities([SolaXScanIntervalSelect(coordinator, entry)])

class SolaXScanIntervalSelect(CoordinatorEntity, SelectEntity):
    """Výběr intervalu aktualizace."""

    _attr_has_entity_name = True
    _attr_name = "Scan Interval"
    _attr_icon = "mdi:timer-cog-outline" # <--- ZMĚNA IKONY
    _attr_entity_category = EntityCategory.CONFIG
    _attr_options = list(INTERVAL_OPTIONS.keys())

    def __init__(self, coordinator, entry):
        super().__init__(coordinator)
        self.entry = entry
        # Unikátní ID musí obsahovat entry_id
        self._attr_unique_id = f"solax_scan_interval_{entry.entry_id}"

    @property
    def device_info(self) -> DeviceInfo:
        """Propojení se zařízením SolaX."""
        return DeviceInfo(
            identifiers={(DOMAIN, self.entry.entry_id)}
        )

    @property
    def current_option(self) -> str | None:
        """Zjistí, která možnost odpovídá aktuálnímu nastavení."""
        if not self.coordinator.update_interval:
            return None
            
        current_seconds = int(self.coordinator.update_interval.total_seconds())
        
        for label, seconds in INTERVAL_OPTIONS.items():
            if seconds == current_seconds:
                return label
        return None

    async def async_select_option(self, option: str) -> None:
        """Když uživatel vybere možnost z roletky."""
        new_seconds = INTERVAL_OPTIONS[option]
        
        # 1. Změna v běžícím systému (okamžitá reakce)
        self.coordinator.update_interval = timedelta(seconds=new_seconds)
        self.async_write_ha_state()
        
        # 2. Uložení do konfigurace (aby to přežilo restart)
        new_data = self.entry.data.copy()
        new_data[CONF_SCAN_INTERVAL] = new_seconds
        
        # Aktualizujeme config entry v Home Assistantovi
        self.hass.config_entries.async_update_entry(self.entry, data=new_data)
        
        # Vynucení okamžitého obnovení dat s novým intervalem
        await self.coordinator.async_request_refresh()