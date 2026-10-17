"""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
TwelfthDoctor1's Developer/Debug Access Panel

> CivicPolicy Tuning

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
import sims4
from civic_policies.base_civic_policy_provider import BaseCivicPolicyProvider
from civic_policies.street_civic_policy_provider import StreetProvider
from distributor.ops import CommunityBoardDialog
from distributor.system import Distributor
from event_testing.game_option_tests import TestableGameOptions
from event_testing.test_events import TestEvent
from google.protobuf import text_format
from protocolbuffers import UI_pb2
from server_commands.argument_helpers import OptionalSimInfoParam, get_optional_target, TunableInstanceParam, extract_ints
from sims4.common import Pack
from sims4.commands import Command, cheat_output, automation_output, CommandType, CheatOutput, Output
import camera
import services
import world.street


@Command('td1devaccess.enact_civic_policy', 'civic_policy.current_street.enact', pack=Pack.EP09, command_type=CommandType.Live)
def street_civic_policy_enact(policy:TunableInstanceParam(sims4.resources.Types.SNIPPET), opt_target:OptionalSimInfoParam=None, _connection=None):
    street_service = services.street_service()
    if street_service is None:
        automation_output('Pack not loaded', _connection)
        cheat_output('Pack not loaded', _connection)
        return
    sim = get_optional_target(opt_target, _connection, target_type=OptionalSimInfoParam)

    if sim is None:

        Output('No Sim Specified.')

        return

    lot_id = services.active_lot_id()

    persistence_service = services.get_persistence_service()

    zone_id = persistence_service.resolve_lot_id_into_zone_id(lot_id, ignore_neighborhood_id=True)

    world_id = persistence_service.get_world_id_from_zone(zone_id)

    street = world.street.get_street_instance_from_world_id(world_id)

    if not street_service.enact(street, policy):
        automation_output('{} not enacted'.format(policy), _connection)
        cheat_output('{} not enacted'.format(policy), _connection)


@Command('td1devaccess.repeal_civic_policy', 'civic_policy.current_street.repeal', pack=Pack.EP09, command_type=CommandType.Live)
def street_civic_policy_repeal(policy:TunableInstanceParam(sims4.resources.Types.SNIPPET), opt_target:OptionalSimInfoParam=None, _connection=None):
    output = CheatOutput(_connection)
    street_service = services.street_service()
    if street_service is None:
        automation_output('Pack not loaded', _connection)
        cheat_output('Pack not loaded', _connection)
        return

    sim = get_optional_target(opt_target, _connection, target_type=OptionalSimInfoParam)

    if sim is None:

        Output('No Sim Specified.')

        return

    lot_id = services.active_lot_id()

    persistence_service = services.get_persistence_service()

    zone_id = persistence_service.resolve_lot_id_into_zone_id(lot_id, ignore_neighborhood_id=True)

    world_id = persistence_service.get_world_id_from_zone(zone_id)

    street = world.street.get_street_instance_from_world_id(world_id)

    if not street_service.repeal(street, policy):
        automation_output('{} not repealed'.format(policy), _connection)
        cheat_output('{} not repealed'.format(policy), _connection)


@Command('td1devaccess.vote_civic_policy', 'civic_policy.current_street.vote', pack=Pack.EP09, command_type=CommandType.Live)
def street_civic_policy_vote(policy:TunableInstanceParam(sims4.resources.Types.SNIPPET), opt_target:OptionalSimInfoParam=None, count:int=1, user_directed:bool=False, lobby_interaction:bool=False, _connection=None):
    street_service = services.street_service()
    if street_service is None:
        automation_output('Pack not loaded', _connection)
        cheat_output('Pack not loaded', _connection)
        return
    sim = get_optional_target(opt_target, _connection, target_type=OptionalSimInfoParam)

    if sim is None:

        Output('No Sim Specified.')

        return

    lot_id = services.active_lot_id()

    persistence_service = services.get_persistence_service()

    zone_id = persistence_service.resolve_lot_id_into_zone_id(lot_id, ignore_neighborhood_id=True)

    world_id = persistence_service.get_world_id_from_zone(zone_id)

    street = world.street.get_street_instance_from_world_id(world_id)
    if not street_service.vote(street, policy, count, user_directed, lobby_interaction):
        cheat_output('Could not add vote to {}'.format(policy), _connection)


@Command('td1devaccess.begin_repeal_policy', 'civic_policy.current_street.begin_repeal', pack=Pack.EP09, command_type=CommandType.Live)
def street_civic_policy_begin_repeal(policy:TunableInstanceParam(sims4.resources.Types.SNIPPET), opt_target:OptionalSimInfoParam=None, _connection=None):
    street_service = services.street_service()
    if street_service is None:
        automation_output('Pack not loaded', _connection)
        cheat_output('Pack not loaded', _connection)
        return
    sim = get_optional_target(opt_target, _connection, target_type=OptionalSimInfoParam)

    if sim is None:

        Output('No Sim Specified.')

        return

    lot_id = services.active_lot_id()

    persistence_service = services.get_persistence_service()

    zone_id = persistence_service.resolve_lot_id_into_zone_id(lot_id, ignore_neighborhood_id=True)

    world_id = persistence_service.get_world_id_from_zone(zone_id)

    street = world.street.get_street_instance_from_world_id(world_id)
    if not street_service.add_for_repeal(street, policy):
        automation_output('{} not added to up for repeal policies'.format(policy), _connection)
        cheat_output('{} not added to up for repeal policies'.format(policy), _connection)


@Command('td1devaccess.end_repeal_policy', 'civic_policy.current_street.end_repeal', pack=Pack.EP09, command_type=CommandType.Live)
def street_civic_policy_end_repeal(policy:TunableInstanceParam(sims4.resources.Types.SNIPPET), opt_target:OptionalSimInfoParam=None, _connection=None):
    street_service = services.street_service()
    if street_service is None:
        automation_output('Pack not loaded', _connection)
        cheat_output('Pack not loaded', _connection)
        return
    sim = get_optional_target(opt_target, _connection, target_type=OptionalSimInfoParam)

    if sim is None:

        Output('No Sim Specified.')

        return

    lot_id = services.active_lot_id()

    persistence_service = services.get_persistence_service()

    zone_id = persistence_service.resolve_lot_id_into_zone_id(lot_id, ignore_neighborhood_id=True)

    world_id = persistence_service.get_world_id_from_zone(zone_id)

    street = world.street.get_street_instance_from_world_id(world_id)
    if not street_service.remove_from_repeal(street, policy):
        automation_output('{} not removed from up for repeal policies'.format(policy), _connection)
        cheat_output('{} not removed from up for repeal policies'.format(policy), _connection)


@Command('td1devaccess.end_voting', 'civic_policy.current_street.force_end_voting', pack=Pack.EP09, command_type=CommandType.DebugOnly)
def street_civic_policy_force_end_voting(all_streets:bool=False, opt_target:OptionalSimInfoParam=None, _connection=None):
    street_civic_policy_service = services.street_service()
    if street_civic_policy_service is None:
        automation_output('Pack not loaded', _connection)
        cheat_output('Pack not loaded', _connection)
        return
    if all_streets:
        cheat_output('Updating all streets', _connection)
        street_civic_policy_service.force_end_voting(street=None)
        return
    sim = get_optional_target(opt_target, _connection, target_type=OptionalSimInfoParam)

    if sim is None:

        Output('No Sim Specified.')

        return

    lot_id = services.active_lot_id()

    persistence_service = services.get_persistence_service()

    zone_id = persistence_service.resolve_lot_id_into_zone_id(lot_id, ignore_neighborhood_id=True)

    world_id = persistence_service.get_world_id_from_zone(zone_id)

    street = world.street.get_street_instance_from_world_id(world_id)
    provider = street_civic_policy_service.get_provider(street)
    if provider is None:
        automation_output('Street has no provider', _connection)
        cheat_output('Street has no provider', _connection)
        return

    def output_enacted_policy_list():
        policies = provider.get_enacted_policies()
        for policy in policies:
            cheat_output('    {}'.format(policy), _connection)

    cheat_output('Before Enacted Policies', _connection)
    output_enacted_policy_list()
    if not street_civic_policy_service.force_end_voting(street):
        cheat_output('Could not force end of voting', _connection)
    cheat_output('After Enacted Policies', _connection)
    output_enacted_policy_list()



