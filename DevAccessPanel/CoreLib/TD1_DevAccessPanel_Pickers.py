"""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
TwelfthDoctor1's Developer/Debug Access Panel

> PickerInteractions Tuning

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
from bucks.bucks_enums import BucksType
from bucks.bucks_utils import BucksUtils
from interactions import ParticipantTypeSim, ParticipantTypeSingleSim
from interactions.base.picker_interaction import PickerSuperInteraction
from interactions.utils.tunable import TunableContinuation
from protocolbuffers.Localization_pb2 import LocalizedString
from sims4.localization import LocalizationHelperTuning, TunableLocalizedStringFactory
from sims4.resources import Types
from sims4.tuning.tunable import TunableReference, TunableList, OptionalTunable, Tunable, TunableEnumEntry
from sims4.tuning.tunable_base import GroupNames
from sims4.utils import flexmethod
from traits.trait_type import TraitType
from tunable_utils.tunable_white_black_list import TunableWhiteBlackList
from ui.ui_dialog_generic import UiDialogTextInputOkCancel
from ui.ui_dialog_picker import ObjectPickerRow
import services

# Importation of Master Logger

try:
    from MasterApprenticeLib.TD1_Lib_MasterLogger import MasterLogger

    master_logger = MasterLogger('TD1 Menu Picker - Converted', main_owner='TwelfthDoctor1')

except ImportError:
    master_logger = False

TEXT_INPUT_STAT_VALUE = 'stat_value'


class TD1CheatSetStatSuperInteraction(PickerSuperInteraction):
    """
    Similar to the CheatSetStat SI but should be able to list all stats on the Object, regardless of name.
    """
    INSTANCE_TUNABLES = {
        'stat_value_dialog': UiDialogTextInputOkCancel.TunableFactory(
            description="The dialog that is displayed (and asks for the user to enter a value to set for the statistic)."
                        "the selected stat's name is passed as a token as well as the stat's value is passed as an "
                        "input override.",
            text_inputs=(
                TEXT_INPUT_STAT_VALUE,
            )
        ),
        'stat_value_text': TunableLocalizedStringFactory(
            description='the string that will show the current value in the picker and within the input override.'
                        'Should include {0.Number}.',
            default=1989018490
        ),
        'stat_list': OptionalTunable(
            tunable=TunableList(
                description='List of stats we want to allow to be changed by this interaction.'
                            'If nothing is set, it will just show all the stats on the object.',
                tunable=TunableReference(
                    manager=(services.get_instance_manager(Types.STATISTIC)),
                    pack_safe=True
                )
            )
        ),
        'return_menu': TunableContinuation(
            description="The Menu UI to return to if no option is selected.",
        )
    }

    def _get_object_stats_gen(self, target):
        if target.statistic_tracker is not None:
            yield from target.statistic_tracker
        if target.commodity_tracker is not None:
            yield from target.commodity_tracker
        if False:
            yield None

    def _get_displayable_stat_name(self, stat):
        if self.stat_list is None or (stat.stat_type in self.stat_list):
            return self._get_stat_name(self, stat.stat_type)

    @classmethod
    def has_valid_choice(cls, target, context, **kwargs):
        for stat in cls._get_object_stats_gen(cls, target):
            if cls._get_displayable_stat_name(cls, stat) is not None:
                return True

        return False

    def _run_interaction_gen(self, timeline):
        self._show_picker_dialog(self.sim)
        return True
        if False:
            yield None

    @flexmethod
    def picker_rows_gen(cls, inst, target, context, **kwargs):
        inst_or_cls = inst if inst is not None else cls
        for stat in inst_or_cls._get_object_stats_gen(target):
            stat_name = cls._get_displayable_stat_name(cls, stat)
            if stat_name is not None:
                stat_tracker = target.get_tracker(stat)
                stat_value = inst_or_cls.stat_value_text(stat_tracker.get_value(stat.stat_type))
                stat_icon = inst_or_cls._get_stat_icon(stat.stat_type)
                yield ObjectPickerRow(name=stat_name, row_description=stat_value, tag=(stat.stat_type), icon=stat_icon)

    def _get_stat_name(self, stat):
        """
        Get the Stat Name of a tuned statistic. If statistic has no name, use raw name.
        :param stat:
        :return:
        """
        stat_name = getattr(stat, 'stat_name', None)
        if stat_name:
            if stat.stat_name.hash is not 0:
                return stat.stat_name
            else:
                return LocalizationHelperTuning.get_raw_text(stat.__name__)
        else:
            return LocalizationHelperTuning.get_raw_text(stat.__name__)

    def _get_stat_icon(self, stat):
        if hasattr(stat, 'icon'):
            return stat.icon
        states = getattr(stat, 'states', ())
        if states:
            return stat.states[0].icon

    def on_choice_selected(self, choice_tag, **kwargs):
        if choice_tag is None:
            return
        statistic = choice_tag
        target = self.target

        def on_response(value_dialog):
            if not value_dialog.accepted:
                return
            new_value = value_dialog.text_input_responses.get(TEXT_INPUT_STAT_VALUE)
            try:
                new_value = int(new_value)
            except:
                return
            else:
                tracker = target.get_tracker(statistic)
                tracker.set_value(statistic, new_value)

            if self.return_menu is not None:
                self.push_tunable_continuation(self.return_menu)

        stat_name = self._get_stat_name(statistic)
        stat_tracker = target.get_tracker(statistic)
        stat_value = self.stat_value_text(stat_tracker.get_value(statistic))
        text_input_overrides = {}
        text_input_overrides[TEXT_INPUT_STAT_VALUE] = lambda *_, **__: stat_value
        tokens = (stat_name, statistic.min_value, statistic.max_value)
        dialog = self.stat_value_dialog(target, self.get_resolver())
        dialog.show_dialog(on_response=on_response, text_input_overrides=text_input_overrides, additional_tokens=tokens)


class TD1TraitPickerSuperInteraction(PickerSuperInteraction):
    """
    Similar to the TraitPicker SI but should be able to list all traits.
    """
    INSTANCE_TUNABLES = {
        'is_add': Tunable(
            description='If this interaction is trying to add a trait to the sim or to remove a trait from the sim.',
            tunable_type=bool,
            default=True,
            tuning_group=GroupNames.PICKERTUNING
        ),
        'already_equipped_tooltip': OptionalTunable(
            description='If tuned, we show this tooltip if row is disabled when trait is already equipped.',
            tunable=TunableLocalizedStringFactory(
                description='Tooltip to display.'
            ),
            tuning_group=GroupNames.PICKERTUNING
        ),
        'filter_by_types': OptionalTunable(
            description='If specified, limits the traits that appear in this picker to specific types of traits.'
                        'If disabled, all traits are available.',
            tunable=TunableWhiteBlackList(
                tunable=TunableEnumEntry(
                    default=(TraitType.PERSONALITY),
                    tunable_type=TraitType
                )
            ),
            tuning_group=GroupNames.PICKERTUNING
        ),
        'continuation': OptionalTunable(
            description='If enabled then a continuation will be pushed after the picker selection has been made.',
            tunable=TunableContinuation(
                description='If specified, a continuation to push when a picker selection has been made.'),
            tuning_group=GroupNames.PICKERTUNING
        ),
        'picker_target': TunableEnumEntry(
            tunable_type=ParticipantTypeSim,
            default=ParticipantTypeSim.TargetSim,
            tuning_group=GroupNames.PICKERTUNING
        ),
        'return_menu': TunableContinuation(
            description="The Menu UI to return to if no option is selected.",
        )
    }

    def _run_interaction_gen(self, timeline):
        trait_target = self.get_participant(self.picker_target)
        self._show_picker_dialog(trait_target, target_sim=trait_target)
        return True
        if False:
            yield None

    @classmethod
    def _match_trait_type(cls, trait):
        if cls.filter_by_types is None:
            return True
        return cls.filter_by_types.test_item(trait.trait_type)

    @classmethod
    def _trait_selection_gen(cls, target):
        trait_manager = services.get_instance_manager(Types.TRAIT)
        trait_tracker = target.sim_info.trait_tracker
        if cls.is_add:
            for trait in trait_manager.types.values():
                if not cls._match_trait_type(trait):
                    continue
                if trait.sim_info_fixup_actions:
                    continue
                if trait_tracker.can_add_trait(trait):
                    yield trait

        else:
            for trait in trait_tracker.equipped_traits:
                if not cls._match_trait_type(trait):
                    continue
                yield trait

    @flexmethod
    def picker_rows_gen(cls, inst, target, context, **kwargs):
        inst_or_cls = inst if inst is not None else cls
        trait_target = (inst_or_cls.get_participant)(cls.picker_target, target=target, context=context, **kwargs)
        trait_tracker = trait_target.sim_info.trait_tracker
        for trait in cls._trait_selection_gen(trait_target):
            if trait.display_name:
                display_name = trait.display_name(trait_target)
            else:
                display_name = LocalizationHelperTuning.get_raw_text(str(trait.__name__))
            is_enabled = True
            row_tooltip = None
            if cls.is_add:
                is_enabled = not trait_tracker.has_trait(trait)
                row_tooltip = None if (is_enabled or cls.already_equipped_tooltip is None) else (
                    lambda *_: cls.already_equipped_tooltip(target))
            row = ObjectPickerRow(name=display_name, row_description=(trait.trait_description(trait_target)),
                                  icon=(trait.icon),
                                  tag=trait,
                                  is_enable=is_enabled,
                                  row_tooltip=row_tooltip)
            yield row

    def on_choice_selected(self, choice_tag, **kwargs):
        trait = choice_tag
        if trait is not None:
            if self.is_add:
                trait_target = self.get_participant(self.picker_target)
                trait_target.sim_info.add_trait(trait)
            else:
                trait_target = self.get_participant(self.picker_target)
                trait_target.sim_info.remove_trait(trait)
            if self.continuation is not None:
                return self.push_tunable_continuation(self.continuation)

        return self.push_tunable_continuation(self.return_menu)


class TD1BucksPerkPickerSuperInteraction(PickerSuperInteraction):
    """
    Similar to BucksPerkPicker SI but should be able to display all perks, show perk cost, etc.
    """
    INSTANCE_TUNABLES = {
        'is_add': Tunable(
            description='If this interaction is trying to add a bucks perk to the sim or to remove a bucks perk from '
                        'the sim.',
            tunable_type=bool,
            default=True,
            tuning_group=GroupNames.PICKERTUNING
        ),
        'bucks_type': TunableEnumEntry(
            description='The type of Bucks required to unlock/lock this perk.',
            tunable_type=BucksType,
            default=BucksType.INVALID,
            pack_safe=True,
            invalid_enums=(
                BucksType.INVALID,
            ),
            tuning_group=GroupNames.PICKERTUNING
        ),
        'continuations': TunableList(
            description='List of continuations to push if a buff is actually selected.',
            tunable=TunableContinuation(),
            tuning_group=GroupNames.PICKERTUNING
        ),
        'subject': TunableEnumEntry(
            description='From whom the BucksPerks should be added/removed.',
            tunable_type=ParticipantTypeSingleSim,
            default=ParticipantTypeSingleSim.TargetSim,
            tuning_group=GroupNames.PICKERTUNING
        ),
        'return_menu': TunableContinuation(
            description="The Menu UI to return to if no option is selected.",
        )
    }

    def _run_interaction_gen(self, timeline):
        participant = self.get_participant(self.subject)
        self._show_picker_dialog(participant, target_sim=participant)
        return True
        if False:
            yield None

    @classmethod
    def _bucks_perk_selection_gen(cls, participant):
        bucks_perk_tracker = BucksUtils.get_tracker_for_bucks_type((cls.bucks_type), (participant.id), add_if_none=True)
        if True:
            for perk in bucks_perk_tracker.all_perks_of_type_gen(cls.bucks_type):
                yield perk

        else:
            # Old Code of Picker - Set If statement False to use
            get_unlocked = not cls.is_add
            for perk in bucks_perk_tracker.all_perks_of_type_with_lock_state_gen(cls.bucks_type, get_unlocked):
                yield perk

    @classmethod
    def _generate_title_with_cost(cls, perk, title):
        perk_cost = LocalizationHelperTuning.get_raw_text(f"▯{perk.unlock_cost}")
        return LocalizationHelperTuning.NAME_VALUE_PARENTHESIS_PAIR_STRUCTURE(title, perk_cost)

    @classmethod
    def _generate_description_with_cost(cls, perk, text, participant):
        bucks_perk_tracker = BucksUtils.get_tracker_for_bucks_type((cls.bucks_type), (participant.id),
                                                                   add_if_none=True)
        bucks_value = bucks_perk_tracker.get_bucks_amount_for_type(cls.bucks_type)

        perk_cost = LocalizationHelperTuning.get_raw_text(f"Cost: ▯{perk.unlock_cost} | At Disposal: ▯{bucks_value}")
        return LocalizationHelperTuning.NEW_LINE_LIST_STRUCTURE(perk_cost, text)

    @classmethod
    def _get_perk_tooltip(cls, perk, participant):
        bucks_perk_tracker = BucksUtils.get_tracker_for_bucks_type((cls.bucks_type), (participant.id),
                                                                   add_if_none=True)
        if perk.perk_description(participant):
            return perk.perk_description(participant)
        else:
            return bucks_perk_tracker.get_disabled_tooltip_for_perk(perk)

    @classmethod
    def _check_buck_unlocked(cls, perk, participant):
        bucks_perk_tracker = BucksUtils.get_tracker_for_bucks_type((cls.bucks_type), (participant.id),
                                                                   add_if_none=True)

        if bucks_perk_tracker.is_perk_unlocked(perk) is not cls.is_add:
            return True
        else:
            return False

    @flexmethod
    def picker_rows_gen(cls, inst, target, context, **kwargs):
        inst_or_cls = inst if inst is not None else cls
        participant = inst_or_cls.get_participant((inst_or_cls.subject), sim=(context.sim), target=target)
        bucks_perk_tracker = BucksUtils.get_tracker_for_bucks_type((cls.bucks_type), (participant.id), add_if_none=True)
        bucks_value = bucks_perk_tracker.get_bucks_amount_for_type(cls.bucks_type)

        for perk in cls._bucks_perk_selection_gen(participant):
            if perk.display_name:
                display_name = perk.display_name(participant)
            else:
                display_name = LocalizationHelperTuning.get_raw_text(perk.__name__)

            perk_cost = LocalizationHelperTuning.get_raw_text(f"▯{str(perk.unlock_cost)}")
            desc_perk_cost = LocalizationHelperTuning.get_raw_text(
                f"Cost: ▯{str(perk.unlock_cost)} | At Disposal: ▯{str(bucks_value)}"
            )

            row_title = LocalizationHelperTuning.NAME_VALUE_PARENTHESIS_PAIR_STRUCTURE(display_name, perk_cost)
            row_text = LocalizationHelperTuning.NEW_LINE_LIST_STRUCTURE(desc_perk_cost, perk.perk_description(participant))  # cls._generate_description_with_cost(perk, perk.perk_description(participant), participant)
            #row_tooltip = # cls._get_perk_tooltip(perk, participant)

            if cls._check_buck_unlocked(perk, participant):
                row_tooltip = perk.perk_description(participant)
            else:
                row_tooltip = bucks_perk_tracker.get_disabled_tooltip_for_perk(perk)

            localized_title = TunableLocalizedStringFactory().default(row_title)
            localized_text = TunableLocalizedStringFactory().default(row_text)
            localized_tooltip = TunableLocalizedStringFactory().default(row_tooltip)

            if master_logger is not None and master_logger is not False:
                master_logger.debug(
                    f"ROW COMPILING DEBUG | {perk.__name__}\n\n"
                    f"Title: {row_title} | LocalizedString: {isinstance(row_title, LocalizedString)} | "
                    f"{callable(row_title)}, {callable(LocalizedString)}, {callable(localized_title)} | {localized_title}\n"
                    f"Description: {row_text} | LocalizedString: {isinstance(row_text, LocalizedString)} | "
                    f"{callable(row_text)}, {callable(LocalizedString)}, {callable(localized_text)} | {localized_text}\n"
                    f"Tooltip: {row_tooltip} | LocalizedString: {isinstance(row_tooltip, LocalizedString)} | "
                    f"{callable(row_tooltip)}, {callable(LocalizedString)}, {callable(localized_tooltip)} | {localized_tooltip}\n"
                    f"Icon: {perk.icon.key}\n"
                    f"Visible: {cls._check_buck_unlocked(perk, participant)}\n"
                )

            row = ObjectPickerRow(
                name=localized_title,
                row_description=localized_text,
                icon=perk.icon.key,
                row_tooltip=localized_tooltip,
                is_enable=cls._check_buck_unlocked(perk, participant),
                tag=perk
            )
            yield row

    def on_choice_selected(self, choice_tag, **kwargs):
        perk = choice_tag
        if perk is None:
            return
        else:
            participant = self.get_participant(self.subject)
            bucks_perk_tracker = BucksUtils.get_tracker_for_bucks_type(self.bucks_type, participant.id)
            if self.is_add:
                bucks_perk_tracker.pay_for_and_unlock_perk(perk)
            else:
                bucks_perk_tracker.lock_perk(perk, True)
        for continuation in self.continuations:
            self.push_tunable_continuation(continuation)
