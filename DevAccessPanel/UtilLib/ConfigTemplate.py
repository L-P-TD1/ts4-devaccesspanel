"""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
TwelfthDoctor1's Developer/Debug Access Panel

> ConfigTemplate

(C) Copyright TD1 & TWoCC 2020 - 2021
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Licensed under MIT License

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

Codes from other parties are not part of the License and Copyright.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""
# ======================================================================================================================
# DEFAULT CONFIGURATION FILE
# This is the default settings for the config file (in .json)
#
# JSON Methodology make use of Python Dictionaries, thereby simplifying
# addition, deletion, and modification processes.
#
# Ensure that the keys are UNIQUE. Also ensure that the keys in code FULLY MATCH
# those written here, or else an error will occur inferring that the key does not exist.
#
# Default values can either be set from here for in UI via value. However, it is recommended to do it here instead.

CONFIG_NAME = "TD1_AccessPanel_Settings"  # Name of Config File
CONFIG_DEFAULT = {
    'disable_notifs': False,
    'override_debug_menu': True,
    'force_debug_cheat_menu': True,
    'allow_selectable_pets': False,
    'override_pack_testset': False,
    'override_integration_testset': False,
    'override_version_testset': False,
    'cheat_debug_pie_menu': False,
    'ep08_org_rank_decay_lock': False,
    'ep06_fame_rank_decay_lock': False,
    'ep06_fame_quirks_decay_lock': False,
    "drgluon_glubee_feature_unlock": False,
    "dev_show_int_tuning_name": False,
    "phone_int_cheat": False
}

CONFIG_CHANGE_SHOW = {
    'disable_notifs': True,
    'override_debug_menu': True,
    'force_debug_cheat_menu': True,
    'allow_selectable_pets': True,
    'override_pack_testset': False,
    'override_integration_testset': False,
    'override_version_testset': False,
    'cheat_debug_pie_menu': True,
    'ep08_org_rank_decay_lock': True,
    'ep06_fame_rank_decay_lock': True,
    'ep06_fame_quirks_decay_lock': True,
    "drgluon_glubee_feature_unlock": True,
    "dev_show_int_tuning_name": True,
    "phone_int_cheat": True
}
# ======================================================================================================================
