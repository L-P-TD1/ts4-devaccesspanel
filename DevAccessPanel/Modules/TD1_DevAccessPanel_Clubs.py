"""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
TwelfthDoctor1's Developer/Debug Access Panel

> Clubs Module

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
import services
from bucks.bucks_commands import get_bucks_tracker
from bucks.bucks_enums import BucksType
from bucks.bucks_utils import BucksUtils
from clubs.club_commands import _get_club_service
from clubs.club_tuning import ClubTunables
from distributor.shared_messages import IconInfoData
from server_commands.argument_helpers import RequiredTargetParam
from sims4.collections import AttributeDict
from sims4.commands import Command, CommandType, output, CheatOutput
from sims4.common import Pack
from sims4.localization import LocalizationHelperTuning
from sims4.resources import get_resource_key, Types
from sims4.tuning.tunable import HasTunableSingletonFactory, AutoFactoryInit
from ui.ui_dialog_generic import UiDialogTextInputOkCancel
from ui.ui_dialog_notification import UiDialogNotification
from ui.ui_text_input import UiTextInput


class DevAccessClubsControl_TextInputLength(HasTunableSingletonFactory, AutoFactoryInit):
    __qualname__ = 'DevAccessClubsControl_TextInputLength'

    def build_msg(self, dialog, msg, *additional_tokens):
        msg.max_length = 30
        msg.min_length = 1


@Command('td1devaccess.get_club_id', 'clubs.get_club_id', command_type=CommandType.Live, pack=Pack.EP02)
def get_club_id(club_name, _connection=None):
    club_service = _get_club_service(_connection)
    if club_service is None:
        output('Club Service Not Found, likely due to Pack EP02 not installed.', _connection)
        return
    club_name_lc = club_name.lower()
    for club in club_service.clubs:
        if club_name_lc in str(club).lower():
            output('{}: {}'.format(club_name, club.id), _connection)
            return
    output('No existing club with a name including the string {}'.format(club_name), _connection)


@Command('td1devaccess.modify_club_points', command_type=CommandType.Live, pack=Pack.EP02)
def modify_club_points(actor_sim:RequiredTargetParam, _connection=None):
    output = CheatOutput(_connection)
    client = services.client_manager().get_first_client()
    club_service = _get_club_service(_connection)
    target_sim_info = actor_sim.get_target(manager=services.sim_info_manager())
    if target_sim_info is None:
        output('Not a valid SimID.')
        return
    bucks_type = 64

    if club_service is None:
        output('Club Service Not Found, likely due to Pack EP02 not installed.')
        return

    def club_input_callback(dialog):

        if not dialog.accepted:
            output('Dialog Cancelled.')

        club_name = dialog.text_input_responses.get('club_name')
        points_to_modify = int(dialog.text_input_responses.get('input_points'))

        output('{}: Modify {} Bucks'.format(club_name, points_to_modify))

        club_name_lc = club_name.lower()

        for club in club_service.clubs:
            if club_name_lc in str(club).lower():

                output('{}: {}'.format(club_name, club.id))

                old_amount = club.bucks_tracker.get_bucks_amount_for_type(bucks_type)

                output('{}: Initial {} Buck Points'.format(club_name, old_amount))

                set_bucks_value = old_amount + points_to_modify

                output('{}: Test Points {}'.format(club_name, set_bucks_value))

                if set_bucks_value > 0:

                    output('{} Bucks will be left after this operation.'.format(set_bucks_value))

                else:

                    output('{} Bucks will lead to a negative Bucks Value which equates to: {} Bucks'.format(points_to_modify, set_bucks_value))

                    failure_title = lambda **_: LocalizationHelperTuning.get_raw_text("Bucks Modification Failure")
                    failure_text = lambda **_: LocalizationHelperTuning.get_raw_text("Not enough ▮Bucks for a Modification.")

                    notification_failure = UiDialogNotification.TunableFactory().default(
                        client.active_sim,
                        text=failure_text,
                        title=failure_title
                    )
                    notification_failure.show_dialog()

                    return

                result = club.bucks_tracker.try_modify_bucks(bucks_type, set_bucks_value, reason='Added Via Cheat.')

                if set_bucks_value > 0:
                    success_title = lambda **_: LocalizationHelperTuning.get_raw_text("Bucks Addition Success")
                    success_text = lambda **_: LocalizationHelperTuning.get_raw_text("▮" + str(points_to_modify) + " Bucks have been added.")  # _create_localized_string(1956515011)

                    notification_success = UiDialogNotification.TunableFactory().default(
                        client.active_sim,
                        text=success_text,
                        title=success_title
                    )
                    notification_success.show_dialog()
                else:
                    success_title = lambda **_: LocalizationHelperTuning.get_raw_text("Bucks Deduction Success")
                    success_text = lambda **_: LocalizationHelperTuning.get_raw_text("▮" + str(points_to_modify) + " Bucks have been added.")  # _create_localized_string(1956515011)

                    notification_success = UiDialogNotification.TunableFactory().default(
                        client.active_sim,
                        text=success_text,
                        title=success_title
                    )
                    notification_success.show_dialog()

        output('No existing club with a name including the string {}'.format(club_name))


    localized_title = lambda **_: LocalizationHelperTuning.get_raw_text("Modify Club Points")
    localized_text = lambda **_: LocalizationHelperTuning.get_raw_text("Indicate the Club Name and the amount of ▮Club Points that you wish to add or deduct:")
    localized_initial_value = lambda **_: LocalizationHelperTuning.get_raw_text("")

    # This defines our input fields
    input_club_name = UiTextInput(sort_order=0, restricted_characters=None)
    input_club_name.default_text = None
    input_club_name.title = lambda **_: LocalizationHelperTuning.get_raw_text("Club Name")
    input_club_name.max_length = 30
    input_club_name.initial_value = localized_initial_value
    input_club_name.length_restriction = DevAccessClubsControl_TextInputLength()
    input_club_name.check_profanity = False
    input_club_name.height = False

    input_points = UiTextInput(sort_order=1, restricted_characters=None)
    input_points.default_text = None
    input_points.title = lambda **_: LocalizationHelperTuning.get_raw_text("▮Club Points to Add/Deduct (For negative values, use -(Number))")
    input_points.max_length = 30
    input_points.initial_value = localized_initial_value
    input_points.length_restriction = DevAccessClubsControl_TextInputLength()
    input_points.check_profanity = False
    input_points.height = False

    inputs = AttributeDict({'club_name': input_club_name, 'input_points': input_points})

    # Create the actual dialog object...
    dialog = UiDialogTextInputOkCancel.TunableFactory().default(client.active_sim, text=localized_text, title=localized_title, text_inputs=inputs)
    icon = get_resource_key(0, Types.PNG)

    dialog.add_listener(club_input_callback)
    dialog.show_dialog(icon_override=IconInfoData(icon_resource=icon))
    output("Main function done")


@Command('td1devaccess.set_club_points', command_type=CommandType.Live, pack=Pack.EP02)
def set_club_points(actor_sim: RequiredTargetParam, _connection=None):
    output = CheatOutput(_connection)
    client = services.client_manager().get_first_client()
    club_service = _get_club_service(_connection)
    target_sim_info = actor_sim.get_target(manager=services.sim_info_manager())
    if target_sim_info is None:
        output('Not a valid SimID.')
        return
    bucks_type = 64

    if club_service is None:
        output('Club Service Not Found, likely due to Pack EP02 not installed.')
        return

    def club_input_callback(dialog):

        if not dialog.accepted:
            output('Dialog Cancelled.')
            return

        club_name = dialog.text_input_responses.get('club_name')
        points_to_modify = int(dialog.text_input_responses.get('input_points'))

        output('{}: Modify {} Bucks'.format(club_name, points_to_modify))

        club_name_lc = club_name.lower()

        for club in club_service.clubs:
            if club_name_lc in str(club).lower():

                output('{}: {}'.format(club_name, club.id))

                old_amount = club.bucks_tracker.get_bucks_amount_for_type(bucks_type)

                output('{}: Initial {} Buck Points'.format(club_name, old_amount))

                if points_to_modify > old_amount:

                    points_for_test = points_to_modify - old_amount

                else:

                    points_for_test = old_amount - points_to_modify

                output('{}: Test Points {}'.format(club_name, points_for_test))

                if points_for_test > 0:

                    output('{} Bucks will be added/deducted after this operation.'.format(points_for_test))

                else:

                    output('{} Bucks will lead to a negative Bucks Value which equates to: {} Bucks'.format(
                        points_to_modify, points_for_test))

                    failure_title = lambda **_: LocalizationHelperTuning.get_raw_text("Bucks Modification Failure")
                    failure_text = lambda **_: LocalizationHelperTuning.get_raw_text("Not enough ▮Bucks for a Modification.")

                    notification_failure = UiDialogNotification.TunableFactory().default(
                        client.active_sim,
                        text=failure_text,
                        title=failure_title
                    )
                    notification_failure.show_dialog()

                    return

                set_bucks_value = points_to_modify - old_amount

                result = club.bucks_tracker.try_modify_bucks(bucks_type, set_bucks_value, reason='Added Via Cheat.')

                if set_bucks_value > 0:
                    success_title = lambda **_: LocalizationHelperTuning.get_raw_text("Bucks Addition Success")
                    success_text = lambda **_: LocalizationHelperTuning.get_raw_text("▮" + str(set_bucks_value) + " Bucks have been added.")  # _create_localized_string(1956515011)

                    notification_success = UiDialogNotification.TunableFactory().default(
                        client.active_sim,
                        text=success_text,
                        title=success_title
                    )
                    notification_success.show_dialog()
                else:
                    success_title = lambda **_: LocalizationHelperTuning.get_raw_text("Bucks Deduction Success")
                    success_text = lambda **_: LocalizationHelperTuning.get_raw_text("▮" + str(-set_bucks_value) + " Bucks have been added.")  # _create_localized_string(1956515011)

                    notification_success = UiDialogNotification.TunableFactory().default(
                        client.active_sim,
                        text=success_text,
                        title=success_title
                    )
                    notification_success.show_dialog()

        output('No existing club with a name including the string {}'.format(club_name))

    localized_title = lambda **_: LocalizationHelperTuning.get_raw_text("Modify Club Points")
    localized_text = lambda **_: LocalizationHelperTuning.get_raw_text("Indicate the Club Name and the amount of ▮Club Points that you wish to add or deduct:")
    localized_initial_value = lambda **_: LocalizationHelperTuning.get_raw_text("")

    # This defines our input fields
    input_club_name_1 = UiTextInput(sort_order=0, restricted_characters=None)
    input_club_name_1.default_text = None
    input_club_name_1.title = lambda **_: LocalizationHelperTuning.get_raw_text("Club Name")
    input_club_name_1.max_length = 30
    input_club_name_1.initial_value = localized_initial_value
    input_club_name_1.length_restriction = DevAccessClubsControl_TextInputLength()
    input_club_name_1.check_profanity = False
    input_club_name_1.height = False

    input_points = UiTextInput(sort_order=1, restricted_characters=None)
    input_points.default_text = None
    input_points.title = lambda **_: LocalizationHelperTuning.get_raw_text("▮Club Points to Add/Deduct (For negative values, use -(Number))")
    input_points.max_length = 30
    input_points.initial_value = localized_initial_value
    input_points.length_restriction = DevAccessClubsControl_TextInputLength()
    input_points.check_profanity = False
    input_points.height = False

    inputs = AttributeDict({'club_name': input_club_name_1, 'input_points': input_points})

    # Create the actual dialog object...
    dialog = UiDialogTextInputOkCancel.TunableFactory().default(client.active_sim, text=localized_text, title=localized_title, text_inputs=inputs)
    icon = get_resource_key(0, Types.PNG)

    dialog.add_listener(club_input_callback)
    dialog.show_dialog(icon_override=IconInfoData(icon_resource=icon))
    output("Main function done")
