import services
from server_commands.argument_helpers import OptionalTargetParam, get_optional_target
from sims4.commands import Command, CommandType, Output
from sims4.resources import Types


@Command("td1devaccess.give_all_rewards", command_type=CommandType.Live)
def give_all_rewards(opt_sim: OptionalTargetParam=None, _connection=None):
    output = Output(_connection)
    sim = get_optional_target(opt_sim, _connection)

    rewards_service = services.get_instance_manager(Types.REWARD)

    for tuning in rewards_service._tuned_classes.values():
        tuning.give_reward(sim.sim_info)
