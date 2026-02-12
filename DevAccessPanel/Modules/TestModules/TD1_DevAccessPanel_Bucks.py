import services
from bucks.bucks_utils import BucksUtils
from gsi_handlers.gsi_utils import parse_filter_to_list
from server_commands.argument_helpers import OptionalTargetParam, get_optional_target
from sims4.commands import Command, CommandType, Output
from sims4.resources import Types


@Command('td1devaccess.generate_bucks_perks_view', command_type=CommandType.Live)
def generate_bucks_perks_view(filter="perk", sim: OptionalTargetParam = None, _connection=None):
    output = Output(_connection)

    # Importation of MasterApprentice Logger
    try:
        from MasterApprenticeLib.TD1_Lib_ApprenticeLogger import ApprenticeLogger
        apprentice_logger = ApprenticeLogger('TD1 Bucks Perks Printer', main_owner='TwelfthDoctor1')

    except ImportError:
        apprentice_logger = False

    try:
        from MasterApprenticeLib.TD1_Lib_MasterLogger import MasterLogger
        master_logger = MasterLogger('TD1 Bucks Printer', main_owner='TwelfthDoctor1')

    except ImportError:
        master_logger = False

    if sim is None:
        opt_sim = get_optional_target(sim, _connection)
        sim_id = opt_sim.id

    filter_list = parse_filter_to_list(filter)
    bucks_perks_data = []
    perks_instance_manager = services.get_instance_manager(Types.BUCKS_PERK)
    previous_bucks_type = None
    for perk in perks_instance_manager.types.values():
        if perk.associated_bucks_type != previous_bucks_type:
            perk_specific_bucks_tracker = BucksUtils.get_tracker_for_bucks_type(perk.associated_bucks_type, sim_id)
            previous_bucks_type = perk.associated_bucks_type
        if 'Unlocked Only' in filter_list:
            if not perk_specific_bucks_tracker is None:
                if not perk_specific_bucks_tracker.is_perk_unlocked(perk):
                    pass
                elif len(filter_list) > 1 and str(perk.associated_bucks_type) not in filter_list:
                    pass
                else:
                    bucks_perks_data.append(
                        {
                            'sim_id': str(sim_id),
                            'name': perk.__name__,
                            'bucks_type': str(perk.associated_bucks_type),
                            'bucks_type_value': int(perk.associated_bucks_type),
                            'bucks_tracker_name': str(perk_specific_bucks_tracker),
                            'is_unlocked': perk_specific_bucks_tracker.is_perk_unlocked(
                                perk) if perk_specific_bucks_tracker is not None else False
                        }
                    )
        elif str(perk.associated_bucks_type) not in filter_list:
            pass
        else:
            bucks_perks_data.append(
                {
                    'sim_id': str(sim_id),
                    'name': perk.__name__,
                    'bucks_type': str(perk.associated_bucks_type),
                    'bucks_type_value': int(perk.associated_bucks_type),
                    'bucks_tracker_name': str(perk_specific_bucks_tracker),
                    'is_unlocked': perk_specific_bucks_tracker.is_perk_unlocked(
                        perk) if perk_specific_bucks_tracker is not None else False
                }
            )
        bucks_perks_data.append(
            {
                'sim_id': str(sim_id),
                'name': perk.__name__,
                'bucks_type': str(perk.associated_bucks_type),
                'bucks_type_value': int(perk.associated_bucks_type),
                'bucks_tracker_name': str(perk_specific_bucks_tracker),
                'is_unlocked': perk_specific_bucks_tracker.is_perk_unlocked(
                    perk) if filter_list is not None and perk_specific_bucks_tracker is not None else False
            }
        )

    for buck_data in bucks_perks_data:
        output(f'{buck_data}')

        if apprentice_logger is not None and apprentice_logger is not False:
            apprentice_logger.debug(buck_data)

        if master_logger is not None and master_logger is not False:
            master_logger.debug(buck_data)
