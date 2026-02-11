"""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
TwelfthDoctor1's Developer/Debug Access Panel

> ModuleHandler Tuning

(C) Copyright TD1 & TWoCC 2020 - 2021
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Licensed under CC-BY-NC-ND 4.0

https://creativecommons.org/licenses/by-nc-nd/4.0/

Codes from other parties are not part of the License and Copyright.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""
import services
import webbrowser
from collections import defaultdict
from DevAccessPanel.CoreLib.TD1_DevAccessPanel_Decorator import to_decorate
from DevAccessPanel.MainLib.TD1_DevAccessPanel_Config import get_option_value, print_config_values_notif
from distributor.shared_messages import IconInfoData
from server.client import SelectableSims
from server_commands.interaction_commands import show_interaction_tuning_name
from sims.sim_info_manager import SimInfoManager
from sims4.collections import make_immutable_slots_class
from sims4.commands import Command, CommandType, CheatOutput, execute, client_cheat, Output
from sims4.localization import LocalizationHelperTuning, _create_localized_string
from sims4.log import Logger
from sims4.resources import Types, get_resource_key
from sims4.tuning.tunable import TunableReference, Tunable, TunableEnumEntry
from ui.ui_dialog import UiDialogResponse, ButtonType, UiDialogOkCancel
from ui.ui_dialog_notification import UiDialogNotification
from DevAccessPanel.CoreLib.TD1_DevAccessPanel_Services import TD1CoreServiceHandler

# Importation of MasterApprentice Logger
try:
    from MasterApprenticeLib.TD1_Lib_ApprenticeLogger import ApprenticeLogger

    apprentice_logger = ApprenticeLogger('TD1 Developer/Debug Access Panel Module Handler', main_owner='TwelfthDoctor1')

except ImportError:
    apprentice_logger = False

try:
    from MasterApprenticeLib.TD1_Lib_MasterLogger import MasterLogger

    master_logger = MasterLogger('TD1 Developer/Debug Access Panel Module Handler', main_owner='TwelfthDoctor1')

except ImportError:
    master_logger = False

logger = Logger('TD1 Developer/Debug Access Panel Module Handler', default_owner='TwelfthDoctor1')

"""
Command List: To allow for calling of Console Only Cheats
Tuple Usage: (Enable Command: String, Disable Command: String, Is Client Type Command: Boolean)

Enable Command: The command along with its parameters used to enable the cheat, Compulsory
Disable Command: The command along with its parameters used to disable the cheat, Optional: Can be left as blank
Is Client Type Command: True Or False, specifies whether the command is Client Type or Command Type

Client Type: Commands not found within the Simulation Files. Cannot be used through XML.
Command Type: Commands found within the Simulation Files. Can be used through XML.
"""
command_lists = [
    (
        # Show Help
        'td1devaccess.help',
        'notif=False',
        '[IN USE]',
        'Calls the Help Notification. Lists all Commands inside this mod. Setting notif to True will show the notifications.',
        'main'
    ),
    (
        # Show Integration
        'td1devaccess.get_integration',
        'No Params',
        '[IN USE]',
        'Calls the Integration Status Notification. List Integrated Mod Install Status.',
        'main'
    ),
    (
        # Show Integration
        'td1devaccess.get_tuning_modifiers',
        'No Params',
        '[IN USE]',
        'Calls the Modifier Status Notification. List Tuning Modifier Status.',
        'main'
    ),
    (
        # Call Version
        'td1devaccess.show_version',
        'scenario=0 (Can be left Empty)',
        '[IN USE]',
        'Calls the Startup Notification used on load. For testing: Set 1 for Success, 2 for Failure',
        'main'
    ),
    (
        # Call Developer Version
        'td1devaccess.show_dev_version',
        'scenario=0 (Can be left Empty)',
        '[IN USE]',
        'Calls the Dev Startup Notification used on load. For testing: Set 1 for Success, 2 for Failure',
        'main'
    ),
    (
        # Call Beta Version
        'td1devaccess.show_beta_version',
        'scenario=0 (Can be left Empty)',
        '[IN USE]',
        'Calls the Beta Startup Notification used on load. For testing: Set 1 for Success, 2 for Failure',
        'main'
    ),
    (
        # Call Version (V2)
        'td1devaccess.show_version_v2',
        'scenario=0 (Can be left Empty), debug=False (Can be left empty)',
        '[IN USE]',
        'Calls the Startup Notification (V2) used on load. Testing options can be seen if Dev Version is toggled.',
        'main'
    ),
    (
        # Reset Startup Notifs
        'td1devaccess.reset_startup_notif',
        'No Params',
        '[IN USE]',
        'Resets the Startup Notifs to show them on next load.',
        'main'
    ),
    (
        # Get Config List
        'td1devaccess.list_config',
        'No Params',
        '[IN USE]',
        'Lists the Config and their Values from the config file for reference.',
        'main'
    ),
    (
        # Set Config Option
        'td1devaccess.set_option',
        'option',
        '[IN USE]',
        'Sets the specified config option onto its inversed value. If originally False, then it will be set as True, vice versa.',
        'main'
    ),
    (
        # Set Pets Selectability
        'td1devaccess.toggle_selectable_pets',
        'option',
        '[IN USE]',
        'Toggles whether Pets can be selectable from the UI. By default it is not selectable.',
        'main'
    ),
    (
        # Changelog UI
        'td1devaccess.changelog',
        'option',
        '[IN USE]',
        'Shows Changelog UI.',
        'main'
    ),
    (
        # Modify Funds
        'td1devaccess.modify_funds',
        'household_id=0 (Can be left Empty)',
        '[IN USE]',
        'Modifies the Household Funds by adding or subtracting to reach the specified value.',
        'funds'
    ),
    (
        # Set Funds
        'td1devaccess.set_funds',
        'household_id=0 (Can be left Empty)',
        '[IN USE]',
        'Modifies the Household Funds setting it to the specified value.',
        'funds'
    ),
    (
        # Modify Bucks
        'td1devaccess.modify_bucks',
        'buck_type (Required), actor_sim (Required)',
        '[IN USE]',
        'Modifies the specified BucksType by adding or subtracting to reach the specified value.',
        'bucks'
    ),
    (
        # Set Bucks
        'td1devaccess.set_bucks',
        'buck_type (Required), actor_sim (Required)',
        '[IN USE]',
        'Modifies the BucksType by setting it to the specified value.',
        'bucks'
    ),
    (
        # Modify Street Eco Footprint
        'td1devaccess.modify_street_eco_footprint',
        'No Params',
        '[IN USE]',
        'Modifies the Street Eco Footprint to the specified value.',
        'ecofootprint'
    ),
    (
        # Modify Lot Eco Footprint
        'td1devaccess.modify_lot_eco_footprint',
        'No Params',
        '[IN USE]',
        'Modifies the Lot Eco Footprint to the specified value. \nThis command WILL NOT produce results, use street version instead.',
        'ecofootprint'
    ),
    (
        # Get Club ID
        'td1devaccess.get_club_id OR clubs.get_club_id',
        'club_name (Required)',
        '[IN USE]',
        "Gets the Club Id from the specified Club Name for use in Club Commands. \nNote that Scumbumbo's Club Utils Mod uses a different method getting the Club ID and is therefore incompatible.",
        'club'
    ),
    (
        # Modify Club Points
        'td1devaccess.modify_club_points',
        'actor_sim (Required)',
        '[IN USE]',
        'Modifies the Club Bucks by adding or subtracting to the specified value.',
        'club'
    ),
    (
        # Set Club Points
        'td1devaccess.set_club_points',
        'actor_sim (Required)',
        '[IN USE]',
        'Modifies the Club Bucks by setting it to the specified value.',
        'club'
    ),
    (
        # Enact Civic Policy
        'td1devaccess.enact_civic_policy OR civic_policy.current_street.enact',
        'policy, opt_target',
        '[IN USE]',
        'Instantly enact a Civic Policy on current street.',
        'civicpolicy'
    ),
    (
        # Repeal Civic Policy
        'td1devaccess.repeal_civic_policy OR civic_policy.current_street.repeal',
        'policy, opt_target',
        '[IN USE]',
        'Instantly repeal a Civic Policy on current street.',
        'civicpolicy'
    ),
    (
        # Vote Civic Policy
        'td1devaccess.vote_civic_policy OR civic_policy.current_street.vote',
        'policy, opt_target, count, user_directed, lobby_interaction',
        '[IN USE]',
        'Vote on a Civic Policy on current street.',
        'civicpolicy'
    ),
    (
        # Begin Civic Policy Repeal
        'td1devaccess.begin_repeal_policy OR civic_policy.current_street.begin_repeal',
        'policy, opt_target',
        '[IN USE]',
        'Begin a Civic Policy Repeal on current street.',
        'civicpolicy'
    ),
    (
        # End Civic Policy Repeal
        'td1devaccess.end_repeal_policy OR civic_policy.current_street.end_repeal',
        'policy, opt_target',
        '[IN USE]',
        'End a Civic Policy Repeal on current street.',
        'civicpolicy'
    ),
    (
        # End Civic Policy Repeal
        'td1devaccess.end_voting OR civic_policy.current_street.force_end_voting',
        'all_streets, opt_target',
        '[IN USE]',
        'Force End Voting on all streets.',
        'civicpolicy'
    ),
    (
        # Pack Entitlements
        'td1devaccess.list_packs OR mtx.list_packs',
        'No Params',
        '[IN USE]',
        'Gets a list of all EPs, GPs, SPs and Misc Packs and prints out into notification. \nNote that Placeholder Packs will be present. \nConsult Origin/EA Desktop/Sims Website for a list of Released Packs.',
        'mtx'
    ),
    (
        # Enable Free Build For XML
        'td1devaccess.enablefreebuild',
        'No Params',
        '[IN USE]',
        'Executes the bb.enablefreebuild cheat. For use in XML.',
        'clientcommands'
    ),
    (
        # Call Client Command/Command From List
        'td1devaccess.call_client_command OR td1devaccess.call OR call_command',
        'identifier, state',
        '[IN USE]',
        'Executes cheats not usable in XML. For use in XML. Also usable for fast typing.',
        'clientcommands'
    ),
    (
        # Get Client Command/Command List
        'td1devaccess.show_client_command_list',
        'No Params',
        '[IN USE]',
        'Prints list of the Client Command/Command List.',
        'clientcommands'
    ),
    (
        # Get Client Command/Command List
        'td1devaccess.convert_cfg_to_json',
        'No Params',
        '[IN USE]',
        'Converts the .cfg file into a .json file.',
        'main'
    ),
]

client_commands_list = [
    (
        # Testing Cheats
        'testingcheats true', 'testingcheats false', False
    ),
    (
        # Free Build Mode: For Generally Uneditable Lots
        'bb.enablefreebuild', '', True
    ),
    (
        # Move Objects
        'bb.moveobjects on', 'bb.moveobjects off', True
    ),
    (
        # Show Debug Objects
        'bb.showhiddenobjects', '', True
    ),
    (
        # Show Live Edit Objects
        'bb.showliveeditobjects', '', True
    ),
    (
        # Unlock Gameplay Objects
        'bb.ignoregameplayunlocksentitlement', '', True
    ),
    (
        # Toggle Headline Effects
        'headlineeffects off', 'headlineeffects on', True
    ),
    (
        # Show Work In Progress Objects: ???
        'bb.showwipobjects', '', True
    ),
    (
        # Shorten Crafting Phases
        'crafting.shorten_phases on', 'crafting.shorten_phases off', False
    ),
    (
        # Toggle NavMesh: ???
        'routing.toggle_navmesh on', 'routing.toggle_navmesh off', True
    ),
    (
        # Routing Toggle Visualisation: ??? (Vector Lines?)
        'routing.toggle_visualization on', 'routing.toggle_visualization off', True
    ),
    (
        # Ambient Autonomy
        'autonomy.ambient off', 'autonomy.ambient on', False
    ),
    (
        # Household Autonomy Autonomy
        'autonomy.household off', 'autonomy.household on', False
    ),
    (
        # Fill Sims Commodities Within Household
        'stats.fill_commodities_household', '', False
    ),
    (
        # Enable/Disable All Sims Commodities (Needs)
        'stats.disable_all_commodities', 'stats.enable_all_commodities', False
    ),
    (
        # Reset All Sims
        'sims.reset_all', '', False
    ),
    (
        # Toggle Death
        'death.toggle False', 'death.toggle True', False
    ),
    (
        # Toggle Fire
        'fire.toggle_enabled off', 'fire.toggle_enabled on', False
    ),
    (
        # Toggle Automation Events
        'qa.automation.enable_events True', 'qa.automation.enable_events False', False
    ),
    (
        # Toggle Civic Policy Voting [EP09]
        'civic_policy.set_npc_voting_enabled True', 'civic_policy.set_npc_voting_enabled False', False
    ),
    (
        # Toggle Dust Service [SP22]
        'dust.set_dust_enabled True', 'dust.set_dust_enabled False', False
    ),
    (
        # Toggle Eco Footprint Service [EP09]
        'eco_footprint.set_eco_footprint_enabled True', 'eco_footprint.set_eco_footprint_enabled False', False
    ),
    (
        # Toggle If Sims Should Opt Out Of Fame [EP06]
        'fame.set_start_all_sims_opted_out_of_fame False', 'fame.set_start_all_sims_opted_out_of_fame True', False
    ),
    (
        # Toggle Force Fame Moments [EP06]
        'fame.force_fame_moments True', 'fame.force_fame_moments False', False
    ),
    (
        # Toggle Debug Force Fame Moments [EP06]
        'fame.debug_force_fame_moments True', 'fame.debug_force_fame_moments False', False
    ),
    (
        # Toggle Force Fame Moments [EP06]
        'fame.force_fame_moments True', 'fame.force_fame_moments False', False
    ),
    (
        # Toggle Debug Visuals For Waypoints
        'debugvis.waypoints.start', 'debugvis.waypoints.stop', False
    ),
    (
        # Toggle Debug Visuals For Socials
        'debugvis.social.start', 'debugvis.waypoints.stop', False
    ),
    (
        # Toggle Debug Visuals For SimPos
        'debugvis.sim_position.start', 'debugvis.sim_position.stop', False
    ),
    (
        # Toggle Debug Visuals For Selected Constraints
        'debugvis.constraints.selected.toggle', '', False
    ),
    (
        # Toggle Debug Visuals For Selected Socials
        'debugvis.socials.selected.toggle', '', False
    ),
    (
        # Toggle Debug Visuals For LOS
        'debugvis.sim_los.start', 'debugvis.sim_los.stop', False
    ),
    (
        # Toggle Debug Visuals For Spawn Points
        'debugvis.spawn_points.start', 'debugvis.spawn_points.stop', False
    ),
    (
        # Toggle Debug Visuals For Spawner Components
        'debugvis.spawner_component.start', 'debugvis.spawner_component.stop', False
    ),
    (
        # Toggle Debug Visuals For Locators
        'debugvis.locators.start', 'debugvis.locators.stop', False
    ),
    (
        # Toggle Debug Visuals For Portals
        'debugvis.portals.start', 'debugvis.portals.stop', False
    ),
    (
        # Toggle Debug Visuals For Sim Quadtree
        'debugvis.sim_quadtree.start', 'debugvis.sim_quadtree.stop', False
    ),
    (
        # Toggle Debug Visuals For Fire Quadtree
        'debugvis.fire_quadtree.start', 'debugvis.fire_quadtree.stop', False
    ),
    (
        # Toggle Debug Visuals For Broadcasters
        'debugvis.broadcasters.start', 'debugvis.broadcasters.stop', False
    ),
    (
        # Toggle Debug Visuals For Routing Formations
        'debugvis.routing_formations.start', 'debugvis.routing_formations.stop', False
    ),
    (
        # Toggle Environment Scores Used to Boost Moods
        'environment_score.enable', 'environment_score.disable', False
    ),
]


class TD1DevAccessPanelMainService(TD1CoreServiceHandler):
    def __init__(self):
        super().__init__(
            name="DevAccessPanel Main Service",
            desc="The DevAccessPanel Main Service is used to track main functions in the DevAccessPanel.",
            owner="TwelfthDoctor1"
        )


MAIN_SERVICE = TD1DevAccessPanelMainService()


class TD1AccessPanelModuleHandler:
    ACCESSPANEL_STARTUP_NOTIFICATION = UiDialogNotification.TunableFactory(
        description='The notification to be used on game load, used on release versions.'
    )
    ACCESSPANEL_DEVELOPER_STARTUP_NOTIFICATION = UiDialogNotification.TunableFactory(
        description='The developer notification to be used on game load, developer use only.'
    )
    ACCESSPANEL_BETA_STARTUP_NOTIFICATION = UiDialogNotification.TunableFactory(
        description='The beta notification to be used on game load, mainly for beta testers.'
    )
    ACCESSPANEL_ALLOW_STARTUP_NOTIFICATION = Tunable(
        description='Whether the startup notification should show up on load.',
        tunable_type=bool,
        default=True
    )
    ACCESSPANEL_ALLOW_DEVELOPER_STARTUP_NOTIFICATION = Tunable(
        description='Whether the developer startup notification should show up on load.',
        tunable_type=bool,
        default=False
    )
    ACCESSPANEL_ALLOW_BETA_STARTUP_NOTIFICATION = Tunable(
        description='Whether the beta startup notification should show up on load.',
        tunable_type=bool,
        default=False
    )
    ACCESSPANEL_ALLOW_INTEGRATION_NOTIFICATION = Tunable(
        description='Whether the mod integration notification should show up on load.',
        tunable_type=bool,
        default=False
    )
    ACCESSPANEL_ALLOW_MODIFIER_NOTIFICATION = Tunable(
        description='Whether the modifier notification should show up on load.',
        tunable_type=bool,
        default=False
    )
    ACCESSPANEL_ALLOW_CONFIG_NOTIFICATION = Tunable(
        description='Whether the Config Notification should show up on load.',
        tunable_type=bool,
        default=False
    )
    ACCESSPANEL_OVERRIDE_PACK_TESTSET = Tunable(
        description='Controls the overridding of Pack TestSets. If enabled, any pack testset that is supposedly to be set as False will be inverted to True. This can allow access to certain sections even though the player does not own the specified pack.',
        tunable_type=bool,
        default=False
    )
    ACCESSPANEL_OVERRIDE_INTEGRATION_TESTSET = Tunable(
        description='Controls the overridding of Integration TestSets. If enabled, any Integration testset that is supposedly to be set as False will be inverted to True. This can allow access to certain sections even though the player does not own the specified Integration.',
        tunable_type=bool,
        default=False
    )
    ACCESSPANEL_OVERRIDE_VERSION_TESTSET = Tunable(
        description='Controls the overridding of Version TestSets. If enabled, any VErsion testset that is supposedly to be set as False will be inverted to True. This can allow access to certain sections even though the player does not own the specified Version.',
        tunable_type=bool,
        default=False
    )
    ACCESSPANEL_MOD_VERSION = Tunable(
        description='Current mod version. Used for Mod Verification and Testing.',
        tunable_type=str,
        default=''
    )
    ACCESSPANEL_IGNORE_MOD_VERSION = Tunable(
        description='Controls the Version Mismatch Test. If ignored, Version Mismatch Test will not flag up errors should versions be different.',
        tunable_type=bool,
        default=False
    )
    ACCESSPANEL_STARTUP_NOTIFICATION_V2_USAGE = Tunable(
        description='Controls usage of which version of the Startup Notification should be used. If disabled, Version 1 will be used. If enabled, Version 2 will be used.',
        tunable_type=bool,
        default=True
    )
    ACCESSPANEL_OVERRIDE_DEBUG_INTERACTIONS = Tunable(
        description='Controls whether Debug Interactions should appear in release versions.',
        tunable_type=bool,
        default=True
    )
    ACCESSPANEL_FORCE_DEBUG_INTERACTIONS_INTO_CHEAT_PIE_MENU = Tunable(
        description='Controls whether Debug-Converted Interactions should be inside the Cheat Pie Menu. If Debug Interactions are not overridden, then this option will be ignored.',
        tunable_type=bool,
        default=True
    )
    ACCESSPANEL_CHANGELOG = Tunable(
        description='Changelog Text for Changelog UI.',
        tunable_type=str,
        default=''
    )
    notification_ran = False
    mod_version = 'Developer Version 31 Build'


# Command Handling Section
# Note: Secnario Var - If 1, then Notif will show up, for all other numbers not 1 excluding 0, Notif will not show with Indication that Tuning is set to Disabled.

@Command('td1devaccess.show_version', command_type=CommandType.Live)
def show_version(scenario: int = 0, _connection=None):
    output = CheatOutput(_connection)
    if scenario is 0:
        if TD1AccessPanelModuleHandler.ACCESSPANEL_ALLOW_STARTUP_NOTIFICATION is True:
            startup_notification = TD1AccessPanelModuleHandler.ACCESSPANEL_STARTUP_NOTIFICATION(None)
            startup_notification.show_dialog()
        else:
            output('Startup Notification Disabled, it can be enabled via the TD1_DevAccessPanel_ModuleHandler Tuning')
    elif scenario is 1:
        startup_notification = TD1AccessPanelModuleHandler.ACCESSPANEL_STARTUP_NOTIFICATION(None)
        startup_notification.show_dialog()
    else:
        output('Startup Notification Disabled, it can be enabled via the TD1_DevAccessPanel_ModuleHandler Tuning')


@Command('td1devaccess.show_dev_version', command_type=CommandType.Live)
def show_dev_version(scenario: int = 0, _connection=None):
    output = CheatOutput(_connection)
    if scenario is 0:
        if TD1AccessPanelModuleHandler.ACCESSPANEL_ALLOW_DEVELOPER_STARTUP_NOTIFICATION is True:
            startup_notification = TD1AccessPanelModuleHandler.ACCESSPANEL_DEVELOPER_STARTUP_NOTIFICATION(None)
            startup_notification.show_dialog()
        else:
            output(
                'Developer Startup Notification Disabled, it can be enabled via the TD1_DevAccessPanel_ModuleHandler Tuning. However, this should only be done by TwelfthDoctor1.')
    elif scenario is 1:
        developer_startup_notification = TD1AccessPanelModuleHandler.ACCESSPANEL_DEVELOPER_STARTUP_NOTIFICATION(None)
        developer_startup_notification.show_dialog()
    else:
        output(
            'Developer Startup Notification Disabled, it can be enabled via the TD1_DevAccessPanel_ModuleHandler Tuning. However, this should only be done by TwelfthDoctor1.')


@Command('td1devaccess.show_beta_version', command_type=CommandType.Live)
def show_dev_version(scenario: int = 0, _connection=None):
    output = CheatOutput(_connection)
    if scenario is 0:
        if TD1AccessPanelModuleHandler.ACCESSPANEL_ALLOW_BETA_STARTUP_NOTIFICATION is True:
            startup_notification = TD1AccessPanelModuleHandler.ACCESSPANEL_BETA_STARTUP_NOTIFICATION(None)
            startup_notification.show_dialog()
        else:
            output(
                'Beta Startup Notification Disabled, it can be enabled via the TD1_DevAccessPanel_ModuleHandler Tuning. However, this should only be done by TwelfthDoctor1.')
    elif scenario is 1:
        beta_startup_notification = TD1AccessPanelModuleHandler.ACCESSPANEL_BETA_STARTUP_NOTIFICATION(None)
        beta_startup_notification.show_dialog()
    else:
        output(
            'Beta Startup Notification Disabled, it can be enabled via the TD1_DevAccessPanel_ModuleHandler Tuning. However, this should only be done by TwelfthDoctor1.')


# Discord Server Invite Command to report-bugs

@Command('td1devaccess.td1_discord', command_type=CommandType.Live)
def td1_discord(_connection=None):
    output = CheatOutput(_connection)
    client = services.client_manager().get_first_client()
    output('Please check your browser for the server invite (Only if you accepted the dialog!).')

    def on_response(discord_dialog):
        if discord_dialog.accepted:
            webbrowser.open(
                'https://discord.gg/waHpcSHZwb')  # This link opens up Discord to invite the user to TD1 Community Server (3.0) for bug reporting

    discord_title = lambda **_: LocalizationHelperTuning.get_raw_text("TD1 Community Server (TD1 CS)")
    discord_text = lambda **_: LocalizationHelperTuning.get_raw_text(
        "If you require mod support or have any questions, you can direct your questions onto the Discord Server.\n\nNote: This will open up a web browser outside The Sims 4."
    )

    discord_dialog = UiDialogOkCancel.TunableFactory().default(
        client.active_sim,
        title=discord_title,
        text=discord_text
    )
    discord_dialog.add_listener(on_response)
    discord_dialog.show_dialog()


@Command('td1devaccess.td1_patreon', command_type=CommandType.Live)
def td1_patreon(_connection=None):
    output = CheatOutput(_connection)
    client = services.client_manager().get_first_client()
    output('Please check your browser for the link (Only if you accepted the dialog!).')

    def on_response(patreon_dialog):
        if patreon_dialog.accepted:
            webbrowser.open('https://www.patreon.com/twelfthdoctor1')  # This link opens up the Patreon Page

    patreon_title = lambda **_: LocalizationHelperTuning.get_raw_text("TD1 Patreon Page")
    patreon_text = lambda **_: LocalizationHelperTuning.get_raw_text(
        "Most Mods will be kept here for free. If you wish to support, you are free to donate.\n\nNote: This will open up a web browser outside The Sims 4."
    )

    patreon_dialog = UiDialogOkCancel.TunableFactory().default(
        client.active_sim,
        title=patreon_title,
        text=patreon_text
    )
    patreon_dialog.add_listener(on_response)
    patreon_dialog.show_dialog()


@Command('td1devaccess.td1_dev_update', command_type=CommandType.Live)
def td1_dev_update(_connection=None):
    output = CheatOutput(_connection)
    client = services.client_manager().get_first_client()
    output('Please check your browser for the link (Only if you accepted the dialog!).')

    def on_response(update_dialog):
        if update_dialog.accepted:
            webbrowser.open(
                'https://td1sims.tumblr.com/tagged/Development')  # This link opens up the Tumblr Mod Dev Update Page

    update_title = lambda **_: LocalizationHelperTuning.get_raw_text("Development Blog Page")
    update_text = lambda **_: LocalizationHelperTuning.get_raw_text(
        "Development to the Access Panel will be tagged under this section. Updates will be listed here.\n\nNote: This will open up a web browser outside The Sims 4."
    )

    update_dialog = UiDialogOkCancel.TunableFactory().default(
        client.active_sim,
        title=update_title,
        text=update_text
    )
    update_dialog.add_listener(on_response)
    update_dialog.show_dialog()


@Command('td1devaccess.license', command_type=CommandType.Live)
def td1_dev_update(_connection=None):
    output = CheatOutput(_connection)
    client = services.client_manager().get_first_client()
    output('Showing License.')

    def on_response(license_dialog):
        if license_dialog.accepted:
            webbrowser.open(
                'https://creativecommons.org/licenses/by-nc-nd/4.0/')  # This link opens up the Creative Commons License Page

    license_title = lambda **_: LocalizationHelperTuning.get_raw_text("CC-BY-ND-ND 4.0 License")
    license_text = lambda **_: LocalizationHelperTuning.get_raw_text(
        "This Mod is licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International License under TD1 & TWoCC 2020-2021. Codes by EA/Maxis are not part of this license. For more information, please visit the Creative Commons Website.\n\nNote: This will open up a web browser outside The Sims 4."
    )

    license_dialog = UiDialogOkCancel.TunableFactory().default(
        client.active_sim,
        title=license_title,
        text=license_text
    )
    license_dialog.add_listener(on_response)
    license_dialog.show_dialog()


@Command('td1devaccess.changelog', command_type=CommandType.Live)
def list_changelog(_connection):
    output = CheatOutput(_connection)
    client = services.client_manager().get_first_client()
    output('Showing Changelog.')

    def on_response(license_dialog):
        if license_dialog.accepted:
            return

    changelog_title = lambda **_: _create_localized_string(
        0x4F1A608A)  # LocalizationHelperTuning.get_raw_text("TD1 Developer/Debug Access Panel Changelog")
    changelog_text = lambda **_: _create_localized_string(0x4F1A608B,
                                                          str(TD1AccessPanelModuleHandler.ACCESSPANEL_MOD_VERSION),
                                                          str(TD1AccessPanelModuleHandler.mod_version),
                                                          str(TD1AccessPanelModuleHandler.ACCESSPANEL_CHANGELOG))

    license_dialog = UiDialogOkCancel.TunableFactory().default(
        client.active_sim,
        title=changelog_title,
        text=changelog_text
    )
    license_dialog.add_listener(on_response)
    license_dialog.show_dialog()


@to_decorate(SimInfoManager, 'on_loading_screen_animation_finished')
def td1_accesspanel_add_on_load_complete(original, self, *args, **kwargs):
    result = original(self, *args, **kwargs)

    if TD1AccessPanelModuleHandler.notification_ran is True:
        return

    try:
        # Services to run for DevAccessPanel
        MAIN_SERVICE.start_service()

        accesspanel_version_control()
        accesspanel_startup_notification_handler()

        TD1AccessPanelModuleHandler.notification_ran = True

        MAIN_SERVICE.inform_service("Startup Complete. No issues found.")

        # execute("td1devaccess.convert_cfg_to_json", None)

    except Exception as e:

        if apprentice_logger is not False and apprentice_logger is not None:
            apprentice_logger.error(f"Error found with Developer Access Panel Startup Notification Module: {str(e)}",
                                    owner="TwelfthDoctor1")

        MAIN_SERVICE.error_service(f"ERROR WITH NOTIFICATION MODULE: {str(e)}")

        raise Exception(
            f"Error found with Developer Access Panel Startup Notification Module by TwelfthDoctor1: {str(e)}")

    return result


def accesspanel_startup_notification_handler():
    if apprentice_logger is not None and apprentice_logger is not False:
        apprentice_logger.info(
            "TD1 Developer Access Panel Version Control\n\nPackage Version: {}\nScript Version: {}".format(
                TD1AccessPanelModuleHandler.ACCESSPANEL_MOD_VERSION, TD1AccessPanelModuleHandler.mod_version
            ))

    if master_logger is not None and master_logger is not False:
        master_logger.info(
            "TD1 Developer Access Panel Version Control\n\nPackage Version: {}\nScript Version: {}".format(
                TD1AccessPanelModuleHandler.ACCESSPANEL_MOD_VERSION, TD1AccessPanelModuleHandler.mod_version
            ))

    if get_option_value('disable_notifs') is True:
        return

    # urllib in EA lib cannot handle https
    # execute('td1devaccess.version_check', None)

    if TD1AccessPanelModuleHandler.ACCESSPANEL_STARTUP_NOTIFICATION_V2_USAGE is True:
        execute('td1devaccess.show_version_v2', None)
    else:
        if TD1AccessPanelModuleHandler.ACCESSPANEL_ALLOW_STARTUP_NOTIFICATION is True:
            execute('td1devaccess.show_version 1', None)
        else:
            execute('td1devaccess.show_version 2', None)

        if TD1AccessPanelModuleHandler.ACCESSPANEL_ALLOW_DEVELOPER_STARTUP_NOTIFICATION is True:
            execute('td1devaccess.show_dev_version 1', None)
        else:
            execute('td1devaccess.show_dev_version 2', None)

        if TD1AccessPanelModuleHandler.ACCESSPANEL_ALLOW_BETA_STARTUP_NOTIFICATION is True:
            execute('td1devaccess.show_beta_version 1', None)
        else:
            execute('td1devaccess.show_beta_version 2', None)

    if TD1AccessPanelModuleHandler.ACCESSPANEL_ALLOW_INTEGRATION_NOTIFICATION is True:
        execute('td1devaccess.get_integration', None)

    if TD1AccessPanelModuleHandler.ACCESSPANEL_ALLOW_MODIFIER_NOTIFICATION is True:
        execute('td1devaccess.get_tuning_modifiers', None)

    if TD1AccessPanelModuleHandler.ACCESSPANEL_ALLOW_CONFIG_NOTIFICATION is True:
        execute('td1devaccess.list_config_notif', None)

    # Show Tuning Names on load
    if get_option_value("dev_show_int_tuning_name") is True:
        # execute('interactions.show_interaction_tuning_name True', None)
        show_interaction_tuning_name(True)


def accesspanel_version_control():
    client = services.client_manager().get_first_client()

    if str(TD1AccessPanelModuleHandler.ACCESSPANEL_MOD_VERSION).find(
            TD1AccessPanelModuleHandler.mod_version) != -1 or TD1AccessPanelModuleHandler.ACCESSPANEL_IGNORE_MOD_VERSION is True:
        return
    else:
        message_title_test_fail = lambda **_: LocalizationHelperTuning.get_raw_text(
            "TD1 Access Panel: Version Mismatch")
        message_text_test_fail = lambda **_: LocalizationHelperTuning.get_raw_text(
            "Version Mismatch found. Please check if your mod package and script are updated correctly.\n\nPackage Version: " + str(
                TD1AccessPanelModuleHandler.ACCESSPANEL_MOD_VERSION) + "\n\nScript Version: " + str(
                TD1AccessPanelModuleHandler.mod_version))

        notification_test_fail = UiDialogNotification.TunableFactory().default(
            client.active_sim,
            text=message_text_test_fail,
            title=message_title_test_fail,
            expand_behavior=UiDialogNotification.UiDialogNotificationExpandBehavior.FORCE_EXPAND,
            urgency=UiDialogNotification.UiDialogNotificationUrgency.URGENT
        )
        notification_test_fail.show_dialog()

        if apprentice_logger is not False and apprentice_logger is not None:
            apprentice_logger.warn("TD1 Access Panel Version Mismatch Error: Please check if your version is correct.",
                                   owner="TwelfthDoctor1")

        MAIN_SERVICE.warn_service(
            f"DevAccessPanel Version Mismatch Error: Please rectify Script Version [{TD1AccessPanelModuleHandler.mod_version}] and Package Version [{TD1AccessPanelModuleHandler.ACCESSPANEL_MOD_VERSION}] or Override Version Check via Module Tuning."
        )


def override_debug_interactions(self):
    debug_override_counter = 0
    cheat_override_counter = 0
    affordance_manager = services.affordance_manager()
    if TD1AccessPanelModuleHandler.ACCESSPANEL_OVERRIDE_DEBUG_INTERACTIONS is True and get_option_value(
            'override_debug_menu') is True:
        for tuning in self._tuned_classes.values():
            if tuning.debug is True:
                if TD1AccessPanelModuleHandler.ACCESSPANEL_FORCE_DEBUG_INTERACTIONS_INTO_CHEAT_PIE_MENU is True and get_option_value(
                        'force_debug_cheat_menu') is True:
                    if tuning.cheat is False:
                        tuning.cheat = True
                        cheat_override_counter += 1
                tuning.debug = False
                logger.info("[TD1 DevAccessPanel {}] Interaction Tuning Override for Debug Tunable: {}".format(
                    TD1AccessPanelModuleHandler.mod_version, tuning), owner="TwelfthDoctor1")

                if apprentice_logger is not False and apprentice_logger is not None:
                    apprentice_logger.info(
                        "[TD1 DevAccessPanel {}] Interaction Tuning Override for Debug Tunable: {}".format(
                            TD1AccessPanelModuleHandler.mod_version, tuning),
                        owner="TwelfthDoctor1")

                if master_logger is not False and master_logger is not None:
                    master_logger.info(
                        "[TD1 DevAccessPanel {}] Interaction Tuning Override for Debug Tunable: {}".format(
                            TD1AccessPanelModuleHandler.mod_version, tuning),
                        owner="TwelfthDoctor1")

                debug_override_counter += 1
        logger.info("[TD1 DevAccessPanel {}] Debug Override Count: {} | Cheat Override Count: {}".format(
            TD1AccessPanelModuleHandler.mod_version, debug_override_counter, cheat_override_counter),
                    owner="TwelfthDoctor1")

        if apprentice_logger is not False and apprentice_logger is not None:
            apprentice_logger.info("[TD1 DevAccessPanel {}] Debug Override Count: {} | Cheat Override Count: {}".format(
                TD1AccessPanelModuleHandler.mod_version, debug_override_counter, cheat_override_counter),
                                   owner="TwelfthDoctor1")

        if master_logger is not False and master_logger is not None:
            master_logger.info("[TD1 DevAccessPanel {}] Debug Override Count: {} | Cheat Override Count: {}".format(
                TD1AccessPanelModuleHandler.mod_version, debug_override_counter, cheat_override_counter),
                               owner="TwelfthDoctor1")


def make_pets_selectable(self, client):
    self._selectable_sim_infos = []
    self.client = client
    self._watchers = defaultdict(list)
    self._can_select_pets = False

    if get_option_value('allow_selectable_pets') is False:
        self._can_select_pets = False

        pet_message2 = 'Pets Selectability Disabled. User is not able to control Pet Sims.'

        logger.info(pet_message2, owner='TwelfthDoctor1')

        if apprentice_logger is not None and apprentice_logger is not False:
            apprentice_logger.info(pet_message2, owner='TwelfthDoctor1')

        if master_logger is not None and master_logger is not False:
            master_logger.info(pet_message2, owner='TwelfthDoctor1')
    else:
        self._can_select_pets = True

        pet_message1 = 'Pets Selectability Enabled. User is now able to control Pet Sims.'

        logger.info(pet_message1, owner='TwelfthDoctor1')

        if apprentice_logger is not None and apprentice_logger is not False:
            apprentice_logger.info(pet_message1, owner='TwelfthDoctor1')

        if master_logger is not None and master_logger is not False:
            master_logger.info(pet_message1, owner='TwelfthDoctor1')


# Base Code Starters
# services.client_manager().add_on_load_complete(td1_accesspanel_add_on_load_complete)
services.affordance_manager().add_on_load_complete(override_debug_interactions)
if get_option_value('allow_selectable_pets') is True:
    SelectableSims.__init__ = make_pets_selectable


@Command('td1devaccess.toggle_selectable_pets', command_type=CommandType.Live)
def toggle_selectable_pets(_connection=None):
    output = Output(_connection)
    selectable_sims = services.client_manager().get_first_client().selectable_sims
    selectable_sims.can_select_pets = not selectable_sims.can_select_pets
    if selectable_sims.can_select_pets:
        output('Pets are now selectable!!!')
    else:
        output('Pets are no longer selectable.')


@Command('td1devaccess.show_version_v2', command_type=CommandType.Live)
def mod_version_startup_notif_v2(scenario: int = 0, debug: bool = False, _connection=None):
    client = services.client_manager().get_first_client()
    output = CheatOutput(_connection)
    button1_text = None
    button2_text = None
    button3_text = None
    button4_text = None
    notif_title = None
    notif_text = None
    info_level = None
    visual = None

    if TD1AccessPanelModuleHandler.ACCESSPANEL_STARTUP_NOTIFICATION_V2_USAGE is False and scenario == 0:
        output(
            "Version 2 Startup Notification Disabled, it can be changed via the TD1_DevAccessPanel_ModuleHandler Tuning. Note that it should only be done by TwelfthDoctor1.")
        if TD1AccessPanelModuleHandler.ACCESSPANEL_ALLOW_DEVELOPER_STARTUP_NOTIFICATION is True:
            output("\nFor Notification Testing, the Variable: Scenario can be modified to use values 1 to 3.")

    if (TD1AccessPanelModuleHandler.ACCESSPANEL_ALLOW_STARTUP_NOTIFICATION is True and debug is False) or scenario == 1:
        notif_title = lambda **_: _create_localized_string(0x29249E2D)
        notif_text = lambda **_: _create_localized_string(0xD45017CE,
                                                          str(TD1AccessPanelModuleHandler.ACCESSPANEL_MOD_VERSION),
                                                          str(TD1AccessPanelModuleHandler.mod_version))
        info_level = UiDialogNotification.UiDialogNotificationLevel.PLAYER
        visual = UiDialogNotification.UiDialogNotificationVisualType.INFORMATION
        button1_text = lambda **_: _create_localized_string(0xD45017C7)
        button2_text = lambda **_: _create_localized_string(0xD45017C9)
        button3_text = lambda **_: _create_localized_string(0xD45017CC)
        button4_text = lambda **_: _create_localized_string(0xD45017CE)

    elif (
            TD1AccessPanelModuleHandler.ACCESSPANEL_ALLOW_DEVELOPER_STARTUP_NOTIFICATION is True and debug is False) or scenario == 2:
        notif_title = lambda **_: _create_localized_string(0x29249E2E)
        notif_text = lambda **_: _create_localized_string(0xD45017CF,
                                                          str(TD1AccessPanelModuleHandler.ACCESSPANEL_MOD_VERSION),
                                                          str(TD1AccessPanelModuleHandler.mod_version))
        info_level = UiDialogNotification.UiDialogNotificationLevel.SIM
        visual = UiDialogNotification.UiDialogNotificationVisualType.SPECIAL_MOMENT
        button1_text = lambda **_: _create_localized_string(0xD45017C8)
        button2_text = lambda **_: _create_localized_string(0xD45017CA)
        button3_text = lambda **_: _create_localized_string(0xD45017CD)
        button4_text = lambda **_: _create_localized_string(0xD45017CE)

    elif (
            TD1AccessPanelModuleHandler.ACCESSPANEL_ALLOW_BETA_STARTUP_NOTIFICATION is True and debug is False) or scenario == 3:
        notif_title = lambda **_: _create_localized_string(0x29249E2F)
        notif_text = lambda **_: _create_localized_string(0xD45017D0,
                                                          str(TD1AccessPanelModuleHandler.ACCESSPANEL_MOD_VERSION),
                                                          str(TD1AccessPanelModuleHandler.mod_version))
        info_level = UiDialogNotification.UiDialogNotificationLevel.SIM
        visual = UiDialogNotification.UiDialogNotificationVisualType.INFORMATION
        button1_text = lambda **_: _create_localized_string(0xD45017C7)
        button2_text = lambda **_: _create_localized_string(0xD45017C9)
        button3_text = lambda **_: _create_localized_string(0xD45017CC)
        button4_text = lambda **_: _create_localized_string(0xD45017CE)

    # Button Control
    # 1. Discord
    # 2. Patreon
    # 3. Update Posts
    # 4. License

    button1_response_command = make_immutable_slots_class(set(['arguments', 'command']))(
        {'arguments': (), 'command': 'td1devaccess.td1_discord'})
    button2_response_command = make_immutable_slots_class(set(['arguments', 'command']))(
        {'arguments': (), 'command': 'td1devaccess.td1_patreon'})
    button3_response_command = make_immutable_slots_class(set(['arguments', 'command']))(
        {'arguments': (), 'command': 'td1devaccess.td1_dev_update'})
    button4_response_command = make_immutable_slots_class(set(['arguments', 'command']))(
        {'arguments': (), 'command': 'td1devaccess.license'})

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
    button3_response = UiDialogResponse(
        dialog_response_id=ButtonType.DIALOG_RESPONSE_OK,
        ui_request=UiDialogResponse.UiDialogUiRequest.SEND_COMMAND,
        response_command=button3_response_command,
        text=button3_text
    )
    button4_response = UiDialogResponse(
        dialog_response_id=ButtonType.DIALOG_RESPONSE_OK,
        ui_request=UiDialogResponse.UiDialogUiRequest.SEND_COMMAND,
        response_command=button4_response_command,
        text=button4_text
    )

    notification_startup = UiDialogNotification.TunableFactory().default(
        client.active_sim,
        title=notif_title,
        text=notif_text,
        information_level=info_level,
        expand_behavior=UiDialogNotification.UiDialogNotificationExpandBehavior.FORCE_EXPAND,
        visual_type=visual,
        icon=lambda _: IconInfoData(
            icon_resource=get_resource_key(
                0xC45DF1733FED8944, Types.PNG
            )
        ),
        ui_responses=(
            button1_response,
            button2_response,
            button3_response,
            # button4_response
        )
    )
    notification_startup.show_dialog()


@Command('td1devaccess.get_tuning_modifiers', command_type=CommandType.Live)
def get_tuning_modifiers(_connection=None):
    client = services.client_manager().get_first_client()
    output = CheatOutput(_connection)

    status_1 = check_modifier_status(TD1AccessPanelModuleHandler.ACCESSPANEL_IGNORE_MOD_VERSION)
    status_2 = check_modifier_status(TD1AccessPanelModuleHandler.ACCESSPANEL_ALLOW_STARTUP_NOTIFICATION)
    status_3 = check_modifier_status(TD1AccessPanelModuleHandler.ACCESSPANEL_ALLOW_DEVELOPER_STARTUP_NOTIFICATION)
    status_4 = check_modifier_status(TD1AccessPanelModuleHandler.ACCESSPANEL_ALLOW_BETA_STARTUP_NOTIFICATION)
    status_5 = check_modifier_status(TD1AccessPanelModuleHandler.ACCESSPANEL_STARTUP_NOTIFICATION_V2_USAGE)
    status_6 = check_modifier_status(TD1AccessPanelModuleHandler.ACCESSPANEL_ALLOW_INTEGRATION_NOTIFICATION)
    status_7 = check_modifier_status(TD1AccessPanelModuleHandler.ACCESSPANEL_ALLOW_MODIFIER_NOTIFICATION)
    status_8 = check_modifier_status(TD1AccessPanelModuleHandler.ACCESSPANEL_OVERRIDE_PACK_TESTSET)
    status_9 = check_modifier_status(TD1AccessPanelModuleHandler.ACCESSPANEL_OVERRIDE_INTEGRATION_TESTSET)
    status_10 = check_modifier_status(TD1AccessPanelModuleHandler.ACCESSPANEL_OVERRIDE_VERSION_TESTSET)
    status_11 = check_modifier_status(TD1AccessPanelModuleHandler.ACCESSPANEL_OVERRIDE_DEBUG_INTERACTIONS)
    status_12 = check_modifier_status(
        TD1AccessPanelModuleHandler.ACCESSPANEL_FORCE_DEBUG_INTERACTIONS_INTO_CHEAT_PIE_MENU)
    # status_13 = check_modifier_status(TD1AccessPanelModuleHandler.ACCESSPANEL_OVERRIDE_DEBUG_COMMANDS)

    ignore_version_txt = "[Ignore Mod Version]: " + status_1
    regular_notif_text = "[Startup Notification]: " + status_2
    dev_notif_text = "[Developer Notification]: " + status_3
    beta_notif_text = "[Beta Notification]: " + status_4
    v2_notif_text = "[Use Version 2 Notif System]: " + status_5
    integration_text = "[Integration Notification]: " + status_6
    modifier_text = "[Modifier Notification]: " + status_7
    pack_text = "[Pack TestSet Override]: " + status_8
    integration_test_text = "[Integration TestSet Override]: " + status_9
    version_test_text = "[Version TestSet Override]: " + status_10
    override_int_debug_text = "[Override Debug Interactions]: " + status_11
    cheat_debug_int_text = "[Force Debug Cheats into Cheat Pie Menu]: " + status_12
    # override_commands_text = "[Override/Unlock Debug Commands]: " + status_13
    text_last = "These modifier tunings can be found inside the TD1_DevAccessPanel_ModuleHandler Tuning. Certain modifiers can lead to LEs should you not meet certain requirements."

    notif_text = ignore_version_txt + '\n\n' + regular_notif_text + '\n\n' + dev_notif_text + '\n\n' + beta_notif_text + '\n\n' + v2_notif_text + '\n\n' + integration_text + '\n\n' + modifier_text + '\n\n' + pack_text + '\n\n' + integration_test_text + '\n\n' + version_test_text + '\n\n' + override_int_debug_text + '\n\n' + cheat_debug_int_text + '\n\n' + text_last

    notification_modifiers = UiDialogNotification.TunableFactory().default(
        client.active_sim,
        title=lambda **_: LocalizationHelperTuning.get_raw_text("TD1 Developer Access Panel Tuning Modifiers"),
        text=lambda **_: LocalizationHelperTuning.get_raw_text(notif_text),
        information_level=UiDialogNotification.UiDialogNotificationLevel.SIM,
        expand_behavior=UiDialogNotification.UiDialogNotificationExpandBehavior.FORCE_EXPAND,
        visual_type=UiDialogNotification.UiDialogNotificationVisualType.SPECIAL_MOMENT
    )
    notification_modifiers.show_dialog()


def check_modifier_status(status):
    if status is True:
        result = "ENABLED"
        return result
    else:
        result = "DISABLED"
        return result


@Command('td1devaccess.reset_startup_notif', command_type=CommandType.Live)
def reset_startup_notif(_connection=None):
    output = CheatOutput(_connection)
    if TD1AccessPanelModuleHandler.notification_ran is True:
        TD1AccessPanelModuleHandler.notification_ran = False
        output('Startup Notification has been reset. Notifications will show up on next load.')
    else:
        output('Startup Notification has not ran yet. Notifications will show up on next load.')


@Command('td1devaccess.enablefreebuild', command_type=CommandType.Live)
def force_enable_free_build(_connection=None):
    output = CheatOutput(_connection)
    output('Forcing Free Build Mode...')
    result = get_command_and_sort_from_list('bb.enablefreebuild', True, _connection)
    if result.find('[FAILURE]') == -1:
        output('{}'.format(result))
    else:
        output('Cheat: bb.enablefreebuild is enabled. Budget is set to Infinity Simoleons.')


@Command('td1devaccess.show_interaction_tuning_name', command_type=CommandType.Live)
def change_interaction_naming(enable: bool, _connection=None):
    output = CheatOutput(_connection)
    output('Changing Interaction Naming...')
    show_interaction_tuning_name(enable)


@Command('td1devaccess.call_client_command', 'td1devaccess.call', 'call_command', command_type=CommandType.Live)
def call_client_command(identifier: str, state: bool, _connection=None):
    output = CheatOutput(_connection)

    identifier_lc = identifier.lower()

    result = get_command_and_sort_from_list(identifier_lc, state, _connection)
    output('{}'.format(result))


def get_command_and_sort_from_list(identifier, state, _connection):
    if identifier is None:
        result = '[FAILURE] Command Identifier Missing. Please specify command.'
        return result
    if state is None:
        state = False
    for (enable_cmd, disable_cmd, is_client) in client_commands_list:
        if enable_cmd.find(identifier) != -1:
            if is_client is True:
                if state is True:
                    client_cheat(enable_cmd, _connection)
                    result = '[SUCCESS] Client Cheat: ' + str(enable_cmd) + ' is now enabled.'
                    return result
                else:
                    client_cheat(disable_cmd, _connection)
                    result = '[SUCCESS] Client Cheat: ' + str(disable_cmd) + ' is now disabled.'
                    return result
            else:
                if state is True:
                    execute(enable_cmd, _connection)
                    result = '[SUCCESS] Command Cheat: ' + str(enable_cmd) + ' is now enabled.'
                    return result
                else:
                    execute(disable_cmd, _connection)
                    result = '[SUCCESS] Command Cheat: ' + str(disable_cmd) + ' is now disabled.'
                    return result
    result = '[FAILURE] Command: ' + str(identifier) + ' is not within TD1 Developer Access Panel Client Command List.'
    return result


@Command('td1devaccess.show_client_command_list', command_type=CommandType.Live)
def show_commands_list(_connection=None):
    output = CheatOutput(_connection)
    text = get_command_and_print_from_list(_connection)
    # output("{}".format(text))


def get_command_and_print_from_list(_connection):
    output = CheatOutput(_connection)
    init_title = 'Client Commands List (For use with td1devaccess.call)'
    disabler = ''
    text = ''
    is_client_str = ''
    holder_text = ''
    full_text = ''
    output("{}".format(init_title))
    for (enable_cmd, disable_cmd, is_client) in client_commands_list:
        if disable_cmd is not '':
            disabler = disable_cmd
        else:
            disabler = 'None'
        if is_client is True:
            is_client_str = 'Yes'
        else:
            is_client_str = 'No'
        text = '\n\nEnable Command: ' + str(enable_cmd) + '\nDisable Command: ' + str(
            disabler) + '\n Is Client: ' + str(is_client_str)
        output("{}".format(text))
        holder_text += text
    full_text += holder_text
    return full_text


@Command('td1devaccess.help', command_type=CommandType.Live)
def list_all_commands(notif: bool = False, _connection=None):
    output = CheatOutput(_connection)
    client = services.client_manager().get_first_client()
    init_text = '[TD1 Developer Access Panel Commands List]'
    main_init = '[Main Commands]'
    funds_init = '[Funds Commands]'
    bucks_init = '[Bucks Commands]'
    eco_fp_init = '[Eco Footprint Commands]'
    club_init = '[Club Commands]'
    civic_init = '[Civic Policy Commands]'
    mtx_init = '[MTX Commands]'
    client_init = '[Client Cheat Commands]'
    main_cmd_list = ''
    main_cmd_list_2 = ''
    funds_cmd_list = ''
    bucks_cmd_list = ''
    eco_fp_cmd_list = ''
    club_cmd_list = ''
    civic_cmd_list = ''
    mtx_cmd_list = ''
    client_cmd_list = ''
    misc_cmd_list = ''
    main_cmd_count = 1

    for (cmd, params, state, desc, tag) in command_lists:
        if tag.find('main') != -1:
            to_merge = str(state) + ' ' + str(cmd) + ' ' + str(params) + '\n' + str(desc) + '\n\n'
            if main_cmd_count <= 6:
                main_cmd_list += to_merge
                main_cmd_count += 1
            elif main_cmd_count <= 12:
                main_cmd_list_2 += to_merge
                main_cmd_count += 1

        elif tag.find('funds') != -1:
            to_merge = str(state) + ' ' + str(cmd) + ' ' + str(params) + '\n' + str(desc) + '\n\n'
            funds_cmd_list += to_merge

        elif tag.find('bucks') != -1:
            to_merge = str(state) + ' ' + str(cmd) + ' ' + str(params) + '\n' + str(desc) + '\n\n'
            bucks_cmd_list += to_merge

        elif tag.find('ecofootprint') != -1:
            to_merge = str(state) + ' ' + str(cmd) + ' ' + str(params) + '\n' + str(desc) + '\n\n'
            eco_fp_cmd_list += to_merge

        elif tag.find('club') != -1:
            to_merge = str(state) + ' ' + str(cmd) + ' ' + str(params) + '\n' + str(desc) + '\n\n'
            club_cmd_list += to_merge

        elif tag.find('civic') != -1:
            to_merge = str(state) + ' ' + str(cmd) + ' ' + str(params) + '\n' + str(desc) + '\n\n'
            civic_cmd_list += to_merge

        elif tag.find('mtx') != -1:
            to_merge = str(state) + ' ' + str(cmd) + ' ' + str(params) + '\n' + str(desc) + '\n\n'
            mtx_cmd_list += to_merge

        elif tag.find('client') != -1:
            to_merge = str(state) + ' ' + str(cmd) + ' ' + str(params) + '\n' + str(desc) + '\n\n'
            client_cmd_list += to_merge

        else:
            to_merge = str(state) + ' ' + str(cmd) + ' ' + str(params) + '\n' + str(desc) + '\n\n'
            misc_cmd_list += to_merge

    def debug_print_list_console():
        output('{} \n'.format(init_text))
        output('{} \n'.format(main_init))
        output('{} \n'.format(main_cmd_list))
        output('{} \n'.format(main_cmd_list_2))
        output('{} \n'.format(funds_init))
        output('{} \n'.format(funds_cmd_list))
        output('{} \n'.format(bucks_init))
        output('{} \n'.format(bucks_cmd_list))
        output('{} \n'.format(eco_fp_init))
        output('{} \n'.format(eco_fp_cmd_list))
        output('{} \n'.format(club_init))
        output('{} \n'.format(club_cmd_list))
        output('{} \n'.format(civic_init))
        output('{} \n'.format(civic_cmd_list))
        output('{} \n'.format(mtx_init))
        output('{} \n'.format(mtx_cmd_list))
        output('{} \n'.format(client_init))
        output('{} \n'.format(client_cmd_list))

    debug_print_list_console()

    if notif is True:
        final_text_1 = str(main_init) + '\n' + str(main_cmd_list) + str(main_cmd_list_2) + '\n' + str(
            funds_init) + '\n' + str(funds_cmd_list) + '\n' + str(bucks_init) + '\n' + str(bucks_cmd_list)
        final_text_2 = str(eco_fp_init) + '\n' + str(eco_fp_cmd_list) + '\n' + str(club_init) + '\n' + str(
            club_cmd_list)
        final_text_3 = str(civic_init) + '\n' + str(civic_cmd_list) + '\n' + str(mtx_init) + '\n' + str(
            mtx_cmd_list) + '\n' + str(client_init) + '\n' + str(client_cmd_list)

        message_title_1 = lambda **_: LocalizationHelperTuning.get_raw_text("TD1 Developer Access Panel Commands")
        message_text_1 = lambda **_: LocalizationHelperTuning.get_raw_text(str(final_text_1))

        notification_1 = UiDialogNotification.TunableFactory().default(
            client.active_sim,
            text=message_text_1,
            title=message_title_1
        )

        message_title_2 = lambda **_: LocalizationHelperTuning.get_raw_text("TD1 Developer Access Panel Commands")
        message_text_2 = lambda **_: LocalizationHelperTuning.get_raw_text(str(final_text_2))

        notification_2 = UiDialogNotification.TunableFactory().default(
            client.active_sim,
            text=message_text_2,
            title=message_title_2
        )

        message_title_3 = lambda **_: LocalizationHelperTuning.get_raw_text("TD1 Developer Access Panel Commands")
        message_text_3 = lambda **_: LocalizationHelperTuning.get_raw_text(str(final_text_3))

        notification_3 = UiDialogNotification.TunableFactory().default(
            client.active_sim,
            text=message_text_3,
            title=message_title_3
        )
        notification_1.show_dialog()
        notification_2.show_dialog()
        notification_3.show_dialog()

        main_cmd_list = None
        main_cmd_list_2 = None
        funds_cmd_list = None
        bucks_cmd_list = None
        eco_fp_cmd_list = None
        club_cmd_list = None
        civic_cmd_list = None
        mtx_cmd_list = None
        client_cmd_list = None
        misc_cmd_list = None
