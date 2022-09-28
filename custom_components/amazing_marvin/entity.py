"""Amazing Marvin entity base class."""
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from . import AmazingMarvinDataUpdateCoordinator
from .const import DOMAIN, NAME, ATTRIBUTION


class AmazingMarvinEntity(CoordinatorEntity):
    def __init__(
            self,
            coordinator: AmazingMarvinDataUpdateCoordinator,
            entry: ConfigEntry
    ) -> None:
        super().__init__(coordinator)
        self.config_entry = entry

    @property
    def unique_id(self):
        """Return a unique ID to use for this entity."""
        return f'{self.config_entry.entry_id}-{self.name}'

    # TODO: specify device info

    #@property
    #def device_info(self):
    #    return {
    #        "identifiers": {(DOMAIN, self.unique_id)},
    #        "name": NAME,
    #        # TODO: specify some model and manufacturer
    #        #"model": VERSION,
    #        #"manufacturer": NAME,
    #    }

    #@property
    #def extra_state_attributes(self):
    #    """Return the state attributes."""
    #    return {
    #        "attribution": ATTRIBUTION,
    #        "id": str(self.coordinator.config_entry.entry_id),
    #        "integration": DOMAIN,
    #    }
