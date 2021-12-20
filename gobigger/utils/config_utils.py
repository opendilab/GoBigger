import copy
from typing import List, Optional


def deep_merge_dicts(original: dict, new_dict: dict) -> dict:
    """
    Overview:
        Merge two dicts by calling ``deep_update``
    Arguments:
        - original (:obj:`dict`): Dict 1.
        - new_dict (:obj:`dict`): Dict 2.
    Returns:
        - merged_dict (:obj:`dict`): A new dict that is d1 and d2 deeply merged.
    """
    original = original or {}
    new_dict = new_dict or {}
    merged = copy.deepcopy(original)
    if new_dict:  # if new_dict is neither empty dict nor None
        deep_update(merged, new_dict, True, [])
    return merged


def deep_update(
        original: dict,
        new_dict: dict,
        new_keys_allowed: bool = False,
        whitelist: Optional[List[str]] = None,
        override_all_if_type_changes: Optional[List[str]] = None
):
    """
    Overview:
        Update original dict with values from new_dict recursively.
    Arguments:
        - original (:obj:`dict`): Dictionary with default values.
        - new_dict (:obj:`dict`): Dictionary with values to be updated
        - new_keys_allowed (:obj:`bool`): Whether new keys are allowed.
        - whitelist (:obj:`Optional[List[str]]`):
            List of keys that correspond to dict
            values where new subkeys can be introduced. This is only at the top
            level.
        - override_all_if_type_changes(:obj:`Optional[List[str]]`):
            List of top level
            keys with value=dict, for which we always simply override the
            entire value (:obj:`dict`), if the "type" key in that value dict changes.

    .. note::

        If new key is introduced in new_dict, then if new_keys_allowed is not
        True, an error will be thrown. Further, for sub-dicts, if the key is
        in the whitelist, then new subkeys can be introduced.
    """
    whitelist = whitelist or []
    override_all_if_type_changes = override_all_if_type_changes or []

    for k, value in new_dict.items():
        if k not in original and not new_keys_allowed:
            raise RuntimeError("Unknown config parameter `{}`. Base config have: {}.".format(k, original.keys()))

        # Both original value and new one are dicts.
        if isinstance(original.get(k), dict) and isinstance(value, dict):
            # Check old type vs old one. If different, override entire value.
            if k in override_all_if_type_changes and \
                    "type" in value and "type" in original[k] and \
                    value["type"] != original[k]["type"]:
                original[k] = value
            # Whitelisted key -> ok to add new subkeys.
            elif k in whitelist:
                deep_update(original[k], value, True)
            # Non-whitelisted key.
            else:
                deep_update(original[k], value, new_keys_allowed)
        # Original value not a dict OR new value not a dict:
        # Override entire value.
        else:
            original[k] = value
    return original
