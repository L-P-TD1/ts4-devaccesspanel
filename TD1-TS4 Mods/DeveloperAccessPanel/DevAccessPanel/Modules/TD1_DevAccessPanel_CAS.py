import services
from server_commands.argument_helpers import OptionalTargetParam, get_optional_target
from sims.occult.occult_enums import OccultType
from sims4.commands import Command, CommandType, CommandRestrictionFlags, output, client_cheat


@Command('td1devaccess.modify_in_cas', command_type=CommandType.Live, command_restrictions=CommandRestrictionFlags.RESTRICT_SAVE_UNLOCKED)
def modify_in_cas(opt_sim:OptionalTargetParam=None, _connection=None):
    sim = get_optional_target(opt_sim, _connection)
    if sim is None:
        output('No valid target for sims.modify_in_cas.', _connection)
        return False
    client_cheat('sims.exit2cas {} {} {}'.format(sim.id, sim.household_id, services.get_active_sim().id), _connection)
    return True


@Command('td1devaccess.modify_in_cas_with_householdId', command_type=CommandType.Live, command_restrictions=CommandRestrictionFlags.RESTRICT_SAVE_UNLOCKED)
def modify_in_cas_with_household_id(opt_sim:OptionalTargetParam=None, occult_type:OccultType=OccultType.HUMAN, cmd_type:str='', _connection=None):
    sim = get_optional_target(opt_sim, _connection)
    if sim is None:
        output('No valid target for sims.modify_in_cas_with_householdId.', _connection)
        return False

    def occult_handler(sim_info):
        occult_tracker = sim_info.occult_tracker
        if occult_tracker.has_occult_type(occult_type):
            occult_tracker.set_pending_occult_type(sim_info.current_occult_types)
            occult_tracker.switch_to_occult_type(
                occult_type if occult_tracker is not OccultType.HUMAN else OccultType.HUMAN
            )

    household = sim.sim_info.household
    for household_sim_info in household.sim_info_gen():
        occult_handler(household_sim_info)
        output(f'Sim ID: {sim.id} | Occult: {occult_type} | CAS Type: {cmd_type}', _connection)

    client_cheat('sims.exit2caswithhouseholdid {} {} {}'.format(sim.id, sim.household_id, cmd_type), _connection)
    return True
