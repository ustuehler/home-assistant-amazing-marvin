import logging

import voluptuous as vol
from homeassistant import config_entries, exceptions
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
from requests import HTTPError

from .const import CONF_API_TOKEN, DOMAIN, CONF_TITLE
from amazing_marvin import AmazingMarvinAPI

_LOGGER = logging.getLogger(__name__)

USER_DATA_SCHEMA = vol.Schema({
    vol.Required(CONF_API_TOKEN): str,
})


async def validate_input(
        hass: HomeAssistant,
        user_input: dict
) -> dict[str, any]:
    """Verify that the user input allows us to connect to Amazing Marvin.

    Data has the keys from DATA_SCHEMA with values provided by the user.
    """
    api_token = user_input[CONF_API_TOKEN]

    try:
        marvin = AmazingMarvinAPI(api_token)
        account_info = await hass.async_add_executor_job(marvin.me)
        email = account_info['email']
    except HTTPError as error:
        if error.response.status_code == 401:
            raise InvalidAuth
        else:
            raise

    return {
        CONF_TITLE: email,
        'data': {
            CONF_API_TOKEN: api_token
        }
    }


class AmazingMarvinConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Amazing Marvin config flow."""

    async def async_step_user(
            self,
            user_input: dict[str, any] or None = None
    ) -> FlowResult:
        errors = {}
        if user_input is not None:
            # noinspection PyBroadException
            try:
                entry = await validate_input(self.hass, user_input)

                await self.async_set_unique_id(entry[CONF_TITLE])
                self._abort_if_unique_id_configured()

                return self.async_create_entry(**entry)
            except InvalidAuth:
                errors['base'] = 'invalid_auth'
            except Exception:
                _LOGGER.exception("Unexpected exception")
                errors['base'] = 'unknown'

        return self.async_show_form(
            step_id='user',
            data_schema=USER_DATA_SCHEMA,
            errors=errors
        )


class InvalidAuth(exceptions.ConfigEntryAuthFailed):
    """Error to indicate an invalid username or password."""
