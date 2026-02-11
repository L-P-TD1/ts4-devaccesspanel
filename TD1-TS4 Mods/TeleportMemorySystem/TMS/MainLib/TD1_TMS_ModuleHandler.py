"""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
TwelfthDoctor1's Teleport Memory System

> ModuleHandler Tuning

(C) Copyright TD1 & TWoCC 2020 - 2021
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Licensed under CC-BY-NC-ND 4.0

https://creativecommons.org/licenses/by-nc-nd/4.0/

Codes from other parties are not part of the License and Copyright.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""
import webbrowser
import services
from TMS.MainLib.TD1_TMS_Config import get_option_value
from distributor.shared_messages import IconInfoData
from sims4.collections import make_immutable_slots_class
from sims4.common import Pack
from sims4.localization import LocalizationHelperTuning, _create_localized_string
from sims4.resources import Types, get_resource_key
from sims4.tuning.tunable import TunableReference, Tunable, TunableList, TunableTuple, TunableEnumEntry
from TMS.MainLib import injector
from sims.sim_info_manager import SimInfoManager
from sims.sim_info_types import Species
from ui.ui_dialog import ButtonType, UiDialogResponse
from ui.ui_dialog_notification import UiDialogNotification
from sims4.commands import Command, CommandType, CheatOutput, execute
from sims4.log import Logger

# Importation of MasterApprentice Logger
try:
    from MasterApprenticeLib.TD1_Lib_ApprenticeLogger import ApprenticeLogger
    apprentice_logger = ApprenticeLogger('TD1 Teleport Memory System Module Handler', main_owner='TwelfthDoctor1')

except ImportError:
    apprentice_logger = False

try:
    from MasterApprenticeLib.TD1_Lib_MasterLogger import MasterLogger
    master_logger = MasterLogger('TD1 Teleport Memory System Module Handler', main_owner='TwelfthDoctor1')

except ImportError:
    master_logger = False

logger = Logger('TD1 Teleport Memory System Module Handler', default_owner='TwelfthDoctor1')

"""
Module Notation: This Module Tuning is an important factor in many of the TMS features.

Section 1: AutoAdd Tunables
The AutoAdd feature can be toggled should it not be required for a teleport type. By default, it will be set to
False if unused.

Section 2: Teleport Enabled Traits
Part of the AutoAdd Mechanics, it is used as a reference for the function later on.

Section 3: TMS Traits
Also past of the AutoAdd Mechanics, it is used to give the relevant trait from the function.

Section 4: Pack Allocation
Used in the TeleportPack Test, it is used to store the relevant Packs.

Section 5: Startup Notifications
Part of the Startup Inits, it holds the notification code to be used on load complete.

Section 6: Startup Notification Control
Controls whether which notification should be used.
"""


class TD1TMSModuleHandler:
    WELLNESS_TMS_AUTOADD = Tunable(
        description='Whether the Wellness TMS Trait will be auto added onto Sims on load',
        tunable_type=bool,
        default=False
    )
    VAMPIRE_BAT_TMS_AUTOADD = Tunable(
        description='Whether the Vampire Bat TMS Trait will be auto added onto Sims on load',
        tunable_type=bool,
        default=False
    )
    VAMPIRE_MIST_TMS_AUTOADD = Tunable(
        description='Whether the Vampire Mist TMS Trait will be auto added onto Sims on load',
        tunable_type=bool,
        default=False
    )
    VAMPIRE_RUN_TMS_AUTOADD = Tunable(
        description='Whether the Vampire Run TMS Trait will be auto added onto Sims on load',
        tunable_type=bool,
        default=False
    )
    WITCH_SPELL_TMS_AUTOADD = Tunable(
        description='Whether the Witch Spell TMS Trait will be auto added onto sims on load',
        tunable_type=bool,
        default=False
    )
    WITCH_BROOMS_TMS_AUTOADD = Tunable(
        description='Whether the Witch Brooms TMS Trait will be auto added onto sims on load',
        tunable_type=bool,
        default=False
    )
    WEREWOLF_SUPER_SPEED_TMS_AUTOADD = Tunable(
        description='Whether the Werewolf Super Speed TMS Trait will be auto added onto sims on load',
        tunable_type=bool,
        default=False
    )
    GHOST_TELEPORT_TMS_AUTOADD = Tunable(
        description='Whether the Ghost Teleport TMS Trait will be auto added onto sims on load',
        tunable_type=bool,
        default=False
    )
    SPACEBEND_TELEPORT_TMS_AUTOADD = Tunable(
        description='Whether the Spacebend Teleport TMS Trait will be auto added onto sims on load',
        tunable_type=bool,
        default=False
    )
    FAIRY_TELEPORT_TMS_AUTOADD = Tunable(
        description='Whether the Fairy Teleport TMS Trait will be auto added onto sims on load',
        tunable_type=bool,
        default=False
    )
    FAIRY_WALKSTYLE_TMS_AUTOADD = Tunable(
        description='Whether the Fairy Walkstyle TMS Trait will be auto added onto sims on load',
        tunable_type=bool,
        default=False
    )
    TD1_DARK_ARRARATE_SPELL_TMS_AUTOADD = Tunable(
        description='Whether the Dark Apparate Spell TMS Trait will be auto added on load',
        tunable_type=bool,
        default=False
    )
    TD1_MIST_SPELL_TMS_AUTOADD = Tunable(
        description='Whether the Mist Spell TMS Trait wil be auto added onto sims on load',
        tunable_type=bool,
        default=False
    )
    TD1_BAT_SPELL_TMS_AUTOADD = Tunable(
        description='Whether the Bat Spell TMS Trait will be auto added onto sims on load',
        tunable_type=bool,
        default=False
    )
    TD1_RUN_SPELL_TMS_AUTOADD = Tunable(
        description='Whether the Run Spell TMS Trait will be auto added onto sims on load',
        tunable_type=bool,
        default=False
    )
    PET_TELEPORT_TMS_AUTOADD = Tunable(
        description='Whether the Run Spell TMS Trait will be auto added onto sims on load',
        tunable_type=bool,
        default=False
    )
    WELLNESS_TELEPORT_ENABLED_TRAIT = TunableReference(
        description='Tuning Instance of the Wellness Teleport Enabled Trait',
        manager=services.trait_manager()
    )
    VAMPIRE_BAT_TELEPORT_ENABLED_TRAIT = TunableReference(
        description='Tuning Instance of the Vampire Bat Teleport Enabled Trait',
        manager=services.trait_manager()
    )
    VAMPIRE_MIST_TELEPORT_ENABLED_TRAIT = TunableReference(
        description='Tuning Instance of the Vampire Mist Teleport Enabled Trait',
        manager=services.trait_manager()
    )
    VAMPIRE_RUN_WALKSTYLE_ENABLED_TRAIT = TunableReference(
        description='Tuning Instance of the Vampire Run Walkstyle Enabled Trait',
        manager=services.trait_manager()
    )
    WITCH_SPELL_TELEPORT_ENABLED_TRAIT = TunableReference(
        description='Tuning Instance of the Witch Teleport Spell Teleport Enabled Trait',
        manager=services.trait_manager()
    )
    WITCH_BROOMS_TELEPORT_ENABLED_TRAIT = TunableReference(
        description='Tuning Instance of the Witch Broom Teleport Enabled Trait',
        manager=services.trait_manager()
    )
    WEREWOLF_SUPER_SPEED_WALKSTYLE_ENABLED_TRAIT = TunableReference(
        description='Tuning Instance of the Werewolf Super Run Walkstyle Enabled Trait',
        manager=services.trait_manager()
    )
    GHOST_TELEPORT_ENABLED_TRAIT = TunableReference(
        description='Tuning Instance of the Ghost Teleport Enabled Trait',
        manager=services.trait_manager()
    )
    SPACEBEND_TELEPORT_ENABLED_TRAIT = TunableReference(
        description='Tuning Instance of the Spacebend Teleport Enabled Trait',
        manager=services.trait_manager()
    )
    FAIRY_TELEPORT_ENABLED_TRAIT = TunableReference(
        description='Tuning Instance of the Fairy Teleport Enabled Trait',
        manager=services.trait_manager()
    )
    FAIRY_WALKSTYLE_ENABLED_TRAIT = TunableReference(
        description='Tuning Instance of the Fairy Walkstyle Enabled Trait',
        manager=services.trait_manager()
    )
    TD1_DARK_APPARATE_SPELL_TELEPORT_ENABLED_TRAIT = TunableReference(
        description='Tuning Instance of the Dark Apparate Spell Teleport Enabled Trait',
        manager=services.trait_manager()
    )
    TD1_MIST_SPELL_TELEPORT_ENABLED_TRAIT = TunableReference(
        description='Tuning Instance of the Mist Spell Teleport Enabled Trait',
        manager=services.trait_manager()
    )
    TD1_BAT_SPELL_TELEPORT_ENABLED_TRAIT = TunableReference(
        description='Tuning Instance of the Bat Spell Teleport Enabled Trait',
        manager=services.trait_manager()
    )
    TD1_RUN_SPELL_WALKSTYLE_ENABLED_TRAIT = TunableReference(
        description='Tuning Instance of the Run Spell Walkstyle Enabled Trait',
        manager=services.trait_manager()
    )
    PET_TELEPORT_ENABLED_TRAIT = TunableReference(
        description='Tuning Instance of the Run Spell Walkstyle Enabled Trait',
        manager=services.trait_manager()
    )
    WELLNESS_TMS_TRAIT = TunableReference(
        description='Tuning Instance of the Wellness TMS Trait',
        manager=services.trait_manager()
    )
    VAMPIRE_BAT_TMS_TRAIT = TunableReference(
        description='Tuning Instance of the Vampire Bat TMS Trait',
        manager=services.trait_manager()
    )
    VAMPIRE_MIST_TMS_TRAIT = TunableReference(
        description='Tuning Instance of the Vampire Mist TMS Trait',
        manager=services.trait_manager()
    )
    VAMPIRE_RUN_TMS_TRAIT = TunableReference(
        description='Tuning Instance of the Vampire Run TMS Trait',
        manager=services.trait_manager()
    )
    WITCH_SPELL_TMS_TRAIT = TunableReference(
        description='Tuning Instance of the Witch Teleport Spell TMS Trait',
        manager=services.trait_manager()
    )
    WITCH_BROOMS_TMS_TRAIT = TunableReference(
        description='Tuning Instance of the Witch Broom TMS Trait',
        manager=services.trait_manager()
    )
    WEREWOLF_SUPER_SPEED_TMS_TRAIT = TunableReference(
        description='Tuning Instance of the Werewolf Super Speed TMS Trait',
        manager=services.trait_manager()
    )
    GHOST_TELEPORT_TMS_TRAIT = TunableReference(
        description='Tuning Instance of the Ghost Teleport TMS Trait',
        manager=services.trait_manager()
    )
    SPACEBEND_TELEPORT_TMS_TRAIT = TunableReference(
        description='Tuning Instance of the Spacebend Teleport TMS Trait',
        manager=services.trait_manager()
    )
    FAIRY_TELEPORT_TMS_TRAIT = TunableReference(
        description='Tuning Instance of the Fairy Teleport TMS Trait',
        manager=services.trait_manager()
    )
    FAIRY_WALKSTYLE_TMS_TRAIT = TunableReference(
        description='Tuning Instance of the Fairy Walkstyle TMS Trait',
        manager=services.trait_manager()
    )
    TD1_DARK_APPARATE_SPELL_TMS_TRAIT = TunableReference(
        description='Tuning Instance of the Dark Apparate Spell TMS Trait',
        manager=services.trait_manager()
    )
    TD1_MIST_SPELL_TMS_TRAIT = TunableReference(
        description='Tuning Instance of the Mist Spell TMS Trait',
        manager=services.trait_manager()
    )
    TD1_BAT_SPELL_TMS_TRAIT = TunableReference(
        description='Tuning Instance of the Bat Spell TMS Trait',
        manager=services.trait_manager()
    )
    TD1_RUN_SPELL_TMS_TRAIT = TunableReference(
        description='Tuning Instance of the Run Spell TMS Trait',
        manager=services.trait_manager()
    )
    PET_TELEPORT_TMS_TRAIT = TunableReference(
        description='Tuning Instance of the Run Spell TMS Trait',
        manager=services.trait_manager()
    )
    WELLNESS_TELEPORT_PACK = TunableEnumEntry(
        description='The pack which has the Wellness Teleport components',
        tunable_type=Pack,
        default=Pack.BASE_GAME
    )
    VAMPIRE_BAT_TELEPORT_PACK = TunableEnumEntry(
        description='The pack which has the Vampire Bat Teleport components',
        tunable_type=Pack,
        default=Pack.BASE_GAME
    )
    VAMPIRE_MIST_TELEPORT_PACK = TunableEnumEntry(
        description='The pack which has the Vampire Mist Teleport components',
        tunable_type=Pack,
        default=Pack.BASE_GAME
    )
    VAMPIRE_RUN_WALKSTYLE_PACK = TunableEnumEntry(
        description='The pack which has the Vampire Run Walkstyle components',
        tunable_type=Pack,
        default=Pack.BASE_GAME
    )
    WITCH_SPELL_TELEPORT_PACK = TunableEnumEntry(
        description='The pack which has the Witch Teleport components',
        tunable_type=Pack,
        default=Pack.BASE_GAME
    )
    WITCH_BROOMS_TELEPORT_PACK = TunableEnumEntry(
        description='The pack which has the Brooms Teleport components',
        tunable_type=Pack,
        default=Pack.BASE_GAME
    )
    WEREWOLF_SUPER_SPEED_WALKSTYLE_PACK = TunableEnumEntry(
        description='The pack which has the Werewolf Super Speed components',
        tunable_type=Pack,
        default=Pack.BASE_GAME
    )
    PET_TELEPORT_PACK = TunableEnumEntry(
        description='The pack which has the Pet Teleport components',
        tunable_type=Pack,
        default=Pack.BASE_GAME
    )
    GHOST_TELEPORT_PACK = TunableEnumEntry(
        description='The pack which has the Ghost Teleport components',
        tunable_type=Pack,
        default=Pack.BASE_GAME
    )
    SPACEBEND_TELEPORT_PACK = TunableEnumEntry(
        description='The pack which has the Spacebend Teleport components',
        tunable_type=Pack,
        default=Pack.BASE_GAME
    )
    FAIRY_TELEPORT_PACK = TunableEnumEntry(
        description='The pack which has the Fairy Teleport components',
        tunable_type=Pack,
        default=Pack.BASE_GAME
    )
    FAIRY_WALKSTYLE_PACK = TunableEnumEntry(
        description='The pack which has the Fairy Walkstyle components',
        tunable_type=Pack,
        default=Pack.BASE_GAME
    )
    TMS_STARTUP_NOTIFICATION = UiDialogNotification.TunableFactory(
        description='The notification to be used on game load, used on release versions'
    )
    TMS_DEVELOPER_STARTUP_NOTIFICATION = UiDialogNotification.TunableFactory(
        description='The developer notification to be used on game load, developer use only'
    )
    TMS_BETA_STARTUP_NOTIFICATION = UiDialogNotification.TunableFactory(
        description='The beta notification to be used on game load, mainly for beta testers'
    )
    TMS_ALLOW_STARTUP_NOTIFICATION = Tunable(
        description='Whether the startup should show up on load',
        tunable_type=bool,
        default=True
    )
    TMS_ALLOW_DEVELOPER_STARTUP_NOTIFICATION = Tunable(
        description='Whether the developer startup should show up on load',
        tunable_type=bool,
        default=False
    )
    TMS_ALLOW_BETA_STARTUP_NOTIFICATION = Tunable(
        description='Whether the beta startup should show up on load',
        tunable_type=bool,
        default=False
    )
    TMS_MOD_VERSION = Tunable(
        description='Current mod version. Used for Mod Verification and Testing.',
        tunable_type=str,
        default=''
    )
    TMS_IGNORE_MOD_VERSION = Tunable(
        description='Controls the Version Mismatch Test. If ignored, Version Mismatch Test will not flag up errors should versions be different.',
        tunable_type=bool,
        default=False
    )
    TMS_STARTUP_NOTIFICATION_V2_USAGE = Tunable(
        description='Controls usage of which version of the Startup Notification should be used. If disabled, Version 1 will be used. If enabled, Version 2 will be used.',
        tunable_type=bool,
        default=True
    )
    notification_ran = False
    mod_version = "Version 2.21.2 Build"


# Command Handling Section
# Note: Secnario Var - If 1, then Notif will show up, for all other numbers not 1 excluding 0, Notif will not show with Indication that Tuning is set to Disabled.

@Command('tms.show_version', command_type=CommandType.Live)
def show_version(scenario:int=0, _connection=None):
    output = CheatOutput(_connection)
    if scenario is 0:
        if TD1TMSModuleHandler.TMS_ALLOW_STARTUP_NOTIFICATION is True:
            startup_notification = TD1TMSModuleHandler.TMS_STARTUP_NOTIFICATION(None)
            startup_notification.show_dialog()
        else:
            output('Startup Notification Disabled, it can be enabled via the TD1_TMS_ModuleHandler Tuning')
    elif scenario is 1:
        startup_notification = TD1TMSModuleHandler.TMS_STARTUP_NOTIFICATION(None)
        startup_notification.show_dialog()
    else:
        output('Startup Notification Disabled, it can be enabled via the TD1_TMS_ModuleHandler Tuning')


@Command('tms.show_dev_version', command_type=CommandType.Live)
def show_dev_version(scenario:int=0, _connection=None):
    output = CheatOutput(_connection)
    if scenario is 0:
        if TD1TMSModuleHandler.TMS_ALLOW_DEVELOPER_STARTUP_NOTIFICATION is True:
            startup_notification = TD1TMSModuleHandler.TMS_DEVELOPER_STARTUP_NOTIFICATION(None)
            startup_notification.show_dialog()
        else:
            output('Developer Startup Notification Disabled, it can be enabled via the TD1_TMS_ModuleHandler Tuning. However, this should only be done by TwelfthDoctor1.')
    elif scenario is 1:
        developer_startup_notification = TD1TMSModuleHandler.TMS_DEVELOPER_STARTUP_NOTIFICATION(None)
        developer_startup_notification.show_dialog()
    else:
        output('Developer Startup Notification Disabled, it can be enabled via the TD1_TMS_ModuleHandler Tuning. However, this should only be done by TwelfthDoctor1.')


@Command('tms.show_beta_version', command_type=CommandType.Live)
def show_dev_version(scenario:int=0, _connection=None):
    output = CheatOutput(_connection)
    if scenario is 0:
        if TD1TMSModuleHandler.TMS_ALLOW_BETA_STARTUP_NOTIFICATION is True:
            startup_notification = TD1TMSModuleHandler.TMS_BETA_STARTUP_NOTIFICATION(None)
            startup_notification.show_dialog()
        else:
            output('Beta Startup Notification Disabled, it can be enabled via the TD1_TMS_ModuleHandler Tuning. However, this should only be done by TwelfthDoctor1.')
    elif scenario is 1:
        beta_startup_notification = TD1TMSModuleHandler.TMS_BETA_STARTUP_NOTIFICATION(None)
        beta_startup_notification.show_dialog()
    else:
        output('Beta Startup Notification Disabled, it can be enabled via the TD1_TMS_ModuleHandler Tuning. However, this should only be done by TwelfthDoctor1.')


# Discord Server Invite Command to report-bugs

@Command('tms.td1_discord', command_type=CommandType.Live)
def td1_discord(_connection=None):
    output = CheatOutput(_connection)
    output('Please check your browser for the server invite.')
    webbrowser.open('https://discord.gg/waHpcSHZwb')  # This link opens up Discord to invite the user to TD1 Community Server (3.0) for bug reporting


@Command('tms.td1_patreon', command_type=CommandType.Live)
def td1_patreon(_connection=None):
    output = CheatOutput(_connection)
    output('Please check your browser for the server invite.')
    webbrowser.open('https://www.patreon.com/twelfthdoctor1')  # This link opens up the Patreon Page


# Inject On Load Complete

@injector.inject_to(SimInfoManager, 'on_loading_screen_animation_finished')
def td1_tms_add_tms_traits_to_sim_on_load(original, self, *args, **kwargs):
    result = original(self, *args, **kwargs)

    if TD1TMSModuleHandler.notification_ran is True:

        return

    try:

        tms_version_control()
        td1_tms_startup_notification_handler()
        # execute("tms.convert_cfg_to_json", None)

        TD1TMSModuleHandler.notification_ran = True

        for sim_info in services.sim_info_manager().get_all():
            td1_tms_auto_add_traits_handler(sim_info)
    except Exception as e:

        if apprentice_logger is not False and apprentice_logger is not None:
            apprentice_logger.error(f"Error found with Teleport Memory System Module Handler: {str(e)}",
                                    owner="TwelfthDoctor1")

        if master_logger is not False and apprentice_logger is not None:
            master_logger.error(f"Error found with Teleport Memory System Module Handler: {str(e)}",
                                owner="TwelfthDoctor1")

        raise Exception(f"Error found with Teleport Memory System Module Handler by TwelfthDoctor1: {str(e)}")

    return result


def td1_tms_startup_notification_handler():

    if apprentice_logger is not None and apprentice_logger is not False:
        apprentice_logger.info("TD1 Teleport Memory System Version Control\n\nPackage Version: {}\nScript Version: {}".format(
            TD1TMSModuleHandler.TMS_MOD_VERSION, TD1TMSModuleHandler.mod_version
        ))

    if master_logger is not None and master_logger is not False:
        master_logger.info("TD1 Teleport Memory System Version Control\n\nPackage Version: {}\nScript Version: {}".format(
            TD1TMSModuleHandler.TMS_MOD_VERSION, TD1TMSModuleHandler.mod_version
        ))

    if get_option_value('disable_notifs') is True:
        return

    if TD1TMSModuleHandler.TMS_STARTUP_NOTIFICATION_V2_USAGE is True:
        execute('tms.show_version_v2', None)
    else:
        if TD1TMSModuleHandler.TMS_ALLOW_STARTUP_NOTIFICATION is True:
            execute('tms.show_version 1', None)
        else:
            execute('tms.show_version 2', None)

        if TD1TMSModuleHandler.TMS_ALLOW_DEVELOPER_STARTUP_NOTIFICATION is True:
            execute('tms.show_dev_version 1', None)
        else:
            execute('tms.show_dev_version 2', None)

        if TD1TMSModuleHandler.TMS_ALLOW_BETA_STARTUP_NOTIFICATION is True:
            execute('tms.show_beta_version 1', None)
        else:
            execute('tms.show_beta_version 2', None)


@Command('tms.show_version_v2', command_type=CommandType.Live)
def mod_version_startup_notif_v2(scenario:int=0, _connection=None):
    client = services.client_manager().get_first_client()
    output = CheatOutput(_connection)
    button1_text = None
    button2_text = None
    button3_text = None
    notif_title = None
    notif_text = None
    info_level = None
    visual = None

    if TD1TMSModuleHandler.TMS_STARTUP_NOTIFICATION_V2_USAGE is False and scenario == 0:
        output("Version 2 Startup Notification Disabled, it can be changed via the TD1_TMS_ModuleHandler Tuning. Note that it should only be done by TwelfthDoctor1.")
        if TD1TMSModuleHandler.TMS_ALLOW_DEVELOPER_STARTUP_NOTIFICATION is True:
            output("\nFor Notification Testing, the Variable: Scenario can be modified to use values 1 to 3.")

    if TD1TMSModuleHandler.TMS_ALLOW_STARTUP_NOTIFICATION is True or scenario == 1:
        notif_title = lambda **_: _create_localized_string(0x21444530)
        notif_text = lambda **_: _create_localized_string(0x21444538, str(TD1TMSModuleHandler.TMS_MOD_VERSION), str(TD1TMSModuleHandler.mod_version))
        info_level = UiDialogNotification.UiDialogNotificationLevel.PLAYER
        visual = UiDialogNotification.UiDialogNotificationVisualType.INFORMATION
        button1_text = lambda **_: _create_localized_string(0x2144453B)
        button2_text = lambda **_: _create_localized_string(0x2144453C)
        # button3_text = lambda **_: _create_localized_string(0x2144453D)

    elif TD1TMSModuleHandler.TMS_ALLOW_DEVELOPER_STARTUP_NOTIFICATION is True or scenario == 2:
        notif_title = lambda **_: _create_localized_string(0x21444532)
        notif_text = lambda **_: _create_localized_string(0x21444539, str(TD1TMSModuleHandler.TMS_MOD_VERSION), str(TD1TMSModuleHandler.mod_version))
        info_level = UiDialogNotification.UiDialogNotificationLevel.SIM
        visual = UiDialogNotification.UiDialogNotificationVisualType.SPECIAL_MOMENT
        button1_text = lambda **_: _create_localized_string(0x2144453B)
        button2_text = lambda **_: _create_localized_string(0x2144453C)
        # button3_text = lambda **_: _create_localized_string(0x2144453D)

    elif TD1TMSModuleHandler.TMS_ALLOW_BETA_STARTUP_NOTIFICATION is True or scenario == 3:
        notif_title = lambda **_: _create_localized_string(0x21444534)
        notif_text = lambda **_: _create_localized_string(0x2144453A, str(TD1TMSModuleHandler.TMS_MOD_VERSION), str(TD1TMSModuleHandler.mod_version))
        info_level = UiDialogNotification.UiDialogNotificationLevel.SIM
        visual = UiDialogNotification.UiDialogNotificationVisualType.INFORMATION
        button1_text = lambda **_: _create_localized_string(0x2144453B)
        button2_text = lambda **_: _create_localized_string(0x2144453C)
        # button3_text = lambda **_: _create_localized_string(0x2144453D)

    # Button Control
    # 1. Discord
    # 2. Patreon

    button1_response_command = make_immutable_slots_class(set(['arguments', 'command']))({'arguments': (), 'command': 'tms.td1_discord'})
    button2_response_command = make_immutable_slots_class(set(['arguments', 'command']))({'arguments': (), 'command': 'tms.td1_patreon'})
    # button3_response_command = make_immutable_slots_class(set(['arguments', 'command']))({'arguments': (), 'command': 'tms.td1_dev_update'})

    button1_response = UiDialogResponse(
        dialog_response_id=ButtonType.DIALOG_RESPONSE_OK,
        ui_request=UiDialogResponse.UiDialogUiRequest.SEND_COMMAND,
        response_command=button1_response_command,
        text=button1_text
    )
    button2_response = UiDialogResponse(
        dialog_response_id=ButtonType.DIALOG_RESPONSE_OK,
        ui_request=UiDialogResponse.UiDialogUiRequest.SEND_COMMAND,
        response_command=button2_response_command,
        text=button2_text
    )
    # button3_response = UiDialogResponse(
    #    dialog_response_id=ButtonType.DIALOG_RESPONSE_OK,
    #    ui_request=UiDialogResponse.UiDialogUiRequest.SEND_COMMAND,
    #    response_command=button3_response_command,
    #    text=button3_text
    # )

    notification_startup = UiDialogNotification.TunableFactory().default(
        client.active_sim,
        title=notif_title,
        text=notif_text,
        information_level=info_level,
        expand_behavior=UiDialogNotification.UiDialogNotificationExpandBehavior.FORCE_EXPAND,
        visual_type=visual,
        icon=lambda _: IconInfoData(
            icon_resource=get_resource_key(
                0x9D293761EB2AC213, Types.PNG
            )
        ),
        ui_responses=(
            button1_response,
            button2_response,
            # button3_response
        )
    )
    notification_startup.show_dialog()


def tms_version_control():
    client = services.client_manager().get_first_client()

    if str(TD1TMSModuleHandler.TMS_MOD_VERSION).find(TD1TMSModuleHandler.mod_version) != -1 or TD1TMSModuleHandler.TMS_IGNORE_MOD_VERSION is True:
        return
    else:
        message_title_test_fail = lambda **_: LocalizationHelperTuning.get_raw_text("TD1 TMS: Version Mismatch")
        message_text_test_fail = lambda **_: LocalizationHelperTuning.get_raw_text("Version Mismatch found. Please check if your mod package and script are updated correctly.\n\nPackage Version: " + str(TD1TMSModuleHandler.TMS_MOD_VERSION) + "\n\nScript Version: " + str(TD1TMSModuleHandler.mod_version))

        notification_test_fail = UiDialogNotification.TunableFactory().default(
            client.active_sim,
            text=message_text_test_fail,
            title=message_title_test_fail,
            expand_behavior=UiDialogNotification.UiDialogNotificationExpandBehavior.FORCE_EXPAND,
            urgency=UiDialogNotification.UiDialogNotificationUrgency.URGENT
        )
        notification_test_fail.show_dialog()

        if apprentice_logger is not False and apprentice_logger is not None:
            apprentice_logger.warn("TD1 TMS Version Mismatch Error: Please check if your version is correct.",
                                   owner="TwelfthDoctor1")

        if master_logger is not False and master_logger is not None:
            master_logger.warn("TD1 TMS Version Mismatch Error: Please rectify Script Version and Package Version or use Override.",
                               owner="TwelfthDoctor1")


# Auto Add Traits Section
def td1_tms_auto_add_traits_handler(sim_info):
    trait_manager = services.trait_manager()

    # Teleportation Enabled Traits In Game

    vampire_bat_tp_trait = trait_manager.get(TD1TMSModuleHandler.VAMPIRE_BAT_TELEPORT_ENABLED_TRAIT)
    vampire_mist_tp_trait = trait_manager.get(TD1TMSModuleHandler.VAMPIRE_MIST_TELEPORT_ENABLED_TRAIT)
    vampire_run_tp_trait = trait_manager.get(TD1TMSModuleHandler.VAMPIRE_RUN_WALKSTYLE_ENABLED_TRAIT)
    witch_teleport_spell_tp_trait = trait_manager.get(TD1TMSModuleHandler.WITCH_SPELL_TELEPORT_ENABLED_TRAIT)
    witch_brooms_tp_trait = trait_manager.get(TD1TMSModuleHandler.WITCH_BROOMS_TELEPORT_ENABLED_TRAIT)
    werewolf_run_tp_trait = trait_manager.get(TD1TMSModuleHandler.WEREWOLF_SUPER_SPEED_WALKSTYLE_ENABLED_TRAIT)
    ghost_teleport_tp_trait = trait_manager.get(TD1TMSModuleHandler.GHOST_TELEPORT_ENABLED_TRAIT)
    spacebend_teleport_tp_trait = trait_manager.get(TD1TMSModuleHandler.SPACEBEND_TELEPORT_ENABLED_TRAIT)
    fairy_teleport_tp_trait = trait_manager.get(TD1TMSModuleHandler.FAIRY_TELEPORT_ENABLED_TRAIT)
    fairy_walkstyle_tp_trait = trait_manager.get(TD1TMSModuleHandler.FAIRY_WALKSTYLE_ENABLED_TRAIT)
    td1_darkapparate_tp_trait = trait_manager.get(TD1TMSModuleHandler.TD1_DARK_APPARATE_SPELL_TELEPORT_ENABLED_TRAIT)
    td1_mist_spell_tp_trait = trait_manager.get(TD1TMSModuleHandler.TD1_MIST_SPELL_TELEPORT_ENABLED_TRAIT)
    td1_bat_spell_tp_trait = trait_manager.get(TD1TMSModuleHandler.TD1_BAT_SPELL_TELEPORT_ENABLED_TRAIT)
    td1_run_spell_tp_trait = trait_manager.get(TD1TMSModuleHandler.TD1_RUN_SPELL_WALKSTYLE_ENABLED_TRAIT)
    td1_wellness_tp_trait = trait_manager.get(TD1TMSModuleHandler.WELLNESS_TELEPORT_ENABLED_TRAIT)
    pet_tp_trait = trait_manager.get(TD1TMSModuleHandler.PET_TELEPORT_ENABLED_TRAIT)

    # TMS Traits

    vampire_bat_tms = trait_manager.get(TD1TMSModuleHandler.VAMPIRE_BAT_TMS_TRAIT)
    vampire_mist_tms = trait_manager.get(TD1TMSModuleHandler.VAMPIRE_MIST_TMS_TRAIT)
    vampire_run_tms = trait_manager.get(TD1TMSModuleHandler.VAMPIRE_RUN_TMS_TRAIT)
    witch_teleport_spell_tms = trait_manager.get(TD1TMSModuleHandler.WITCH_SPELL_TMS_TRAIT)
    witch_brooms_tms = trait_manager.get(TD1TMSModuleHandler.WITCH_BROOMS_TMS_TRAIT)
    werewolf_run_tms = trait_manager.get(TD1TMSModuleHandler.WEREWOLF_SUPER_SPEED_TMS_TRAIT)
    ghost_teleport_tms = trait_manager.get(TD1TMSModuleHandler.GHOST_TELEPORT_TMS_TRAIT)
    spacebend_teleport_tms = trait_manager.get(TD1TMSModuleHandler.SPACEBEND_TELEPORT_TMS_TRAIT)
    fairy_teleport_tms = trait_manager.get(TD1TMSModuleHandler.FAIRY_TELEPORT_TMS_TRAIT)
    fairy_walkstyle_tms = trait_manager.get(TD1TMSModuleHandler.FAIRY_WALKSTYLE_TMS_TRAIT)
    td1_darkapparate_tms = trait_manager.get(TD1TMSModuleHandler.TD1_DARK_APPARATE_SPELL_TMS_TRAIT)
    td1_mist_spell_tms = trait_manager.get(TD1TMSModuleHandler.TD1_MIST_SPELL_TMS_TRAIT)
    td1_bat_spell_tms = trait_manager.get(TD1TMSModuleHandler.TD1_BAT_SPELL_TMS_TRAIT)
    td1_run_spell_tms = trait_manager.get(TD1TMSModuleHandler.TD1_RUN_SPELL_TMS_TRAIT)
    td1_wellness_tms = trait_manager.get(TD1TMSModuleHandler.WELLNESS_TMS_TRAIT)
    pet_teleport_tms = trait_manager.get(TD1TMSModuleHandler.PET_TELEPORT_TMS_TRAIT)

    if sim_info.has_trait(vampire_bat_tms) or sim_info.has_trait(vampire_mist_tms) or sim_info.has_trait(vampire_run_tms) or sim_info.has_trait(witch_teleport_spell_tms) or sim_info.has_trait(witch_brooms_tms) or sim_info.has_trait(td1_darkapparate_tms) or sim_info.has_trait(td1_mist_spell_tms) or sim_info.has_trait(td1_bat_spell_tms) or sim_info.has_trait(td1_wellness_tms):
        pass
    else:
        if sim_info is not None and sim_info.species == Species.HUMAN:
            if TD1TMSModuleHandler.VAMPIRE_BAT_TMS_AUTOADD is True and get_option_value('vampire_bat_tms_autoadd') is True:
                if sim_info.has_trait(vampire_bat_tp_trait):
                    sim_info.add_trait(vampire_bat_tms)

            elif TD1TMSModuleHandler.VAMPIRE_MIST_TMS_AUTOADD is True and get_option_value('vampire_mist_tms_autoadd') is True:
                if sim_info.has_trait(vampire_mist_tp_trait):
                    sim_info.add_trait(vampire_mist_tms)

            elif TD1TMSModuleHandler.VAMPIRE_RUN_TMS_AUTOADD is True and get_option_value('vampire_run_tms_autoadd') is True:
                if sim_info.has_trait(vampire_run_tp_trait):
                    sim_info.add_trait(vampire_run_tms)

            elif TD1TMSModuleHandler.WITCH_SPELL_TMS_AUTOADD is True and get_option_value('witch_spell_tms_autoadd') is True:
                if sim_info.has_trait(witch_teleport_spell_tp_trait):
                    sim_info.add_trait(witch_teleport_spell_tms)

            elif TD1TMSModuleHandler.WITCH_BROOMS_TMS_AUTOADD is True and get_option_value('witch_broom_tms_autoadd') is True:
                if sim_info.has_trait(witch_brooms_tp_trait):
                    sim_info.add_trait(witch_brooms_tms)

            elif TD1TMSModuleHandler.WEREWOLF_SUPER_SPEED_TMS_AUTOADD is True and get_option_value('werewolf_run_tms_autoadd') is True:
                if sim_info.has_trait(werewolf_run_tp_trait):
                    sim_info.add_trait(werewolf_run_tms)

            elif TD1TMSModuleHandler.GHOST_TELEPORT_TMS_AUTOADD is True and get_option_value('ghost_teleport_tms_autoadd') is True:
                if sim_info.has_trait(ghost_teleport_tp_trait):
                    sim_info.add_trait(ghost_teleport_tms)

            elif TD1TMSModuleHandler.SPACEBEND_TELEPORT_TMS_AUTOADD is True and get_option_value('spacebend_teleport_tms_autoadd') is True:
                if sim_info.has_trait(spacebend_teleport_tp_trait):
                    sim_info.add_trait(spacebend_teleport_tms)

            elif TD1TMSModuleHandler.FAIRY_TELEPORT_TMS_AUTOADD is True and get_option_value('fairy_teleport_tms_autoadd') is True:
                if sim_info.has_trait(fairy_teleport_tp_trait):
                    sim_info.add_trait(fairy_teleport_tms)

            elif TD1TMSModuleHandler.FAIRY_WALKSTYLE_TMS_AUTOADD is True and get_option_value('fairy_walkstyle_tms_autoadd') is True:
                if sim_info.has_trait(fairy_walkstyle_tp_trait):
                    sim_info.add_trait(fairy_walkstyle_tms)

            elif TD1TMSModuleHandler.TD1_DARK_ARRARATE_SPELL_TMS_AUTOADD is True and get_option_value('td1_dark_apparate_tms_autoadd') is True:
                if sim_info.has_trait(td1_darkapparate_tp_trait):
                    sim_info.add_trait(td1_darkapparate_tms)

            elif TD1TMSModuleHandler.TD1_MIST_SPELL_TMS_AUTOADD is True and get_option_value('td1_mist_spell_tms_autoadd') is True:
                if sim_info.has_trait(td1_mist_spell_tp_trait):
                    sim_info.add_trait(td1_mist_spell_tms)

            elif TD1TMSModuleHandler.TD1_BAT_SPELL_TMS_AUTOADD is True and get_option_value('td1_bat_spell_tms_autoadd') is True:
                if sim_info.has_trait(td1_bat_spell_tp_trait):
                    sim_info.add_trait(td1_bat_spell_tms)

            elif TD1TMSModuleHandler.TD1_RUN_SPELL_TMS_AUTOADD is True and get_option_value('td1_run_spell_tms_autoadd') is True:
                if sim_info.has_trait(td1_run_spell_tp_trait):
                    sim_info.add_trait(td1_run_spell_tms)

            elif TD1TMSModuleHandler.WELLNESS_TMS_AUTOADD is True and get_option_value('wellness_tms_autoadd') is True:
                if sim_info.has_trait(td1_wellness_tp_trait):
                    sim_info.add_trait(td1_wellness_tms)

            elif TD1TMSModuleHandler.PET_TELEPORT_TMS_AUTOADD is True and get_option_value('pet_teleport_tms_autoadd') is True:
                if sim_info.has_trait(pet_tp_trait):
                    sim_info.add_trait(pet_teleport_tms)

            else:
                pass
