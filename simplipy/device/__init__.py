"""Define a base SimpliSafe device."""
from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING, Any, Dict, cast

if TYPE_CHECKING:
    from simplipy.system import System


class DeviceTypes(Enum):
    """Device types based on internal SimpliSafe ID number."""

    remote = 0
    keypad = 1
    keychain = 2
    panic_button = 3
    motion = 4
    entry = 5
    glass_break = 6
    carbon_monoxide = 7
    smoke = 8
    leak = 9
    temperature = 10
    camera = 12
    siren = 13
    doorbell = 15
    lock = 16
    outdoor_camera = 17
    lock_keypad = 253
    unknown = 99


class Device:
    """A base SimpliSafe device.

    Note that this class shouldn't be instantiated directly; it will be instantiated as
    appropriate via :meth:`simplipy.API.get_systems`.

    :param system: A :meth:`simplipy.system.System` object (or one of its subclasses)
    :type system: :meth:`simplipy.system.System`
    :param device_type: The type of device represented
    :type device_type: :meth:`simplipy.device.DeviceTypes`
    :param serial: The serial number of the device
    :type serial: ``str``
    """

    def __init__(self, system: System, device_type: DeviceTypes, serial: str) -> None:
        """Initialize."""
        self._device_type = device_type
        self._serial = serial
        self._system = system

    @property
    def name(self) -> str:
        """Return the device name.

        :rtype: ``str``
        """
        return cast(str, self._system.sensor_data[self._serial]["name"])

    @property
    def serial(self) -> str:
        """Return the device's serial number.

        :rtype: ``str``
        """
        return cast(str, self._system.sensor_data[self._serial]["serial"])

    @property
    def type(self) -> DeviceTypes:
        """Return the device type.

        :rtype: :meth:`simplipy.device.DeviceTypes`
        """
        return self._device_type

    async def update(self, cached: bool = True) -> None:
        """Retrieve the latest state/properties for the device.

        The ``cached`` parameter determines whether the SimpliSafe Cloud uses the last
        known values retrieved from the base station (``True``) or retrieves new data.

        :param cached: Whether to used cached data.
        :type cached: ``bool``
        """
        await self._system.update(
            include_subscription=False, include_settings=False, cached=cached
        )


class DeviceV3(Device):
    """A base device for V3 systems.

    Note that this class shouldn't be instantiated directly; it will be
    instantiated as appropriate via :meth:`simplipy.API.get_systems`.
    """

    @property
    def error(self) -> bool:
        """Return the device's error status.

        :rtype: ``bool``
        """
        return cast(
            bool,
            self._system.sensor_data[self._serial]["status"].get("malfunction", False),
        )

    @property
    def low_battery(self) -> bool:
        """Return whether the device's battery is low.

        :rtype: ``bool``
        """
        return cast(bool, self._system.sensor_data[self._serial]["flags"]["lowBattery"])

    @property
    def offline(self) -> bool:
        """Return whether the device is offline.

        :rtype: ``bool``
        """
        return cast(bool, self._system.sensor_data[self._serial]["flags"]["offline"])

    @property
    def settings(self) -> dict[str, Any]:
        """Return the device's settings.

        Note that these can change based on what device type the device is.

        :rtype: ``dict``
        """
        return cast(Dict[str, Any], self._system.sensor_data[self._serial]["setting"])
