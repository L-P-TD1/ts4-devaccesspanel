"""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
TwelfthDoctor1's Developer/Debug Access Panel

> ModCheck & Integration Tuning

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
import enum
import services
from sims4.commands import Command
from sims4.localization import LocalizationHelperTuning
from ui.ui_dialog_notification import UiDialogNotification
from DevAccessPanel.MainLib.TD1_DevAccessPanel_ModuleHandler import MAIN_SERVICE

# Importation of MasterApprentice Logger
try:
    from MasterApprenticeLib.TD1_Lib_ApprenticeLogger import ApprenticeLogger

    apprentice_logger = ApprenticeLogger('TD1 Developer/Debug Access Panel Mod Check', main_owner='TwelfthDoctor1')

except ImportError:
    apprentice_logger = False

try:
    from MasterApprenticeLib.TD1_Lib_MasterLogger import MasterLogger

    master_logger = MasterLogger('TD1 Developer/Debug Access Panel Mod Check', main_owner='TwelfthDoctor1')

except ImportError:
    master_logger = False


class IntegrationEnums(enum.Int):
    NONE = 0
    MASTER_SPELLS = 1
    TMS = 2
    UNLOCK_RECIPES = 3
    CUSTOM_LOANS = 4
    UNLOCK_REWARDS = 5
    OCCULT_HYBRID = 6


def is_available_integration(integration):
    try:
        import TD1_MasterSpells_ModuleHandler
        result_1 = True

    except ImportError:
        result_1 = False

    try:
        from TMS.MainLib import TD1_TMS_ModuleHandler
        result_2 = True

    except ImportError:
        result_2 = False

    try:
        import TD1_UnlockRecipes_add_interactions_to_sims_under_basegame
        result_3 = True

    except ImportError:
        result_3 = False

    try:
        import TD1_Loans_CustomLoanTuning
        result_4 = True

    except ImportError:
        result_4 = False

    try:
        import TD1_UnlockRewards_ModuleHandler
        result_5 = True

    except ImportError:
        result_5 = False

    try:
        import OccultHybrid.Modules.TD1_OccultHybrid_OccultCMDs
        result_6 = True

    except ImportError:
        result_6 = False

    if integration == IntegrationEnums.MASTER_SPELLS and result_1 is True:
        return True
    elif integration == IntegrationEnums.TMS and result_2 is True:
        return True
    elif integration == IntegrationEnums.UNLOCK_RECIPES and result_3 is True:
        return True
    elif integration == IntegrationEnums.CUSTOM_LOANS and result_4 is True:
        return True
    elif integration == IntegrationEnums.UNLOCK_REWARDS and result_5 is True:
        return True
    elif integration == IntegrationEnums.OCCULT_HYBRID and result_6 is True:
        return True
    else:
        return False


@Command('td1devaccess.get_integration')
def get_integration_mods(_connection=None):
    client = services.client_manager().get_first_client()
    try:
        import TD1_MasterSpells_ModuleHandler
        result_1 = True

    except ImportError:
        result_1 = False

    try:
        from TMS.MainLib import TD1_TMS_ModuleHandler
        result_2 = True

    except ImportError:
        result_2 = False

    try:
        import TD1_UnlockRecipes_add_interactions_to_sims_under_basegame
        result_3 = True

    except ImportError:
        result_3 = False

    try:
        import TD1_Loans_CustomLoanTuning
        result_4 = True

    except ImportError:
        result_4 = False

    try:
        import TD1_UnlockRewards_ModuleHandler
        result_5 = True

    except ImportError:
        result_5 = False

    try:
        import OccultHybrid.Modules.TD1_OccultHybrid_OccultCMDs
        result_6 = True

    except ImportError:
        result_6 = False

    try:
        # Old Version TTV SM Script
        import TD1_TravelToVenue_add_phone_interaction
        travel_to_venue_status = True

    except ImportError:
        travel_to_venue_status = False

    try:
        from TravelToVenue.CoreLib import TD1_TravelToVenue_MenuUI
        ttv_struct_v2_status = True

    except ImportError:
        ttv_struct_v2_status = False

    try:
        import TD1_ForceNoChangeOutfit_add_interactions_to_sims
        outfit_lock_status = True

    except ImportError:
        outfit_lock_status = False

    status_1 = check_integration_status(result_1)
    status_2 = check_integration_status(result_2)
    status_3 = check_integration_status(result_3)
    status_4 = check_integration_status(result_4)
    status_5 = check_integration_status(result_5)
    status_6 = check_integration_status(result_6)
    travel_to_venue_standalone_check(travel_to_venue_status, ttv_struct_v2_status)
    outfitlock_standalone_check(outfit_lock_status)

    text_1 = '[Sage of Mastery Magic + Mastery Spells]\nStatus: ' + status_1
    text_2 = '[Teleport Memory System]\nStatus: ' + status_2
    text_3 = '[Unlock Recipes]\nStatus: ' + status_3
    text_4 = '[TD1 Custom Loans & Bank Services]\nStatus: ' + status_4
    text_5 = '[Unlock Rewards]\nStatus: ' + status_5
    text_6 = '[Occult Hybrid Handler]\nStatus: ' + status_6

    last_text = 'Should you find that something is wrong with the Integration Status, please check your Mods Folder.'

    text_final = text_1 + '\n\n' + text_2 + '\n\n' + text_3 + '\n\n' + text_4 + '\n\n' + text_5 + '\n\n' + text_6 + \
                 '\n\n' + last_text

    message_title = lambda **_: LocalizationHelperTuning.get_raw_text("TD1 Developer Access Panel Mod Integrations")
    message_text = lambda **_: LocalizationHelperTuning.get_raw_text(text_final)

    notification = UiDialogNotification.TunableFactory().default(
        client.active_sim,
        text=message_text,
        title=message_title,
        expand_behavior=UiDialogNotification.UiDialogNotificationExpandBehavior.FORCE_EXPAND,
    )
    notification.show_dialog()


def check_integration_status(result):
    if result is True:
        status = '[INSTALLED]'
        return status
    else:
        status = '[NOT INSTALLED]'
        return status


def travel_to_venue_standalone_check(result1, result2):
    client = services.client_manager().get_first_client()
    if result1 is True or result2 is True:

        message_title_ttv = lambda **_: LocalizationHelperTuning.get_raw_text("Travel To Venue Standalone Mod Detected")
        message_text_ttv = lambda **_: LocalizationHelperTuning.get_raw_text(
            "The Travel To Venue Standalone Mod has been detected in your Mods Folder. <b>Please remove it from your Mods Folder.</b>\n\nIf you need help, please check with TwelfthDoctor1 via Discord or Patreon if needed.")

        notification_ttv = UiDialogNotification.TunableFactory().default(
            client.active_sim,
            text=message_text_ttv,
            title=message_title_ttv,
            expand_behavior=UiDialogNotification.UiDialogNotificationExpandBehavior.FORCE_EXPAND,
            urgency=UiDialogNotification.UiDialogNotificationUrgency.URGENT
        )
        notification_ttv.show_dialog()

        if apprentice_logger is not None and apprentice_logger is not False:
            apprentice_logger.warn("Please remove the Travel To Venue Standalone Mod from your Mods Folder.",
                                   owner="TwelfthDoctor1")

        if master_logger is not None and master_logger is not False:
            master_logger.warn("Please remove the Travel To Venue Standalone Mod from your Mods Folder.",
                               owner="TwelfthDoctor1")

        MAIN_SERVICE.warn_service(
            f"[MOD COMPATIBILITY CHECK]: Travel To Venue Standalone Mod is detected in Mods Folder. "
            f"Continued use of both mods will lead to LEs, please remove it.")

        return
    else:
        return


def outfitlock_standalone_check(result):
    client = services.client_manager().get_first_client()
    if result is True:

        message_title_ol = lambda **_: LocalizationHelperTuning.get_raw_text(
            "Force No Change Outfit Standalone Mod Detected")
        message_text_ol = lambda **_: LocalizationHelperTuning.get_raw_text(
            "The Force No Change Outfit Standalone Mod has been detected in your Mods Folder. <b>Please remove it from your Mods Folder.</b>\n\nIf you need help, please check with TwelfthDoctor1 via Discord or Patreon if needed.")

        notification_ol = UiDialogNotification.TunableFactory().default(
            client.active_sim,
            text=message_text_ol,
            title=message_title_ol,
            expand_behavior=UiDialogNotification.UiDialogNotificationExpandBehavior.FORCE_EXPAND,
            urgency=UiDialogNotification.UiDialogNotificationUrgency.URGENT
        )
        notification_ol.show_dialog()

        if apprentice_logger is not None and apprentice_logger is not False:
            apprentice_logger.warn("Please remove the Force No Change Outfit Standalone Mod from your Mods Folder.",
                                   owner="TwelfthDoctor1")

        if master_logger is not None and master_logger is not False:
            master_logger.warn("Please remove the Force No Change Outfit Standalone Mod from your Mods Folder.",
                               owner="TwelfthDoctor1")

        MAIN_SERVICE.warn_service(
            f"[MOD COMPATIBILITY CHECK]: Force No Change Outfit Standalone Mod is detected in Mods Folder. "
            f"Continued use of both mods will lead to LEs, please remove it.")

        return
    else:
        return
