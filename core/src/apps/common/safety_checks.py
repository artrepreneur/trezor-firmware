import storage.device
from trezor.messages import SafetyCheckLevel

if False:
    from typing import Optional, Tuple
    from trezor.messages.ApplySettings import EnumTypeSafetyCheckLevel

_temporary_safety_checks = None  # type: Optional[EnumTypeSafetyCheckLevel]


def get() -> EnumTypeSafetyCheckLevel:
    """
    Returns the effective safety check level.
    """
    if _temporary_safety_checks is None:
        return storage.device.safety_check_level()
    else:
        return _temporary_safety_checks


def get_settings() -> Tuple[
    EnumTypeSafetyCheckLevel, Optional[EnumTypeSafetyCheckLevel]
]:
    """
    Returns both settings.
    """
    return storage.device.safety_check_level(), _temporary_safety_checks


def set(
    persistent: Optional[EnumTypeSafetyCheckLevel],
    temporary: Optional[EnumTypeSafetyCheckLevel],
) -> None:
    """
    Changes the safety level settings. If the persistent value is None it is left as is.
    If the temporary value is None it is cleared (i.e. persistent value becomes effective afterwards).
    """
    global _temporary_safety_checks

    if persistent is None:
        persistent = storage.device.safety_check_level()

    if temporary is not None and persistent == temporary:
        raise ValueError(
            "Cannot set safety_checks and temporary_safety_checks to the same level"
        )

    _temporary_safety_checks = temporary
    storage.device.set_safety_check_level(persistent)


def is_prompt() -> bool:
    """
    Shorthand for checking whether the effective level is Prompt.
    """
    return get() == SafetyCheckLevel.Prompt
