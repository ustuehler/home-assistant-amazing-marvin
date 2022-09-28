"""Constants for the Amazing Marvin integration."""
from datetime import timedelta

from amazing_marvin import API_URL
from homeassistant.const import Platform

# TODO: rename this integration's domain to `amazing_marvin`
DOMAIN = 'amazing_marvin'
NAME = 'Amazing Marvin'
ATTRIBUTION = f"Data provided by {API_URL}"

PLATFORMS = [Platform.SENSOR]

CONF_TITLE = 'title'
CONF_API_TOKEN = 'api_token'

SCAN_INTERVAL = timedelta(minutes=15)

DATA_TODAY_ITEMS = 'today_items'

TODAY_ITEMS_SENSOR_NAME = "Amazing Marvin Today Items"
TODAY_ITEMS_SENSOR_ICON = 'mdi:calendar-check'

TODAY_ESTIMATE_SENSOR_NAME = "Amazing Marvin Today Estimate"
TODAY_ESTIMATE_SENSOR_ICON = 'mdi:calendar-clock'
