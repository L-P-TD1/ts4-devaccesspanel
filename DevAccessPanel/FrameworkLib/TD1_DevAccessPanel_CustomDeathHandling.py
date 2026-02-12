"""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
TwelfthDoctor1's Developer/Debug Access Panel

> Custom Death Handling Injector Tuning

(C) Copyright TD1 & TWoCC 2020 - 2021
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Licensed under CC-BY-NC-ND 4.0

https://creativecommons.org/licenses/by-nc-nd/4.0/

Codes from other parties are not part of the License and Copyright.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""
import services
from _sims4_collections import frozendict
from DevAccessPanel.Utils.TD1_DevAccessPanel_EnumHandling import add_custom_enums
from interactions.utils.death import DeathType, DeathTracker
from sims4.resources import Types
from sims4.tuning.instances import HashedTunedInstanceMetaclass
from sims4.tuning.tunable import TunableMapping, TunableEnumEntry, TunableReference

# Importation of MasterApprentice Logger

try:
    from MasterApprenticeLib.TD1_Lib_ApprenticeLogger import ApprenticeLogger

    apprentice_logger = ApprenticeLogger('TD1 DeathTracker Injector', main_owner='TwelfthDoctor1')

except ImportError:
    apprentice_logger = False

try:
    from MasterApprenticeLib.TD1_Lib_MasterLogger import MasterLogger

    master_logger = MasterLogger('TD1 DeathTracker Injector', main_owner='TwelfthDoctor1')

except ImportError:
    master_logger = False

# Custom Enum Injection: DeathType
# Add the following EnumValue (FNV24) and its respective tag below as name, number.
# Example: add_category_tags('BucksTagName', EnumValue)
add_custom_enums(DeathType, {'TD1PieDeath': 1179724})
add_custom_enums(DeathType, {'TD1CursedDrinkDeath': 11353219})


class TD1DeathTrackerMappingInjector(metaclass=HashedTunedInstanceMetaclass,
                                     manager=services.get_instance_manager(Types.SNIPPET)):
    INSTANCE_TUNABLES = {
        'death_type_ghost_trait_map': TunableMapping(
            description='The ghost trait to be applied to a Sim when they die with a given death type.',
            key_type=TunableEnumEntry(
                description='The death type to map to a ghost trait.',
                tunable_type=DeathType,
                default=DeathType.NONE
            ),
            key_name='Death Type',
            value_type=TunableReference(
                description='The ghost trait to apply to a Sim when they die from the specified death type.',
                manager=services.get_instance_manager(Types.TRAIT)
            ),
            value_name='Ghost Trait'
        )
    }

    __slots__ = 'death_type_ghost_trait_map'

    @classmethod
    def _tuning_loaded_callback(cls):
        DeathTracker.DEATH_TYPE_GHOST_TRAIT_MAP = frozendict(
            dict(DeathTracker.DEATH_TYPE_GHOST_TRAIT_MAP) + cls.death_type_ghost_trait_map
        )
