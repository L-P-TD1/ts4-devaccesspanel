"""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
TwelfthDoctor1's Developer/Debug Access Panel

> InfoLister Module

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
from server_commands.argument_helpers import OptionalTargetParam, get_optional_target
from sims4.commands import Command, CommandType, output
from sims4.resources import Types


# Type Text Converter
def convert_typestr_to_typeint(type_str):
    """
    Convert Lowercase String Types into proper Types.
    """
    if type_str == "interaction":
        return Types.INTERACTION

    elif type_str == "buff":
        return Types.BUFF

    elif type_str == "trait":
        return Types.TRAIT

    elif type_str == "action" or type_str == "loot":
        return Types.ACTION

    elif type_str == "ac_cache":
        return Types.AC_CACHE

    elif type_str == "achievement":
        return Types.ACHIEVEMENT

    elif type_str == "achievement_category":
        return Types.ACHIEVEMENT_CATEGORY

    elif type_str == "achievement_collection":
        return Types.ACHIEVEMENT_COLLECTION

    elif type_str == "animation":
        return Types.ANIMATION

    elif type_str == "aspiration":
        return Types.ASPIRATION

    elif type_str == "aspiration_category":
        return Types.ASPIRATION_CATEGORY

    elif type_str == "aspiration_track":
        return Types.ASPIRATION_TRACK

    elif type_str == "away_action":
        return Types.AWAY_ACTION

    elif type_str == "balloon":
        return Types.BALLOON

    else:
        return Types.INVALID


# TMS Info to be matched against
tms_traits = [
    10760501216104755480,
    13212266947000163928,
    14216887555706128234,
    17651445185794912764,
    14397550127706485724,
    13272767914332633668,
    9592693799654824662,
    16396485019333961014,
    18008731275607325275,
    11747225551054246279,
    11555373528213947560,
    11555375727237204046,
    15905974779494409483,
    15305168741322583900,
    15305170940345840370,
    16699379430913097855,
    14781975565827589768,
    17844492510063473271,
    15286728415382451776,
    9229185247782942544,
    15081900718012207330,
    13171737776804396430,
    16625656771725357044,
    155860,
    155861,
    14293373760291272983,
    13302803134369982456,
    13302805333393238686,
    9388367873247577943,
    12378150380800800905,
    16452022451175551808,
    12378154778847313861,
    17691447597187342018,
    12164515499549796385,
    16141698299623181042,
    18287439845397848025,
    17924260800677990134,
    9446822085751918062,
    13965452029516233120,
    214838,
    217844
]

tms_buffs = [
    152520,
    152521,
    15191212286770539627,
    18440038451570190247,
    12505548506328372845,
    10418413357221096115,
    10585701346395406236,
    14824061154521288189,
]


@Command('td1devaccess.list_traits', command_type=CommandType.Live)
def show_traits(trait_filter:str="", tag_filter:str="",opt_sim:OptionalTargetParam=None, _connection=None):
    sim = get_optional_target(opt_sim, _connection)
    if sim is not None:
        trait_tracker = sim.sim_info.trait_tracker
        if trait_tracker is None:
            output("Sim {} doesn't have trait tracker".format(sim), _connection)
            return
        output('Sim {} has {} traits equipped, {} slots left'.format(sim, len(trait_tracker), trait_tracker.empty_slot_number), _connection)

        # automation_output('TraitsList; Status:Begin', _connection)

        if tag_filter.lower() == "tms":
            output("TMS Traits Equipped:", _connection)

            for trait in trait_tracker.equipped_traits:
                for tms_trait in tms_traits:
                    if trait == tms_trait:
                        if trait.__name__.find(trait_filter) != -1 or trait_filter == "":
                            s = f'{trait.__name__} | {trait}'
                            output(s, _connection)

        else:
            output("Equipped traits:", _connection)

            for trait in trait_tracker.equipped_traits:
                if str(trait.__name__).find(trait_filter) != -1 or trait_filter == "":
                    s = f'{trait.__name__} | {trait}'
                    output(s, _connection)

            # automation_output('TraitsList; Status:Data, Trait:{}'.format(trait.__name__), _connection)
        # automation_output('TraitsList; Status:End', _connection)


@Command('td1devaccess.list_buffs', command_type=CommandType.Live)
def show_buffs(buff_filter:str="", tag_filter:str="",opt_sim:OptionalTargetParam=None, _connection=None):
    sim = get_optional_target(opt_sim, _connection)
    if sim is None:
        output('Invalid Sim id: {}'.format(opt_sim), _connection)
        return False

    buff_component = sim.Buffs

    if buff_component is None:
        output('Sim has no Buffs component: {}'.format(opt_sim), _connection)
        return False

    # automation_output('BuffsInfo; Status:Begin', _connection)

    if tag_filter.lower() == "tms":
        output("TMS Buffs Equipped:", _connection)

        for buff_entry in buff_component:
            for tms_buff in tms_buffs:
                if buff_entry.__class__ == tms_buff:
                    if buff_entry.__class__.__name__.find(buff_filter) != -1 or buff_filter == "":
                        s = ' {}'.format(buff_entry.__class__.__name__)
                        output(s, _connection)

    else:
        output('Buffs: ', _connection)

        for buff_entry in buff_component:
            if str(buff_entry.__class__.__name__).find(buff_filter) != -1 or buff_filter == "":
                s = ' {}'.format(buff_entry.__class__.__name__)
                output(s, _connection)

        # automation_output('BuffsInfo; Status:Data, Value:{}'.format(buff_entry.__class__.__name__), _connection)
    # automation_output('BuffsInfo; Status:End', _connection)

@Command("td1devaccess.get_info_from_id", command_type=CommandType.Live)
def get_info_from_id(id:int=0, type:str=""):
    pass
