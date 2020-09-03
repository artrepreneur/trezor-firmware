import storage.cache
import storage.device
from storage.cache import APP_COMMON_SAFETY_CHECKS_TEMPORARY
from trezor.messages import SafetyCheckLevel

if False:
    from typing import Optional
    from trezor.messages.ApplySettings import EnumTypeSafetyCheckLevel


def get() -> EnumTypeSafetyCheckLevel:
    """
    Returns the effective safety check level.
    """
    temporary_safety_check_level = storage.cache.get(
        APP_COMMON_SAFETY_CHECKS_TEMPORARY
    )  # type: Optional[EnumTypeSafetyCheckLevel]
    if temporary_safety_check_level is None:
        return storage.device.safety_check_level()
    else:
        return temporary_safety_check_level


def set(level: EnumTypeSafetyCheckLevel) -> None:
    """
    Changes the safety level settings.
    """
    if level in (SafetyCheckLevel.Strict, SafetyCheckLevel.PromptAlways):
        storage.cache.delete(APP_COMMON_SAFETY_CHECKS_TEMPORARY)
        storage.device.set_safety_check_level(level)
    elif level == SafetyCheckLevel.PromptTemporarily:
        storage.device.set_safety_check_level(SafetyCheckLevel.Strict)
        storage.cache.set(APP_COMMON_SAFETY_CHECKS_TEMPORARY, level)
    else:
        raise ValueError("Unknown SafetyCheckLevel")


def is_prompt() -> bool:
    """
    Shorthand for checking whether the effective level is PromptAlways or PromptTemporarily.
    """
    return get() in (SafetyCheckLevel.PromptAlways, SafetyCheckLevel.PromptTemporarily)
