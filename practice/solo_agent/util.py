import copy
import json
import os
from typing import NoReturn, Optional, List

import yaml
from easydict import EasyDict
import re
from collections.abc import Sequence, Mapping
from typing import List, Dict, Union, Any

import torch
import collections.abc as container_abcs
from torch._six import string_classes
#from torch._six import int_classes as _int_classes
int_classes = int

np_str_obj_array_pattern = re.compile(r'[SaUO]')

default_collate_err_msg_format = (
    "default_collate: batch must contain tensors, numpy arrays, numbers, "
    "dicts or lists; found {}"
)


def read_config(path: str) -> EasyDict:
    """
    Overview:
        read configuration from path
    Arguments:
        - path (:obj:`str`): Path of source yaml
    Returns:
        - (:obj:`EasyDict`): Config data from this file with dict type
    """
    if path:
        assert os.path.exists(path), path
        with open(path, "r") as f:
            config = yaml.safe_load(f)
    else:
        config = {}
    return EasyDict(config)

def deep_merge_dicts(original: dict, new_dict: dict) -> dict:
    """
    Overview:
        merge two dict using deep_update
    Arguments:
        - original (:obj:`dict`): Dict 1.
        - new_dict (:obj:`dict`): Dict 2.
    Returns:
        - (:obj:`dict`): A new dict that is d1 and d2 deeply merged.
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
        Updates original dict with values from new_dict recursively.

    .. note::

        If new key is introduced in new_dict, then if new_keys_allowed is not
        True, an error will be thrown. Further, for sub-dicts, if the key is
        in the whitelist, then new subkeys can be introduced.

    Arguments:
        - original (:obj:`dict`): Dictionary with default values.
        - new_dict (:obj:`dict`): Dictionary with values to be updated
        - new_keys_allowed (:obj:`bool`): Whether new keys are allowed.
        - whitelist (Optional[List[str]]): List of keys that correspond to dict
            values where new subkeys can be introduced. This is only at the top
            level.
        - override_all_if_type_changes(Optional[List[str]]): List of top level
            keys with value=dict, for which we always simply override the
            entire value (:obj:`dict`), if the "type" key in that value dict changes.
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


def default_collate_with_dim(batch,device='cpu',dim=0, k=None,cat=False):
    r"""Puts each data field into a tensor with outer dimension batch size"""
    elem = batch[0]
    elem_type = type(elem)
    #if k is not None:
    #    print(k)

    if isinstance(elem, torch.Tensor):
        out = None
        if torch.utils.data.get_worker_info() is not None:
            # If we're in a background process, concatenate directly into a
            # shared memory tensor to avoid an extra copy
            numel = sum([x.numel() for x in batch])
            storage = elem.storage()._new_shared(numel)
            out = elem.new(storage)
        try:
            if cat == True:
                return torch.cat(batch, dim=dim, out=out).to(device=device)
            else:
                return torch.stack(batch, dim=dim, out=out).to(device=device)
        except:
            print(batch)
            if k is not None:
                print(k)
    elif elem_type.__module__ == 'numpy' and elem_type.__name__ != 'str_' \
            and elem_type.__name__ != 'string_':
        if elem_type.__name__ == 'ndarray' or elem_type.__name__ == 'memmap':
            # array of string classes and object
            if np_str_obj_array_pattern.search(elem.dtype.str) is not None:
                raise TypeError(default_collate_err_msg_format.format(elem.dtype))

            return default_collate_with_dim([torch.as_tensor(b,device=device) for b in batch],device=device,dim=dim,cat=cat)
        elif elem.shape == ():  # scalars
            try:
                return torch.as_tensor(batch,device=device)
            except:
                print(batch)
                if k is not None:
                    print(k)
    elif isinstance(elem, float):
        try:
            return torch.tensor(batch,device=device)
        except:
            print(batch)
            if k is not None:
                print(k)
    elif isinstance(elem, int_classes):
        try:
            return torch.tensor(batch,device=device)
        except:
            print(batch)
            if k is not None:
                print(k)
    elif isinstance(elem, string_classes):
        return batch
    elif isinstance(elem, container_abcs.Mapping):
        return {key: default_collate_with_dim([d[key] for d in batch if key in d.keys()],device=device,dim=dim, k=key, cat=cat) for key in elem}
    elif isinstance(elem, tuple) and hasattr(elem, '_fields'):  # namedtuple
        return elem_type(*(default_collate_with_dim(samples,device=device,dim=dim,cat=cat) for samples in zip(*batch)))
    elif isinstance(elem, container_abcs.Sequence):
        # check to make sure that the elements in batch have consistent size
        it = iter(batch)
        elem_size = len(next(it))
        if not all(len(elem) == elem_size for elem in it):
            raise RuntimeError('each element in list of batch should be of equal size')
        transposed = zip(*batch)
        return [default_collate_with_dim(samples,device=device,dim=dim,cat=cat) for samples in transposed]

    raise TypeError(default_collate_err_msg_format.format(elem_type))