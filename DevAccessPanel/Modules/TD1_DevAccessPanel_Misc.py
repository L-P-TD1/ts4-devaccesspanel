import weakref
import objects
import services
from crafting.crafting_interactions import create_craftable
from distributor.shared_messages import IconInfoData
from objects import system
from objects.system import create_object
from server_commands.argument_helpers import RequiredTargetParam, get_optional_target, OptionalTargetParam
from sims4.collections import AttributeDict
from sims4.commands import Command, CommandType, output, CheatOutput, Output
from sims4 import math, hash_util
from sims4.localization import LocalizationHelperTuning
from sims4.resources import get_resource_key, Types
from sims4.tuning.tunable import HasTunableSingletonFactory, AutoFactoryInit
from ui.ui_dialog_generic import UiDialogTextInputOkCancel
from ui.ui_text_input import UiTextInput
from vfx import PlayEffect

# Importation of MasterApprentice Logger

try:
    from MasterApprenticeLib.TD1_Lib_ApprenticeLogger import ApprenticeLogger
    apprentice_logger = ApprenticeLogger('TD1 DevAccessPanel SimInfo Dumper', main_owner='TwelfthDoctor1')

except ImportError:
    apprentice_logger = False

try:
    from MasterApprenticeLib.TD1_Lib_MasterLogger import MasterLogger
    master_logger = MasterLogger('TD1 DevAccessPanel SimInfo Dumper', main_owner='TwelfthDoctor1')

except ImportError:
    master_logger = False


class DevAccessMiscControl_TextInputLength(HasTunableSingletonFactory, AutoFactoryInit):
    __qualname__ = 'DevAccessMiscControl_TextInputLength'

    def build_msg(self, dialog, msg, *additional_tokens):
        msg.max_length = 30
        msg.min_length = 1


@Command('td1devaccess.print_sim_info', command_type=CommandType.Live)
def print_sim_info(opt_sim:OptionalTargetParam=None, _connection=None):
    output = Output(_connection)
    sim = get_optional_target(opt_sim, _connection)

    if sim is None:
        output("No valid Sim specified.")
        return
    output('============================================================================')
    output(f'Sim Name: {sim} | Sim ID: {sim.id}')


@Command('td1devaccess.dump_sim_info', command_type=CommandType.Live)
def dump_sim_info(opt_sim:OptionalTargetParam=None, _connection=None):
    output = Output(_connection)
    sim = get_optional_target(opt_sim, _connection)

    if sim is None:
        output("No valid Sim specified.")
        return

    if apprentice_logger is not None and apprentice_logger is not False:
        apprentice_logger.info(f'Sim: {sim}\nSim ID: {sim.id}\nSpecies: {sim.species}')

    if master_logger is not None and master_logger is not False:
        master_logger.info(f'Sim: {sim}\nSim ID: {sim.id}')


previous_vfx = ''
previous_target_bone = ''


@Command('td1devaccess.set_vfx')
def set_vfx(actor_sim:OptionalTargetParam=None, _connection=None):
    sim = get_optional_target(actor_sim, _connection)
    client = services.client_manager().get_first_client()
    output = Output(_connection)

    if previous_vfx == '':
        previous_vfx_translate = None
    else:
        previous_vfx_translate = previous_vfx

    if previous_target_bone == '':
        previous_target_bone_translate = None
    else:
        previous_target_bone_translate = previous_target_bone

    def on_response(dialog):
        if not dialog.accepted:
            return

        vfx_effect = dialog.text_input_responses.get("vfx")
        target_bone = dialog.text_input_responses.get("target_bone")

        output(f'VFX: {vfx_effect}| Target Bone: {target_bone}')

        if previous_vfx_translate is not None and previous_target_bone_translate is not None:
            previous_vfx_status = PlayEffect(sim, previous_vfx_translate, hash_util.hash32(previous_target_bone_translate), sim.id, hash_util.hash32(previous_target_bone_translate), play_immediate=True)

            previous_vfx_status.stop(immediate=True)

        current_vfx_status = PlayEffect(sim, vfx_effect, hash_util.hash32(target_bone), sim.id, hash_util.hash32(target_bone), play_immediate=True)

        current_vfx_status.start()

        previous_vfx = vfx_effect
        previous_target_bone = target_bone

    localized_title = lambda **_: LocalizationHelperTuning.get_raw_text("Cheat: Set VFX")
    localized_text = lambda **_: LocalizationHelperTuning.get_raw_text(
        "Specify the VFX (Visual Effect) and Target Bone for the VFX Cheat.\n\n For Target Bones, please see <b>sims.list_target_bones</b>")
    localized_initial_value = lambda **_: LocalizationHelperTuning.get_raw_text("")

    # This defines our input fields
    input_vfx = UiTextInput(sort_order=0, restricted_characters=None)
    input_vfx.default_text = None
    input_vfx.title = lambda **_: LocalizationHelperTuning.get_raw_text("Visual Effect (VFX) Name: ")
    input_vfx.max_length = 30
    input_vfx.initial_value = localized_initial_value
    input_vfx.length_restriction = DevAccessMiscControl_TextInputLength()
    input_vfx.check_profanity = False
    input_vfx.height = False

    input_target_bone = UiTextInput(sort_order=1, restricted_characters=None)
    input_target_bone.default_text = None
    input_target_bone.title = lambda **_: LocalizationHelperTuning.get_raw_text("Target Bone: Input _FX_ for Regular Cheat")
    input_target_bone.max_length = 30
    input_target_bone.initial_value = localized_initial_value
    input_target_bone.length_restriction = DevAccessMiscControl_TextInputLength()
    input_target_bone.check_profanity = False
    input_target_bone.height = False

    inputs = AttributeDict(
        {
            'vfx': input_vfx,
            'target_bone': input_target_bone,
        }
    )

    # Create the actual dialog object...
    dialog = UiDialogTextInputOkCancel.TunableFactory().default(client.active_sim, text=localized_text,
                                                                title=localized_title, text_inputs=inputs)
    icon = get_resource_key(0, Types.PNG)

    dialog.add_listener(on_response)
    dialog.show_dialog(icon_override=IconInfoData(icon_resource=icon))
    output("Main function done")


@Command('td1devaccess.set_as_head', command_type=CommandType.Cheat)
def set_as_head(obj_id:RequiredTargetParam=None, target_bone:str='b__neck__', scale:float=None, forward_rot:float=None, up_rot:float=None, _connection=None):
    sim = get_optional_target(None, _connection)
    if sim is None:
        return
    original_obj = obj_id.get_target()
    if original_obj is None:
        return
    if original_obj.is_sim:
        output('Cannot set a Sim as your head.', _connection)
        return
    obj_definition_id = original_obj.definition.id
    if original_obj.crafting_component is not None:
        obj = create_craftable(original_obj.crafting_component._crafting_process.recipe, sim)
    else:
        obj = objects.system.create_object(obj_definition_id)
    if obj is None:
        return
    if scale is None:
        head_width = 0.75
        default_object_width = head_width/4
        polygon = obj.footprint_polygon
        if len(polygon) > 1:
            polygon2 = list(polygon)[1:]
            polygon2.append(polygon[-1])
            object_width_x = max([abs(x - y).x for (x, y) in zip(polygon2, polygon)])
            object_width_z = max([abs(x - y).z for (x, y) in zip(polygon2, polygon)])
            object_width = min((object_width_x, object_width_z))
        else:
            object_width = default_object_width
        new_scale = head_width/object_width
        obj.scale = new_scale
    else:
        obj.scale = scale
    forward_rot = 4*math.PI/3 if forward_rot is None else forward_rot
    up_rot = 3*math.PI/2 if up_rot is None else up_rot
    forward_orientation = math.Quaternion.from_axis_angle(forward_rot, math.FORWARD_AXIS)
    up_orientation = math.Quaternion.from_axis_angle(up_rot, math.UP_AXIS)
    orientation = math.Quaternion.concatenate(forward_orientation, up_orientation)
    new_transform = math.Transform.IDENTITY()
    new_transform.orientation = orientation
    target_bone_hash = hash_util.hash32(target_bone)
    if sim.current_object_set_as_head is not None and sim.current_object_set_as_head() is not None:
        sim.current_object_set_as_head().destroy(source=sim, cause='Destroying existing object set as head when setting new one.')
    sim.current_object_set_as_head = weakref.ref(obj)
    obj.set_parent(sim, transform=new_transform, joint_name_or_hash=target_bone_hash)


@Command('td1devaccess.set_as_head_specifier', command_type=CommandType.Cheat)
def set_as_head(obj_id:RequiredTargetParam=None, _connection=None):
    sim = get_optional_target(None, _connection)
    output = CheatOutput(_connection)
    # output(f'Object ID: {obj_id}')
    client = services.client_manager().get_first_client()
    if sim is None:
        return
    original_obj = obj_id.get_target()
    # output(f'Original OBJ: {original_obj}')
    if original_obj is None:
        return
    if original_obj.is_sim:
        output('Cannot set a Sim as your head.')
        return
    obj_definition_id = original_obj.definition.id
    # output(f'Object Definition ID: {obj_definition_id}')
    if original_obj.crafting_component is not None:
        obj = create_craftable(original_obj.crafting_component._crafting_process.recipe, sim)
    else:
        obj = create_object(obj_definition_id)
    # output(f'Object: {obj}')
    if obj is None:
        return

    output(f'Object ID: {obj_id} | Original OBJ: {original_obj} | Object Definition ID: {obj_definition_id} | Object: {obj}')

    def on_response(dialog):

        if not dialog.accepted:
            return

        target_bone = dialog.text_input_responses.get("target_bone")
        scale_stage1 = dialog.text_input_responses.get("scale")
        forward_rot_stage1 = dialog.text_input_responses.get("forward_rot")
        up_rot_stage1 = dialog.text_input_responses.get("up_rot")

        output(f'Target Bone: {target_bone} | Scale: {scale_stage1} | Forward Rotation: {forward_rot_stage1} | Upwards Rotation: {up_rot_stage1}')

        try:
            scale = float(scale_stage1)

        except ValueError:
            scale = None

        try:
            forward_rot = float(forward_rot_stage1)

        except ValueError:
            forward_rot = None

        try:
            up_rot = float(up_rot_stage1)

        except ValueError:
            up_rot = None

        output(f'Target Bone: {target_bone} | Scale: {scale} | Forward Rotation: {forward_rot} | Upwards Rotation: {up_rot}')

        if scale is None:
            head_width = 0.75
            default_object_width = head_width/4
            polygon = obj.footprint_polygon
            if len(polygon) > 1:
                polygon2 = list(polygon)[1:]
                polygon2.append(polygon[-1])
                object_width_x = max([abs(x - y).x for (x, y) in zip(polygon2, polygon)])
                object_width_z = max([abs(x - y).z for (x, y) in zip(polygon2, polygon)])
                object_width = min((object_width_x, object_width_z))
            else:
                object_width = default_object_width
            new_scale = head_width/object_width
            obj.scale = new_scale
        else:
            obj.scale = scale

        forward_rot = 4*math.PI/3 if forward_rot is None else forward_rot
        up_rot = 3*math.PI/2 if up_rot is None else up_rot
        forward_orientation = math.Quaternion.from_axis_angle(forward_rot, math.FORWARD_AXIS)
        up_orientation = math.Quaternion.from_axis_angle(up_rot, math.UP_AXIS)
        orientation = math.Quaternion.concatenate(forward_orientation, up_orientation)
        new_transform = math.Transform.IDENTITY()
        new_transform.orientation = orientation
        target_bone_hash = hash_util.hash32(target_bone)
        if sim.current_object_set_as_head is not None and sim.current_object_set_as_head() is not None:
            sim.current_object_set_as_head().destroy(source=sim, cause='Destroying existing object set as head when setting new one.')
        sim.current_object_set_as_head = weakref.ref(obj)
        obj.set_parent(sim, transform=new_transform, joint_name_or_hash=target_bone_hash)

    localized_title = lambda **_: LocalizationHelperTuning.get_raw_text("Cheat: Set As Head")
    localized_text = lambda **_: LocalizationHelperTuning.get_raw_text(
        "Specify the Target Bone, Scale, Forward Rotation and Upwards Rotation for the Set As Head Cheat.\n\n For Target Bones, please see <b>sims.list_target_bones</b>")
    localized_initial_value = lambda **_: LocalizationHelperTuning.get_raw_text("")

    # This defines our input fields
    input_target_bone = UiTextInput(sort_order=0, restricted_characters=None)
    input_target_bone.default_text = None
    input_target_bone.title = lambda **_: LocalizationHelperTuning.get_raw_text("Target Bone: Input b__neck__ for Regular Cheat")
    input_target_bone.max_length = 30
    input_target_bone.initial_value = localized_initial_value
    input_target_bone.length_restriction = DevAccessMiscControl_TextInputLength()
    input_target_bone.check_profanity = False
    input_target_bone.height = False

    input_scale = UiTextInput(sort_order=1, restricted_characters=None)
    input_scale.default_text = None
    input_scale.title = lambda **_: LocalizationHelperTuning.get_raw_text("Scale: Input None if unused")
    input_scale.max_length = 30
    input_scale.initial_value = localized_initial_value
    input_scale.length_restriction = DevAccessMiscControl_TextInputLength()
    input_scale.check_profanity = False
    input_scale.height = False

    input_forward_rot = UiTextInput(sort_order=2, restricted_characters=None)
    input_forward_rot.default_text = None
    input_forward_rot.title = lambda **_: LocalizationHelperTuning.get_raw_text("Forward Rotation: Input None if unused")
    input_forward_rot.max_length = 30
    input_forward_rot.initial_value = localized_initial_value
    input_forward_rot.length_restriction = DevAccessMiscControl_TextInputLength()
    input_forward_rot.check_profanity = False
    input_forward_rot.height = False

    input_up_rot = UiTextInput(sort_order=3, restricted_characters=None)
    input_up_rot.default_text = None
    input_up_rot.title = lambda **_: LocalizationHelperTuning.get_raw_text("Upwards Rotation: Input None if unused")
    input_up_rot.max_length = 30
    input_up_rot.initial_value = localized_initial_value
    input_up_rot.length_restriction = DevAccessMiscControl_TextInputLength()
    input_up_rot.check_profanity = False
    input_up_rot.height = False

    inputs = AttributeDict(
        {
            'target_bone': input_target_bone,
            'scale': input_scale,
            'forward_rot': input_forward_rot,
            'up_rot': input_up_rot
        }
    )

    # Create the actual dialog object...
    dialog = UiDialogTextInputOkCancel.TunableFactory().default(client.active_sim, text=localized_text,
                                                                title=localized_title, text_inputs=inputs)
    icon = get_resource_key(0, Types.PNG)

    dialog.add_listener(on_response)
    dialog.show_dialog(icon_override=IconInfoData(icon_resource=icon))
    output("Main function done")


@Command('sims.list_target_bones', command_type=CommandType.Cheat)
def list_target_bones(_connection=None):
    output = Output(_connection)
    output("Sim Target Bones\n")
    output("b__ROOT__ | The Base Target Bone")
    output("b__ROOT_bind__ | ~")
    output("b__Spine0__ | ~")
    output("b__Pelvis__ | ~")
    output("b__L_Prop__ | Left Handed Prop Target Bone")
    output("b__R_Prop__ | Right Handed Prop Target Bone")
    output("b__Spine1__ | ~")
    output("b__Spine2__ | ~")
    output("b__Neck__ | Neck Target Bone")
    output("b__Head__ | Head Target Bone")
    output("b__CAS_Glasses__ | Glasses Target Bone")
    output("b__L_Cheek__ | Left Cheek Target Bone")
    output("b__L_Squint__ | ~")
    output("b__CAS_L_EyeArea__ | ~")
    output("b__L_InBrow__ | ~")
    output("b__L_MidBrow__ | ~")
    output("b__L_OutBrow__ | ~")
    output("b__CAS_L_EyeScale__ | ~")
    output("b__L_LoLid__ | ~")
    output("b__L_UpLid__| ~")
    output("b__L_Eye__ | Left Eye Target Bone")
    output("b__R_Cheek__ | Right Cheek Target Bone")
    output("b__R_Squint__ | ~")
    output("b__CAS_R_EyeArea__ | ~")
    output("b__R_InBrow__ | ~")
    output("b__R_MidBrow__ | ~")
    output("b__R_OutBrow__ | ~")
    output("b__CAS_R_EyeScale__ | ~")
    output("b__R_LoLid__ | ~")
    output("b__R_UpLid__| ~")
    output("b__R_Eye__ | Right Eye Target Bone")
    output("b__CAS_NoseArea__ | ~")
    output("b__CAS_NoseTip__ | ~")
    output("b__CAS_NoseBridge__ | ~")
    output("b__CAS_L_Nostril__ | ~")
    output("b__CAS_R_Nostril__ | ~")
    output("b__CAS_UpperMouthArea__ | ~")
    output("b__L_Mouth__ | ~")
    output("b__R_Mouth__ | ~")
    output("b__L_UpLip__ | ~")
    output("b__R_UpLip__ | ~")
    output("b__UpLip__ | ~")
    output("b__mouth_slot__ | ~")
    output("b__jaw__ | ~")
    output("b__CAS_LowerMouthArea__ | ~")
    output("b__L_LoLip__ | ~")
    output("b__R_LoLip__ | ~")
    output("b__CAS_JawComp__ | ~")
    output("b__CAS_Chin__ | ~")
    output("b__L_Earring_slot | ~")
    output("b__R_Earring_slot | ~")
    output("b__Neck_slot | ~")
    output("b__backNeck_slot | ~")
    output("b__L_chestTarget_slot | ~")
    output("b__L_shoulderbladeTarget_slot | ~")
    output("b__R_chestTarget_slot | ~")
    output("b__R_shoulderbladeTarget_slot | ~")
    output("b__R_Clavicle__ | ~")
    output("b__R_ShoulderTarget_slot | ~")
    output("b__R_UpperArm__ | ~")
    output("b__R_Forearm__ | ~")
    output("b__R_ForearmTwist__ | ~")
    output("b__R_Bracelet_slot | ~")
    output("b__R_Hand__ | ~")
    output("b__R_Stigmata | ~")
    output("b__R_Thumb0__ | ~")
    output("b__R_Thumb1__ | ~")
    output("b__R_Thumb2__ | ~")
    output("b__R_Pinky0__ | ~")
    output("b__R_Pinky1__ | ~")
    output("b__R_Pinky2__ | ~")
    output("b__R_Ring0__ | ~")
    output("b__R_Ring1__ | ~")
    output("b__R_Ring2__ | ~")
    output("b__R_Ring_slot | ~")
    output("b__R_Mid0__ | ~")
    output("b__R_Mid1__ | ~")
    output("b__R_Mid2__ | ~")
    output("b__R_Index0__ | ~")
    output("b__R_Index1__ | ~")
    output("b__R_Index2__ | ~")
    output("b__R_ForearTarget_slot | ~")
    output("b__R_Elbow__ | ~")
    output("b__R_ShoulderTwist__ | ~")
    output("b__R_outShortSleeve_slot | ~")
    output("b__L_Clavicle__ | ~")
    output("b__L_ShoulderTarget_slot | ~")
    output("b__L_UpperArm__ | ~")
    output("b__L_Forearm__ | ~")
    output("b__L_ForearmTwist__ | ~")
    output("b__L_Bracelet_slot | ~")
    output("b__L_Hand__ | ~")
    output("b__L_Stigmata | ~")
    output("b__L_Thumb0__ | ~")
    output("b__L_Thumb1__ | ~")
    output("b__L_Thumb2__ | ~")
    output("b__L_Pinky0__ | ~")
    output("b__L_Pinky1__ | ~")
    output("b__L_Pinky2__ | ~")
    output("b__L_Ring0__ | ~")
    output("b__L_Ring1__ | ~")
    output("b__L_Ring2__ | ~")
    output("b__L_Ring_slot | ~")
    output("b__L_Mid0__ | ~")
    output("b__L_Mid1__ | ~")
    output("b__L_Mid2__ | ~")
    output("b__L_Index0__ | ~")
    output("b__L_Index1__ | ~")
    output("b__L_Index2__ | ~")
    output("b__L_ForearTarget_slot | ~")
    output("b__L_Elbow__ | ~")
    output("b__L_ShoulderTwist__ | ~")
    output("b__L_outShortSleeve_slot | ~")
    output("b__R_ArmExportPole__ | ~")
    output("b__L_ArmExportPole__ | ~")
    output("b__R_HandDangle_slot | ~")
    output("b__L_HandDangle_slot | ~")
    output("b__CAS_L_Breast__ | ~")
    output("b__L_breastTarget_slot | ~")
    output("b__L_frontTorsoTarget_slot | ~")
    output("b__L_sideBackTorsoTarget_slot | ~")
    output("b__CAS_R_Breast__ | ~")
    output("b__R_breastTarget_slot | ~")
    output("b__R_frontTorsoTarget_slot | ~")
    output("b__R_sideBackTorsoTarget_slot | ~")
    output("b__R_BackTarget_slot | ~")
    output("b__L_BackTarget_slot | ~")
    output("b__Carry__ | ~")
    output("b__R_carry_slot | ~")
    output("b__L_carry_slot | ~")
    output("b__L_backBellyTarget_slot | ~")
    output("b__L_BellyTarget_slot | ~")
    output("b__L_frontBellyTarget_slot | ~")
    output("b__R_backBellyTarget_slot | ~")
    output("b__R_BellyTarget_slot | ~")
    output("b__R_frontBellyTarget_slot | ~")
    output("b__L_lowBackTarget_slot | ~")
    output("b__R_lowBackTarget_slot | ~")
    output("b__L_Thigh__ | ~")
    output("b__L_Calf__ | ~")
    output("b__L_Foot__ | ~")
    output("b__L_Toe__ | ~")
    output("b__L_frontCalfTarget_slot | ~")
    output("b__L_inCalfTarget_slot | ~")
    output("b__L_KneeTarget_slot | ~")
    output("b__L_Skirt__ | ~")
    output("b__L_ThighTwist__ | ~")
    output("b__L_LegExportPole__ | ~")
    output("b__L_outThighTarget_slot | ~")
    output("b__L_ThighFrontTarget_slot | ~")
    output("b__R_Thigh__ | ~")
    output("b__R_Calf__ | ~")
    output("b__R_Foot__ | ~")
    output("b__R_Toe__ | ~")
    output("b__R_frontCalfTarget_slot | ~")
    output("b__R_inCalfTarget_slot | ~")
    output("b__R_KneeTarget_slot | ~")
    output("b__R_Skirt__ | ~")
    output("b__R_ThighTwist__ | ~")
    output("b__R_LegExportPole__ | ~")
    output("b__R_outThighTarget_slot | ~")
    output("b__R_ThighFrontTarget_slot | ~")
