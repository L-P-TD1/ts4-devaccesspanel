import services
from bucks.bucks_commands import get_bucks_tracker, get_bucks_types_without_invalid_gen, get_short_buck_type
from bucks.bucks_enums import BucksType
from bucks.bucks_utils import BucksUtils
from distributor.shared_messages import IconInfoData
from protocolbuffers import Consts_pb2
from server_commands.argument_helpers import get_optional_target, OptionalTargetParam
from sims4.collections import FrozenAttributeDict, AttributeDict
from sims4.commands import Command, CommandType, CheatOutput, execute
from sims4.common import Pack
from sims4.localization import LocalizationHelperTuning
from sims4.resources import get_resource_key, Types
from sims4.tuning.tunable import HasTunableSingletonFactory, AutoFactoryInit
from ui.ui_dialog_generic import UiDialogTextInputOkCancel
from ui.ui_dialog_notification import UiDialogNotification
from ui.ui_text_input import UiTextInput
from sims4.localization import _create_localized_string


class DevAccessBaseControl_TextInputLength(HasTunableSingletonFactory, AutoFactoryInit):
    __qualname__ = 'DevAccessBaseControl_TextInputLength'

    def build_msg(self, dialog, msg, *additional_tokens):
        msg.max_length = 30
        msg.min_length = 1


@Command('td1devaccess.modify_funds', command_type=CommandType.Live)
def devaccess_modify_simoleons(household_id:int=0, _connection=None, reason_for_modification=None):
    output = CheatOutput(_connection)
    client = services.client_manager().get_first_client()

    if reason_for_modification is None:
        reason_for_modification = Consts_pb2.TELEMETRY_MONEY_CHEAT

    if household_id == 0:

        tgt_client = services.client_manager().get(_connection)

        if tgt_client is not None:

            household = tgt_client.household

    else:

        household = services.household_manager().get(household_id)

    def get_inputs_callback(dialog):
        if not dialog.accepted:
            output("Dialog was cancelled")
            return
        funds_to_modify = int(dialog.text_input_responses.get("input_number"))
        output("User typed '{}'".format(funds_to_modify))

        if household is not None:

            household_init_amount = int(household.funds.money)

            output('{}'.format(household_init_amount))

            household_amount_for_test = household_init_amount + funds_to_modify

            output('{}'.format(household_amount_for_test))

            if household_amount_for_test > 0:

                output('{} Simoleons will be left after this operation.'.format(household_amount_for_test))

            else:

                output('{} Simoleons will lead to a negative Simoleon which equates to: {} Simoleons'.format(funds_to_modify, household_amount_for_test))

                failure_title = lambda **_: LocalizationHelperTuning.get_raw_text("Modification Failure")
                failure_text = lambda **_: LocalizationHelperTuning.get_raw_text("Not enough § Simoleons for a deduction.")

                notification_failure = UiDialogNotification.TunableFactory().default(
                    client.active_sim,
                    text=failure_text,
                    title=failure_title
                )
                notification_failure.show_dialog()

                return

        else:

            output('No Household specified.')

            return

        if funds_to_modify > 0:

            household.funds.add(funds_to_modify, reason_for_modification)

            success_title = lambda **_: LocalizationHelperTuning.get_raw_text("Simoleon Addition Success")
            success_text = lambda **_: LocalizationHelperTuning.get_raw_text("§" + str(funds_to_modify) + " has been added.")  # _create_localized_string(3535052052)

            notification_success = UiDialogNotification.TunableFactory().default(
                client.active_sim,
                text=success_text,
                title=success_title
            )
            notification_success.show_dialog()

        else:

            household.funds.try_remove(-funds_to_modify, reason_for_modification)

            success_title = lambda **_: LocalizationHelperTuning.get_raw_text("Simoleon Deduction Success")
            success_text = lambda **_: LocalizationHelperTuning.get_raw_text("§" + str(-funds_to_modify) + " has been deducted.")  # _create_localized_string(3535052052)

            notification_success = UiDialogNotification.TunableFactory().default(
                client.active_sim,
                text=success_text,
                title=success_title
            )
            notification_success.show_dialog()

        # End of the callback

    # Create the dialog title and text from a raw text string
    """
    Note: Not all string are in use, most of the LocalizationHelperTunings are disabled. Only those with Variable amount will use it.
    """
    localized_title = lambda **_: LocalizationHelperTuning.get_raw_text("Modify Household Funds")
    localized_text = lambda **_: LocalizationHelperTuning.get_raw_text("Indicate the amount of § Simoleons that are to be added or removed (For negative values, use -(Number)):")
    localized_initial_value = lambda **_: LocalizationHelperTuning.get_raw_text("")

    # This defines our input fields
    input_funds = UiTextInput(sort_order=0, restricted_characters=None)
    input_funds.default_text = None
    input_funds.title = None
    input_funds.max_length = 30
    input_funds.initial_value = localized_initial_value
    input_funds.length_restriction = DevAccessBaseControl_TextInputLength()
    input_funds.check_profanity = False
    input_funds.height = False

    inputs = AttributeDict({'input_number': input_funds})

    # Create the actual dialog object...
    dialog = UiDialogTextInputOkCancel.TunableFactory().default(client.active_sim, text=localized_text, title=localized_title, text_inputs=inputs)
    icon = get_resource_key(0, Types.PNG)

    dialog.add_listener(get_inputs_callback)
    dialog.show_dialog(icon_override=IconInfoData(icon_resource=icon))
    output("Main function done")


@Command('td1devaccess.set_funds', command_type=CommandType.Live)
def devaccess_set_simoleons(household_id:int=0, _connection=None, reason_for_modification=None):
    output = CheatOutput(_connection)
    client = services.client_manager().get_first_client()

    if reason_for_modification is None:
        reason_for_modification = Consts_pb2.TELEMETRY_MONEY_CHEAT

    if household_id == 0:

        tgt_client = services.client_manager().get(_connection)

        if tgt_client is not None:
            household = tgt_client.household

    else:

        household = services.household_manager().get(household_id)

    test_money = household.funds.money

    output('Current Funds: {}, Household ID: {}'.format(test_money, household))

    def get_inputs_callback(dialog):
        if not dialog.accepted:

            output("Dialog was cancelled")

            return

        funds_to_set = int(dialog.text_input_responses.get('input_number'))

        output("User typed '{}'".format(funds_to_set))

        if household is not None:

            household_init_amount = int(household.funds.money)

            if funds_to_set > household_init_amount:

                household_amount_for_test = funds_to_set - household_init_amount

            else:

                household_amount_for_test = household_init_amount - funds_to_set

            if household_amount_for_test > 0:

                output('{} Simoleons will be added/deducted after this operation.'.format(household_amount_for_test))

            else:

                output('{} Simoleons will lead to a negative Simoleon which equates to: {} Simoleons'.format(funds_to_set, household_amount_for_test))

                failure_title = lambda **_: LocalizationHelperTuning.get_raw_text("Modification Failure")
                failure_text = lambda **_: LocalizationHelperTuning.get_raw_text("Not enough § Simoleons for a deduction.")

                notification_failure = UiDialogNotification.TunableFactory().default(
                    client.active_sim,
                    text=failure_text,
                    title=failure_title
                )
                notification_failure.show_dialog()

                return

        else:

            output('No Household specified.')

            return

        set_funds_value = funds_to_set - household_init_amount

        if set_funds_value > 0:

            household.funds.add(set_funds_value, reason_for_modification)

            success_title = lambda **_: LocalizationHelperTuning.get_raw_text("Simoleon Addition Success")
            success_text = lambda **_: LocalizationHelperTuning.get_raw_text("§" + str(set_funds_value) + " has been added.")  # _create_localized_string(3535052052)

            notification_success = UiDialogNotification.TunableFactory().default(
                client.active_sim,
                text=success_text,
                title=success_title
            )
            notification_success.show_dialog()

        else:

            household.funds.try_remove(-set_funds_value, reason_for_modification)

            success_title = lambda **_: LocalizationHelperTuning.get_raw_text("Simoleon Deduction Success")
            success_text = lambda **_: LocalizationHelperTuning.get_raw_text("§" + str(-set_funds_value) + " has been deducted.")  # _create_localized_string(3535052052)

            notification_success = UiDialogNotification.TunableFactory().default(
                client.active_sim,
                text=success_text,
                title=success_title
            )
            notification_success.show_dialog()

        # End of the callback

    # Create the dialog title and text from a raw text string
    """
    Note: Not all string are in use, most of the LocalizationHelperTunings are disabled. Only those with Variable amount will use it.
    """
    localized_title = lambda **_: LocalizationHelperTuning.get_raw_text("Modify Household Funds")
    localized_text = lambda **_: LocalizationHelperTuning.get_raw_text("Indicate the number of § Simoleons that are to be added or deducted (For negative values, use -(Number)):")
    localized_initial_value = lambda **_: LocalizationHelperTuning.get_raw_text("")

    # This defines our input fields
    input_simoleons = UiTextInput(sort_order=0, restricted_characters=None)
    input_simoleons.default_text = None
    input_simoleons.title = None
    input_simoleons.max_length = 30
    input_simoleons.initial_value = localized_initial_value
    input_simoleons.length_restriction = DevAccessBaseControl_TextInputLength()
    input_simoleons.check_profanity = False
    input_simoleons.height = False

    inputs = AttributeDict({'input_number': input_simoleons})

    # Create the actual dialog object...
    dialog = UiDialogTextInputOkCancel.TunableFactory().default(client.active_sim, text=localized_text, title=localized_title, text_inputs=inputs)
    icon = get_resource_key(0, Types.PNG)

    dialog.add_listener(get_inputs_callback)
    dialog.show_dialog(icon_override=IconInfoData(icon_resource=icon))
    output("Main function done")


@Command('td1devaccess.modify_bucks', command_type=CommandType.Live)
def modify_bucks(bucks_type:BucksType, actor_sim:int=None, _connection=None):
    output = CheatOutput(_connection)
    client = services.client_manager().get_first_client()

    tracker_actor = get_bucks_tracker(bucks_type, actor_sim, _connection, add_if_none=True)

    if tracker_actor is None:
        return False

    def get_inputs_callback(dialog):
        if not dialog.accepted:
            output("Dialog was cancelled")
            return
        point_to_transfer = int(dialog.text_input_responses.get("input_number"))
        output("User typed '{}'".format(point_to_transfer))

        actor_init_buck_tracker = BucksUtils.get_tracker_for_bucks_type(bucks_type, actor_sim)

        if actor_init_buck_tracker is not None:

            bucks_init_amount = actor_init_buck_tracker.get_bucks_amount_for_type(bucks_type)

            bucks_amount_for_test = bucks_init_amount + point_to_transfer

            if bucks_amount_for_test > 0:

                output('{} Bucks will be left after this operation.'.format(bucks_amount_for_test))

            else:

                output('{} Bucks will lead to a negative Bucks Value which equates to: {} Bucks'.format(point_to_transfer, bucks_amount_for_test))

                failure_title = lambda **_: LocalizationHelperTuning.get_raw_text("Bucks Modification Failure")
                failure_text = lambda **_: LocalizationHelperTuning.get_raw_text("Not enough ▯Bucks for a Modification.\n\nSim only has ▯" + str(bucks_init_amount))

                notification_failure = UiDialogNotification.TunableFactory().default(
                    client.active_sim,
                    text=failure_text,
                    title=failure_title
                )
                notification_failure.show_dialog()

                return

        else:

            output('No Actor Sim specified. Please enter a valid Sim ID when running this command.')

            return

        tracker = get_bucks_tracker(bucks_type, actor_sim, _connection, add_if_none=True)

        if tracker is None:
            return False

        result = tracker.try_modify_bucks(bucks_type, point_to_transfer, reason='Added Via Cheat.')

        if point_to_transfer > 0:
            success_title = lambda **_: LocalizationHelperTuning.get_raw_text("Bucks Addition Success")
            success_text = lambda **_: LocalizationHelperTuning.get_raw_text("▯" + str(point_to_transfer) + " have been added.\n\nSim now has ▯" + str(bucks_amount_for_test))  # _create_localized_string(1956515011)

            notification_success = UiDialogNotification.TunableFactory().default(
                client.active_sim,
                text=success_text,
                title=success_title
            )
            notification_success.show_dialog()
        else:
            success_title = lambda **_: LocalizationHelperTuning.get_raw_text("Bucks Deduction Success")
            success_text = lambda **_: LocalizationHelperTuning.get_raw_text("▯" + str(point_to_transfer) + " have been deducted.\n\nSim now has ▯" + str(bucks_amount_for_test))  # _create_localized_string(1956515011)

            notification_success = UiDialogNotification.TunableFactory().default(
                client.active_sim,
                text=success_text,
                title=success_title
            )
            notification_success.show_dialog()

        # End of the callback

    # Create the dialog title and text from a raw text string
    """
    Note: Not all string are in use, most of the LocalizationHelperTunings are disabled. Only those with Variable amount will use it.
    """
    localized_title = lambda **_: LocalizationHelperTuning.get_raw_text("Modify Bucks")
    localized_text = lambda **_: LocalizationHelperTuning.get_raw_text("Indicate the number of ▯ Bucks that are to be added or deducted (For negative values, use -(Number)):")
    localized_initial_value = lambda **_: LocalizationHelperTuning.get_raw_text("")

    # This defines our input fields
    input_points = UiTextInput(sort_order=0, restricted_characters=None)
    input_points.default_text = None
    input_points.title = None
    input_points.max_length = 30
    input_points.initial_value = localized_initial_value
    input_points.length_restriction = DevAccessBaseControl_TextInputLength()
    input_points.check_profanity = False
    input_points.height = False

    inputs = AttributeDict({'input_number': input_points})

    # Create the actual dialog object...
    dialog = UiDialogTextInputOkCancel.TunableFactory().default(client.active_sim, text=localized_text,
                                                                title=localized_title, text_inputs=inputs, text_tokens=inputs)
    icon = get_resource_key(0, Types.PNG)

    dialog.add_listener(get_inputs_callback)
    dialog.show_dialog(icon_override=IconInfoData(icon_resource=icon))
    output("Main function done")


@Command('td1devaccess.set_bucks', command_type=CommandType.Live)
def set_bucks(bucks_type:BucksType, actor_sim: int = None, _connection=None):
    output = CheatOutput(_connection)
    client = services.client_manager().get_first_client()

    tracker_actor = get_bucks_tracker(bucks_type, actor_sim, _connection, add_if_none=True)

    if tracker_actor is None:
        return False

    def get_inputs_callback(dialog):
        if not dialog.accepted:
            output("Dialog was cancelled")
            return
        point_to_transfer = int(dialog.text_input_responses.get("input_number"))
        output("User typed '{}'".format(point_to_transfer))

        actor_init_buck_tracker = BucksUtils.get_tracker_for_bucks_type(bucks_type, actor_sim)

        if actor_init_buck_tracker is not None:

            bucks_init_amount = actor_init_buck_tracker.get_bucks_amount_for_type(bucks_type)

            if point_to_transfer > bucks_init_amount:

                bucks_amount_for_test = point_to_transfer - bucks_init_amount

            else:

                bucks_amount_for_test = bucks_init_amount - point_to_transfer

            if bucks_amount_for_test > 0:

                output('{} Bucks will be added/deducted after this operation.'.format(bucks_amount_for_test))

            else:

                output(
                    '{} Bucks will lead to a negative Bucks Value which equates to: {} Bucks'.format(point_to_transfer,
                                                                                                     bucks_amount_for_test))

                failure_title = lambda **_: LocalizationHelperTuning.get_raw_text("Bucks Modification Failure")
                failure_text = lambda **_: LocalizationHelperTuning.get_raw_text("Not enough ▯ Bucks for a Modification.\n\nSim only has ▯" + str(bucks_init_amount))

                notification_failure = UiDialogNotification.TunableFactory().default(
                    client.active_sim,
                    text=failure_text,
                    title=failure_title
                )
                notification_failure.show_dialog()

                return

        else:

            output('No Actor Sim specified. Please enter a valid Sim ID when running this command.')

            return

        tracker = get_bucks_tracker(bucks_type, actor_sim, _connection, add_if_none=True)

        if tracker is None:
            return False

        set_bucks_value = point_to_transfer - bucks_init_amount

        result = tracker.try_modify_bucks(bucks_type, set_bucks_value, reason='Added Via Cheat.')

        if set_bucks_value > 0:
            success_title = lambda **_: LocalizationHelperTuning.get_raw_text("Bucks Addition Success")
            success_text = lambda **_: LocalizationHelperTuning.get_raw_text("▯" + str(point_to_transfer) + " have been added.\n\nSim now has ▯ " + str(set_bucks_value))  # _create_localized_string(1956515011)

            notification_success = UiDialogNotification.TunableFactory().default(
                client.active_sim,
                text=success_text,
                title=success_title
            )
            notification_success.show_dialog()
        else:
            success_title = lambda **_: LocalizationHelperTuning.get_raw_text("Bucks Deduction Success")
            success_text = lambda **_: LocalizationHelperTuning.get_raw_text("▯" + str(-point_to_transfer) + " have been deducted.\n\nSim now has ▯" + str(set_bucks_value))  # _create_localized_string(1956515011)

            notification_success = UiDialogNotification.TunableFactory().default(
                client.active_sim,
                text=success_text,
                title=success_title
            )
            notification_success.show_dialog()

        # End of the callback

    # Create the dialog title and text from a raw text string
    """
    Note: Not all string are in use, most of the LocalizationHelperTunings are disabled. Only those with Variable amount will use it.
    """
    localized_title = lambda **_: LocalizationHelperTuning.get_raw_text("Modify Bucks")
    localized_text = lambda **_: LocalizationHelperTuning.get_raw_text("Indicate the number of ▯ Bucks that are to be added or deducted (For negative values, use -(Number)):")
    localized_initial_value = lambda **_: LocalizationHelperTuning.get_raw_text("")

    # This defines our input fields
    input_points_1 = UiTextInput(sort_order=0, restricted_characters=None)
    input_points_1.default_text = None
    input_points_1.title = None
    input_points_1.max_length = 30
    input_points_1.initial_value = localized_initial_value
    input_points_1.length_restriction = DevAccessBaseControl_TextInputLength()
    input_points_1.check_profanity = False
    input_points_1.height = False

    inputs = AttributeDict({'input_number': input_points_1})

    # Create the actual dialog object...
    dialog = UiDialogTextInputOkCancel.TunableFactory().default(client.active_sim, text=localized_text, title=localized_title, text_inputs=inputs, text_tokens=inputs)
    icon = get_resource_key(0, Types.PNG)

    dialog.add_listener(get_inputs_callback)
    dialog.show_dialog(icon_override=IconInfoData(icon_resource=icon))
    output("Main function done")
