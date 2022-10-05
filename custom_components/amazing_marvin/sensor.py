"""Sensor platform for Amazing Marvin."""

from homeassistant.components.sensor import SensorStateClass, SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.components.sensor.const import CONF_STATE_CLASS
from homeassistant.const import CONF_UNIT_OF_MEASUREMENT, TIME_MINUTES
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN, TODAY_ITEMS_SENSOR_NAME, TODAY_ITEMS_SENSOR_ICON, \
    DATA_TODAY_ITEMS, TODAY_ESTIMATE_SENSOR_NAME, TODAY_ESTIMATE_SENSOR_ICON
from .entity import AmazingMarvinEntity


async def async_setup_entry(
        hass: HomeAssistant,
        entry: ConfigEntry,
        async_add_entities: AddEntitiesCallback
) -> None:
    """Set up sensor platform for config entry."""
    coordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities([
        AmazingMarvinTodayItemsSensor(coordinator=coordinator, entry=entry),
        AmazingMarvinTodayEstimateSensor(coordinator=coordinator, entry=entry)
    ], True)


class AmazingMarvinTodayItemsSensor(AmazingMarvinEntity, SensorEntity):
    """Sensor class reporting the number of items scheduled for today."""

    @property
    def name(self):
        """Return the name of the sensor."""
        return TODAY_ITEMS_SENSOR_NAME

    @property
    def icon(self):
        """Return the icon of the sensor."""
        return TODAY_ITEMS_SENSOR_ICON

    @property
    def native_value(self):
        """Return the native value of the sensor."""
        return len(self.coordinator.data[DATA_TODAY_ITEMS])

    @property
    def extra_state_attributes(self):
        """Return the attributes of the sensor."""
        return {
            CONF_STATE_CLASS: SensorStateClass.MEASUREMENT
        }


class AmazingMarvinTodayEstimateSensor(AmazingMarvinEntity, SensorEntity):
    """Sensor class reporting the estimated time for items scheduled today."""

    @property
    def name(self):
        """Return the name of the sensor."""
        return TODAY_ESTIMATE_SENSOR_NAME

    @property
    def icon(self):
        """Return the icon of the sensor."""
        return TODAY_ESTIMATE_SENSOR_ICON

    @property
    def native_value(self):
        """Return the native value of the sensor."""
        time_estimate = 0
        for item in self.coordinator.data[DATA_TODAY_ITEMS]:
            if 'timeEstimate' in item and item['timeEstimate']:
                time_estimate += item['timeEstimate']

            if 'subtasks' in item and item['subtasks']:
                for subtask in item['subtasks'].values():
                    if 'done' in subtask and subtask['done']:
                        # Already completed subtasks don't count.
                        continue

                    if 'timeEstimate' in subtask and subtask['timeEstimate']:
                        time_estimate += subtask['timeEstimate']

        return int(round(time_estimate / 1000 / 60, 0))

    @property
    def extra_state_attributes(self):
        """Return the attributes of the sensor."""
        return {
            CONF_STATE_CLASS: SensorStateClass.MEASUREMENT,
            CONF_UNIT_OF_MEASUREMENT: TIME_MINUTES
        }
