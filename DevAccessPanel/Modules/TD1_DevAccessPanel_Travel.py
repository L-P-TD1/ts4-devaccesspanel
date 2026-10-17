"""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
TwelfthDoctor1's Developer/Debug Access Panel

> Travel Module

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
from event_testing.resolver import SingleSimResolver
from event_testing.results import TestResult
from interactions.base.super_interaction import SuperInteraction
from server_commands.argument_helpers import OptionalTargetParam, get_optional_target, get_tunable_instance
from sims.self_interactions import TravelParticipantZone, TravelParticipantHomeZone, TravelObjectHouseholdOwnerHomeZone, \
    TravelCareerCustomerLot, TravelSpecificLot
from sims4.commands import Command, CommandType, Output
from sims4.resources import get_resource_key, Types
from sims4.tuning.tunable import HasTunableSingletonFactory, AutoFactoryInit, Tunable, TunableVariant, \
    TunableLotDescription
from ui.ui_dialog import UiDialogOkCancel
from ui.ui_dialog_generic import UiDialogTextInputOkCancel
from world import get_lot_id_from_instance_id, region
from world.travel_service import travel_sim_to_zone
from sims4.log import Logger
from world.lot import LotTuningMaps

# Importation of MasterApprentice Logger

try:
    from MasterApprenticeLib.TD1_Lib_ApprenticeLogger import ApprenticeLogger
    apprentice_logger = ApprenticeLogger('TD1 DevAccessPanel TravelInteractions', main_owner='TwelfthDoctor1')

except ImportError:
    apprentice_logger = False

try:
    from MasterApprenticeLib.TD1_Lib_MasterLogger import MasterLogger
    master_logger = MasterLogger('TD1 DevAccessPanel TravelInteractions | TravelCheats', main_owner='TwelfthDoctor1')

except ImportError:
    master_logger = False

logger = Logger('TD1 DevAccessPanel TravelInteractions | TravelCheats', default_owner='TwelfthDoctor1')

LOT_TRAVEL_TEXT_INPUT = 'lot_input'
LOT_TRAVEL_ZONE_ID = 0


class DevAccessTravelControl_TextInputLength(HasTunableSingletonFactory, AutoFactoryInit):
    __qualname__ = 'DevAccessTravelControl_TextInputLength'

    def build_msg(self, dialog, msg, *additional_tokens):
        msg.max_length = 30
        msg.min_length = 1


@Command('td1devaccess.travel_to_lot', command_type=CommandType.Live)
def travel_to_specified_lot(lot_desc_raw: int, opt_sim: OptionalTargetParam=None, _connection=None):
    output = Output(_connection)

    sim = get_optional_target(opt_sim, _connection)

    if sim is None:
        output("No valid Sim specified.")
        return

    output(f"LOT ID: {lot_desc_raw}")

    # lot_desc = services.get_instance_manager(Types.LOT_DESCRIPTION).get(lot_desc_raw)

    lot_desc = get_tunable_instance(Types.LOT_DESCRIPTION, lot_desc_raw)

    output(f"{lot_desc} | {lot_desc_raw}")

    lot_id = get_lot_id_from_instance_id(lot_desc)
    zone_id = services.get_persistence_service().resolve_lot_id_into_zone_id(lot_id, ignore_neighborhood_id=True)

    output(f"{lot_desc} | {lot_id} | {zone_id}")

    travel_sim_to_zone(sim.id, zone_id)


@Command('td1devaccess.print_lot_data', command_type=CommandType.Live)
def print_lot_data(_connection=None):
    output = Output(_connection)
    lot_desc_list = []

    output("The Lot Data Dump can be found in the Apprentice/Master Logger tagged as [INFO | TD1 TravelInteractions | TravelCheats].")

    for (key, value) in LotTuningMaps.LOT_TO_LOTTUNING_MAP.items():
        lot_desc_list.append(key)

    output(f"{services.get_instance_manager(Types.LOT_DESCRIPTION)}")

    if apprentice_logger is not None and apprentice_logger is not False:
        apprentice_logger.info(f"LOT DESCRIPTION LIST DUMP\n\n{lot_desc_list}")

    if master_logger is not None and master_logger is not False:
        master_logger.info(f"LOT DESCRIPTION LIST DUMP\n\n{lot_desc_list}")


class TravelUserSpecificLot(HasTunableSingletonFactory, AutoFactoryInit):
    FACTORY_TUNABLES = {
        'destination_lot': UiDialogTextInputOkCancel.TunableFactory(
            description='The Text Input for the user to specify their destination lot.',
            text_inputs=(LOT_TRAVEL_TEXT_INPUT),
        ),
    }

    __slots__ = 'destination_lot'

    def __call__(self, interaction, target, context):

        sim = context.sim

        def on_response(dialog):
            if master_logger is not None and master_logger is not False:
                master_logger.debug(f"[DEBUG LOOKUP] {dialog.text_input_responses.get(LOT_TRAVEL_TEXT_INPUT)}")
                
            if not dialog.accepted:
                return 0

            # lot_desc = TunableLotDescription().default(int(dialog.text_input_responses.get(LOT_TRAVEL_TEXT_INPUT)))
            lot_desc = get_tunable_instance(Types.LOT_DESCRIPTION, int(dialog.text_input_responses.get(LOT_TRAVEL_TEXT_INPUT)))
            lot_id = get_lot_id_from_instance_id(lot_desc)
            zone_id = services.get_persistence_service().resolve_lot_id_into_zone_id(lot_id, ignore_neighborhood_id=True)

            if master_logger is not None and master_logger is not False:
                master_logger.debug(f"[DEBUG LOOKUP] {lot_desc} | {lot_id} | {zone_id}")

            return zone_id

        dialog = self.destination_lot(sim, SingleSimResolver(sim))
        dialog.show_dialog(on_response=on_response)


class TD1GoToUserSpecificLotTravelInteraction(SuperInteraction):
    INSTANCE_TUNABLES = {
        'destination': TunableVariant(
            description='This is the process of how we determine which zone the Sim will travel to.',
            specific_lot=TravelSpecificLot.TunableFactory(),
            user_specific_lot=TravelUserSpecificLot.TunableFactory(),
            participant_zone=TravelParticipantZone.TunableFactory(),
            participant_home_zone=TravelParticipantHomeZone.TunableFactory(),
            object_household_owner_zone=TravelObjectHouseholdOwnerHomeZone.TunableFactory(),
            career_customer_lot=TravelCareerCustomerLot.TunableFactory(),
            default='user_specific_lot'
        ),
        'check_region_compatibility': Tunable(
            description="If checked, the interaction will fail if the actor's region is not compatible with the destination region.",
            tunable_type=bool,
            default=False
        )
    }

    @classmethod
    def _test(cls, target, context, **kwargs):
        zone_id = cls.destination(cls, target, context)
        if cls.check_region_compatibility:
            to_region = region.get_region_instance_from_zone_id(zone_id)
            from_region = region.get_region_instance_from_zone_id(cls.sim.zone_id)
            if not from_region.is_region_compatible(to_region):
                return TestResult(False,
                                  'GoToUserSpecificLotTravelInteraction: Actor region {} is not compatible with destination {}.'.format(
                                      from_region, to_region))
        if zone_id and zone_id is None:
            return TestResult(False,
                              'GoToUserSpecificLotTravelInteraction: {} could not get a valid zone from tuning or participants.',
                              cls)
        return TestResult.TRUE

    def _setup_gen(self, timeline):
        zone_id = self.destination(self, self.target, self.context)
        if zone_id and zone_id is not None:
            self.interaction_parameters['picked_zone_ids'] = frozenset((zone_id,))
        else:
            if master_logger is not None and master_logger is not False:
                master_logger.error('GoToUserSpecificLotTravelInteraction {} | {} has invalid destination.'.format(self, zone_id), owner='Original: rmccord | Post: TwelfthDoctor1')

            logger.error('GoToUserSpecificLotTravelInteraction {} | {} has invalid destination.'.format(self, zone_id), owner='Original: rmccord | Post: TwelfthDoctor1')
            return False
        result = yield from super()._setup_gen(timeline)

        if master_logger is not None and master_logger is not False:
            master_logger.debug(f"[TARGET DESTINATION | ZONE ID]: {zone_id}")

        return result
