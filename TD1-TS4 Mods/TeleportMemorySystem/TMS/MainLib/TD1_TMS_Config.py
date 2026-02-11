"""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
TwelfthDoctor1's Teleport Memory System

> Config Tuning

(C) Copyright TD1 & TWoCC 2020 - 2021
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Licensed under CC-BY-NC-ND 4.0

https://creativecommons.org/licenses/by-nc-nd/4.0/

Codes from other parties are not part of the License and Copyright.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""
import os
import configparser
from pathlib import Path
import services
from sims4.commands import Command, CommandType, Output
from sims4.localization import LocalizationHelperTuning
from sims4.tuning.tunable import TunableMapping, Tunable, TunableTuple
from ui.ui_dialog import UiDialogOkCancel
from ui.ui_dialog_generic import UiDialogTextInputOkCancel
from ui.ui_dialog_notification import UiDialogNotification
from TMS.UtilLib.ConfigJSON import ConfigJSON
from TMS.UtilLib.ConfigTemplate import CONFIG_NAME, CONFIG_DEFAULT, CONFIG_CHANGE_SHOW

# Importation of MasterApprentice Logger

try:
    from MasterApprenticeLib.TD1_Lib_ApprenticeLogger import ApprenticeLogger

    apprentice_logger = ApprenticeLogger('TD1 Teleport Memory System Config', main_owner='TwelfthDoctor1')

except ImportError:
    apprentice_logger = False

try:
    from MasterApprenticeLib.TD1_Lib_MasterLogger import MasterLogger

    master_logger = MasterLogger('TD1 Teleport Memory System Config', main_owner='TwelfthDoctor1')

except ImportError:
    master_logger = False


class TD1TMSConfigHandlerUI:
    CONFIG_UI_TEXT_INPUT = 'config_value'
    CONFIG_UI_TEXT_DISPLAY = TunableMapping(
        description='List to hold the UI Text for each option.',
        key_name='option_type',
        key_type=Tunable(
            description='The option type for the UI to be associated with.',
            tunable_type=str,
            default=''
        ),
        value_name='ui_data',
        value_type=TunableTuple(
            ok_cancel=UiDialogOkCancel.TunableFactory(
                description='Meant for Boolean Options.',
            ),
            text_input=UiDialogTextInputOkCancel.TunableFactory(
                description='Meant for String, Integer and Float Options. For 1 Text Input.',
                text_inputs=(CONFIG_UI_TEXT_INPUT),
            ),
        )
    )


main_dir = Path(__file__).resolve().parent.parent.parent.parent

config = ConfigJSON(CONFIG_NAME)
config.generate_config()
config.getConfigData()

main_header = 'TD1 Teleport Memory System Config Settings'

# convert = False


@Command('tms.list_config', command_type=CommandType.Live)
def print_config_values(_connection=None):
    output = Output(_connection)
    config.getConfigData()

    for k, v in config.return_json().items():
        output(f"{k}: {v}")


@Command('tms.list_config_notif', command_type=CommandType.Live)
def print_config_values_notif(_connection=None):
    client = services.client_manager().get_first_client()
    output = Output(_connection)
    config.getConfigData()
    text_final = ""
    for k, v in config.return_json().items():
        output(f"{k}: {v}")
        text_final += f'[{k}]: {v}\n\n'
    text_final += 'These modifier tunings can be found inside the TD1_TMS_Settings.cfg file. Use the Settings Panel to modify settings.'
    message_title = lambda **_: LocalizationHelperTuning.get_raw_text('TD1 Teleport Memory System Mod Configurations')
    message_text = lambda **_: LocalizationHelperTuning.get_raw_text(text_final)
    notification = UiDialogNotification.TunableFactory().default(
        client.active_sim,
        text=message_text,
        title=message_title,
        information_level=UiDialogNotification.UiDialogNotificationLevel.SIM,
        expand_behavior=UiDialogNotification.UiDialogNotificationExpandBehavior.FORCE_EXPAND,
        visual_type=UiDialogNotification.UiDialogNotificationVisualType.SPECIAL_MOMENT
    )
    notification.show_dialog()


@Command('tms.list_config_all', command_type=CommandType.Live)
def print_all_config_values(_connection=None):
    output = Output(_connection)
    config.getConfigData()

    for k, v in config.return_json().items():
        output(f"{k}: {v}")

    for (option_type, dialog_data) in TD1TMSConfigHandlerUI.CONFIG_UI_TEXT_DISPLAY.items():
        output(f"{option_type}")


@Command('tms.set_option', command_type=CommandType.Live)
def config_set_option(option, _connection=None):
    output = Output(_connection)
    config.getConfigData()

    if option in config.return_json():
        for (option_type, dialog_data) in TD1TMSConfigHandlerUI.CONFIG_UI_TEXT_DISPLAY.items():
            if option_type == option:
                client = services.client_manager().get_first_client()
                if type(CONFIG_DEFAULT[option]) == bool:
                    def on_response(dialog):
                        if dialog.accepted:
                            option_toggle(option)

                    dialog = dialog_data.ok_cancel(None)
                    dialog.add_listener(on_response)
                    dialog.show_dialog()
                else:
                    def on_response(dialog):
                        if dialog.accepted:
                            option_toggle(option, str(dialog.text_input_responses.get("config_value")))

                    dialog = dialog_data.text_input(None)
                    dialog.add_listener(on_response)
                    dialog.show_dialog()

    else:
        output("Wrong Option Specified. Please refer to config list and try again.")


def option_toggle(config_key, to_set:str=''):
    client = services.client_manager().get_first_client()

    cfg_value = config.return_specific_json(config_key)

    if type(cfg_value) == bool:
        config.update_specific_json(config_key, not cfg_value)

        to_set = not cfg_value

    elif type(cfg_value) == int or type(cfg_value) == float:
        if to_set.isdigit():
            config.update_specific_json(config_key, int(to_set))
        else:
            config.update_specific_json(config_key, float(to_set))

    else:
        config.update_specific_json(config_key, str(to_set))

    config.update_json_file()

    if apprentice_logger is not None and apprentice_logger is not False:
        apprentice_logger.info(
            f"Option: {config_key} has been set to {to_set}. (Formerly {cfg_value})",
            owner="TwelfthDoctor1")

    if master_logger is not None and master_logger is not False:
        master_logger.info(f"Option: {config_key} has been set to {to_set}. (Formerly {cfg_value})",
                           owner="TwelfthDoctor1")

    if CONFIG_CHANGE_SHOW[config_key] is True:
        dialog_message = f"The option: {config_key} has been changed from {cfg_value} to {to_set}.\n\nA restart may be required for changes to take effect."

    else:
        dialog_message = f"The option: {config_key} has been changed from {cfg_value} to {to_set}."

    message_title_config_change = lambda **_: LocalizationHelperTuning.get_raw_text("Access Panel Option Change")
    message_text_config_change = lambda **_: LocalizationHelperTuning.get_raw_text(dialog_message)

    notification_config_change = UiDialogNotification.TunableFactory().default(
        client.active_sim,
        text=message_text_config_change,
        title=message_title_config_change,
        expand_behavior=UiDialogNotification.UiDialogNotificationExpandBehavior.FORCE_EXPAND,
        urgency=UiDialogNotification.UiDialogNotificationUrgency.URGENT
    )
    notification_config_change.show_dialog()


def get_option_value(option):
    """
    Gets the value from the option (key) in the Config List.
    :param option:
    :return:
    """
    config.getConfigData()
    return config.return_specific_json(option)


def config_exist(option):
    config.getConfigData()
    if option in config.json_data:
        return True
    else:
        return False


@Command("tms.convert_cfg_to_json")
def config_convert_to_json(_connection=None):
    output = Output(_connection)
    old_cfg_name = "TD1_TMS_Settings.cfg"

    old_config_dir = os.path.join(main_dir, old_cfg_name)
    if os.path.exists(old_config_dir):
        output(f"Old ConfigParser file found. Process conversion...")

        if master_logger is not None and master_logger is not False:
            master_logger.info(f"Old ConfigParser file found. Process conversion...")

        config_old = configparser.ConfigParser()

        with open(old_config_dir, "r") as old_config_file:
            config_old.read_file(old_config_file)
            old_data = dict(config_old.items(main_header))
            old_config_file.close()

        old_data_convert = dict()

        for k, v in old_data.items():
            if v == "True":
                old_data_convert[k] = True

            elif v == "False":
                old_data_convert[k] = False

            elif v.isdigit():
                old_data_convert[k] = int(v)

            elif v.isdecimal():
                old_data_convert[k] = float(v)

            else:
                old_data_convert[k] = str(v)

        for k, v in old_data_convert.items():
            output(f"CONVERSION STATUS\n\n{k} : {v} | TYPE: {type(v)}")

            if master_logger is not None and master_logger is not False:
                master_logger.info(
                    f"CONVERSION STATUS\n\n{k} : {v} | TYPE: {type(v)}"
                )
            config.update_specific_json(k, v)

        config.update_json_file()

        os.remove(old_config_dir)

        output(f"Conversion Complete, old Config File will be deleted.")

        if master_logger is not None and master_logger is not False:
            master_logger.info(
                f"Old Config File deleted."
            )
    else:
        output(f"Old Config File not detected. Conversion will not be processed.")
