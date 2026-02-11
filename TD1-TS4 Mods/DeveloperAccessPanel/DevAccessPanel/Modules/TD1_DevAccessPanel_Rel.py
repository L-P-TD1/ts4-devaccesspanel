import services
from distributor.shared_messages import IconInfoData
from server_commands.argument_helpers import RequiredTargetParam
from sims4.collections import AttributeDict
from sims4.commands import Command, Output, CommandType
from sims4.localization import LocalizationHelperTuning
from sims4.resources import get_resource_key, Types
from sims4.tuning.tunable import HasTunableSingletonFactory, AutoFactoryInit
from ui.ui_dialog_generic import UiDialogTextInputOkCancel
from ui.ui_dialog_notification import UiDialogNotification
from ui.ui_text_input import UiTextInput


class DevAccessRelControl_TextInputLength(HasTunableSingletonFactory, AutoFactoryInit):
    __qualname__ = 'DevAccessEcoControl_TextInputLength'

    def build_msg(self, dialog, msg, *additional_tokens):
        msg.max_length = 30
        msg.min_length = 1


@Command('td1devaccess.set_object_relationship', command_type=CommandType.Live)
def set_object_relationship(sim:RequiredTargetParam=None, obj_inst_id:RequiredTargetParam=None, obj_def_id: int = None, _connection=None):
    client = services.client_manager().get_first_client()
    sim_id = sim.get_target(manager=services.sim_info_manager())
    obj = obj_inst_id.get_target(manager=services.object_manager())
    output = Output(_connection)
    if obj is None:
        obj = services.inventory_manager().get(obj_inst_id)
    if obj_def_id is None:
        obj_def_id = obj.definition.id
    obj_tag_set = services.relationship_service().get_mapped_tag_set_of_id(obj_def_id)

    title = lambda **_: LocalizationHelperTuning.get_raw_text("Cheat Object Relationship")
    text = lambda **_: LocalizationHelperTuning.get_raw_text("Indicate the Relationship Value between the Sim and the Object (For negative values, use -(Number)):")
    init_value = lambda **_: LocalizationHelperTuning.get_raw_text("")

    def get_input_callback(dialog):
        if not dialog.accepted:
            return

        value = float(dialog.get_input_responses.get('input_rel'))

        notif_title = lambda **_: LocalizationHelperTuning.get_raw_text("Relationship Change Success")
        notif_text = lambda **_: LocalizationHelperTuning.get_raw_text(f"The Relationship between the Sim and the object is now {value}.")

        notification = UiDialogNotification.TunableFactory(
            client.active_sim,
            title=notif_title,
            text=notif_text
        )

        if obj is not None and obj_tag_set is not None:
            obj_relationship = services.relationship_service()._find_object_relationship(
                sim_id,
                obj_tag_set,
                obj_def_id,
                create=True
            )

            if obj_relationship is None:
                output('Object relationship creation failed for Sim {} on object {}'.format(sim_id, obj_def_id))
                return False
            stat_type = services.relationship_service().get_mapped_track_of_tag_set(obj_tag_set)
            obj_relationship.relationship_track_tracker.set_value(stat_type, value)
            notification.show_dialog()

        else:
            if obj is None:
                output('Could not find target object {} relationship with Sim {}.'.format(obj_inst_id, sim_id))
                return False
            obj_rel = obj.objectrelationship_component
            if obj_rel is None:
                output('Object relationship for Sim {} on object {} is not valid.'.format(sim_id, obj_inst_id))
                return False
            obj_rel.modify_relationship(sim_id, value, set_value=True)
            notification.show_dialog()

    input_rel_value = UiTextInput(
        sort_order=0,
        restricted_characters="0-9.",
        default_text=None,
        max_length=30,
        initial_value=init_value,
        title=None,
        length_restriction=DevAccessRelControl_TextInputLength,
        check_profanity=False,
        height=False
    )

    inputs = AttributeDict(
        {
            'input_rel': input_rel_value
        }
    )

    dialog = UiDialogTextInputOkCancel.TunableFactory().default(
        client.active_sim,
        text=text,
        title=title,
        text_inputs=inputs
    )

    icon = get_resource_key(0, Types.PNG)
    dialog.add_listener(get_input_callback)
    dialog.show_dialog(
        icon_override=IconInfoData(
            icon_resource=icon
        )
    )
