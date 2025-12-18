from homeassistant.components.sensor import SensorDeviceClass

DOMAIN = "solax_local_api"

# Definice: "klíč": ["Název", "Jednotka", DeviceClass, Index_v_Data, Faktor, Typ_Dat, Ikona]
# Typy dat (dtype): 0=uint, 1=int (signed), 2=long (32bit), 3=status/mode, 7=info
SENSOR_TYPES = {
    # --- VÝKONOVÉ SENZORY (W) ---
    "pv_power_total": ["Celkový výkon panelů", "W", SensorDeviceClass.POWER, 34, 1, 0, "mdi:solar-power"],
    "pv_power_1": ["Výkon panelů 1", "W", SensorDeviceClass.POWER, 10, 1, 0, "mdi:solar-panel"],
    "pv_power_2": ["Výkon panelů 2", "W", SensorDeviceClass.POWER, 11, 1, 0, "mdi:solar-panel"],
    "grid_power": ["Síťový výkon", "W", SensorDeviceClass.POWER, 70, 1, 1, "mdi:transmission-tower"],
    "battery_power": ["Výkon baterie", "W", SensorDeviceClass.POWER, 39, 1, 1, "mdi:battery-charging-100"],
    "load_power": ["Spotřeba domu", "W", SensorDeviceClass.POWER, 47, 1, 0, "mdi:home-lightning-bolt"],

    # --- ENERGETICKÉ SENZORY (kWh) pro Energy Dashboard ---
    "today_yield": ["Dnešní výroba", "kWh", SensorDeviceClass.ENERGY, 82, 0.1, 0, "mdi:solar-power-variant"],
    "total_yield": ["Celková výroba", "kWh", SensorDeviceClass.ENERGY, [80, 81], 0.1, 2, "mdi:sigma"],
    "today_export": ["Dnešní přetok do sítě", "kWh", SensorDeviceClass.ENERGY, 86, 0.01, 0, "mdi:export"],
    "total_export": ["Celkový přetok do sítě", "kWh", SensorDeviceClass.ENERGY, [84, 85], 0.01, 2, "mdi:database-export"],
    "today_import": ["Dnešní odběr ze sítě", "kWh", SensorDeviceClass.ENERGY, 89, 0.01, 0, "mdi:import"],
    "total_import": ["Celkový odběr ze sítě", "kWh", SensorDeviceClass.ENERGY, [87, 88], 0.01, 2, "mdi:database-import"],

    # --- STAV BATERIE ---
    "battery_soc": ["Baterie SoC", "%", SensorDeviceClass.BATTERY, 103, 1, 0, "mdi:battery-high"],
    "battery_temp": ["Teplota baterie", "°C", SensorDeviceClass.TEMPERATURE, 105, 1, 0, "mdi:thermometer"],

    # --- DIAGNOSTIKA ---
    "status": ["Stav střídače", None, None, 9, 1, 3, "mdi:information-outline"],
    "mode": ["Pracovní režim", None, None, 57, 1, 3, "mdi:cog-outline"],
}

SOLAX_STATES = {
    0: "Wait", 1: "Checking", 2: "Normal", 3: "Fault", 4: "Permanent Fault", 5: "Update", 6: "EPS Check", 7: "EPS Mode", 8: "Self Test", 9: "Idle", 10: "Standby"
}

SOLAX_MODES = {
    0: "Self Use", 1: "Feed-in Priority", 2: "Back-up Mode", 3: "Manual Mode", 4: "Force Grid Charge"
}
