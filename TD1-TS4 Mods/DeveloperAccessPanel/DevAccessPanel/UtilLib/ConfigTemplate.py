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
