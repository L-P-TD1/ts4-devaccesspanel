import enum
from server_commands.argument_helpers import OptionalTargetParam, get_optional_target
from sims4.commands import Command, CommandType, Output
from statistics.commodity import MotiveUIStyle
import services
from sims4.resources import Types

WITCH_CHARGE = 213024
WEREWOLF_FURY = 276223


class CommodityPriority(enum.Int):
    NONE = 0
    WITCH = 1
    WEREWOLF = 2


PRIORITY = CommodityPriority.WEREWOLF

@Command("td1devaccess.change_orb_stat", command_type=CommandType.Live)
def change_orb_stat(sim: OptionalTargetParam, priority:str, _connection=None):
    output = Output(_connection)
    sim = get_optional_target(sim, _connection)

    if priority.lower() != "witch" and priority.lower() != "werewolf":
        output("ERROR: Choose from either Witch or Werewolf to have orb stat priority.")

    needs_tracker = sim.sim_info.commodity_tracker
    stats = needs_tracker.get_all_commodities()
    needs_orb = []
    for stat in stats:
        if stat.is_commodity and stat.ui_render_style == MotiveUIStyle.ORB:
            needs_orb.append(stat)

    witch_charge_stat = services.get_instance_manager(Types.STATISTIC).get(WITCH_CHARGE)
    werewolf_fury_stat = services.get_instance_manager(Types.STATISTIC).get(WEREWOLF_FURY)

    output(f"{needs_orb[0].stat_name} | {needs_orb[1].stat_name} | {witch_charge_stat.stat_name} | {werewolf_fury_stat.stat_name}")

    for need in needs_orb:
        if need.stat_name == witch_charge_stat.stat_name:
            if priority.lower() == "witch":
                witch_charge_stat.ui_sort_index = 1
                output("Spellcaster Charge set to HIGH priority.")

            else:
                witch_charge_stat.ui_sort_index = 0
                output("Spellcaster Charge set to LOW priority.")

        elif need.stat_name == werewolf_fury_stat.stat_name:
            if priority.lower() == "werewolf":
                werewolf_fury_stat.ui_sort_index = 1
                output("Werewolf Fury set to HIGH priority.")

            else:
                werewolf_fury_stat.ui_sort_index = 0
                output("Werewolf Fury set to LOW priority.")


def force_orb_commodity_priority():
    witch_charge_stat = services.get_instance_manager(Types.STATISTIC).get(WITCH_CHARGE)
    werewolf_fury_stat = services.get_instance_manager(Types.STATISTIC).get(WEREWOLF_FURY)

    if PRIORITY == CommodityPriority.WEREWOLF:
        werewolf_fury_stat.ui_sort_index = 9
        witch_charge_stat.ui_sort_index = 0

    elif PRIORITY == CommodityPriority.WITCH:
        werewolf_fury_stat.ui_sort_index = 0
        witch_charge_stat.ui_sort_index = 9

    else:
        pass
