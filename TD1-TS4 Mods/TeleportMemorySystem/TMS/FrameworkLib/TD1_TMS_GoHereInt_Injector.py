"""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
TwelfthDoctor1's Teleport Memory System

> GoHere Interaction Injector Tuning

(C) Copyright TD1 & TWoCC 2020 - 2024
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Licensed under CC-BY-NC-ND 4.0

https://creativecommons.org/licenses/by-nc-nd/4.0/

Codes from other parties are not part of the License and Copyright.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""
import services
from event_testing import tests
from interactions.utils.tunable_icon import TunableIconVariant
from sims4.common import Pack, is_available_pack
from sims4.localization import TunableLocalizedStringFactory
from sims4.log import Logger
from sims4.resources import Types
from sims4.tuning.instances import HashedTunedInstanceMetaclass
from sims4.tuning.tunable import TunableReference, TunableList, TunableTuple, OptionalTunable, TunableEnumEntry

# Importation of MasterApprentice Logger
try:
    from MasterApprenticeLib.TD1_Lib_ApprenticeLogger import ApprenticeLogger

    apprentice_logger = ApprenticeLogger('TD1 Go Here Interaction Injector', main_owner='TwelfthDoctor1')

except ImportError:
    apprentice_logger = False

try:
    from MasterApprenticeLib.TD1_Lib_MasterLogger import MasterLogger

    master_logger = MasterLogger('TD1 Go Here Interaction Injector', main_owner='TwelfthDoctor1')

except ImportError:
    master_logger = False

logger = Logger('TD1 Go Here Interaction Injector', default_owner='TwelfthDoctor1')


class TD1TMSGoHereInteractionInjector(metaclass=HashedTunedInstanceMetaclass,
                                      manager=services.get_instance_manager(Types.SNIPPET)):
    INSTANCE_TUNABLES = {
        'go_here_interaction_reference': TunableReference(
            description='The Instance ID of the specified Go Here Super Interaction.',
            manager=services.get_instance_manager(Types.INTERACTION),
            class_restrictions=('GoHereSuperInteraction',)
        ),
        'tested_display_overrides': TunableList(
            description='The tested display overrides to inject into the specified Go Here Super Interaction.',
            tunable=TunableTuple(
                description='A tuple of a test and the name that would be chosen if the test passes.',
                test=tests.TunableTestSet(
                    description='The test to run to see if the display_name should be overridden.'
                ),
                new_display_name=OptionalTunable(
                    description='If enabled, we will override the display name. Sometimes you might not want to do this, such as with crafting interactions that show the recipe name.',
                    tunable=TunableLocalizedStringFactory(
                        description='The localized name of this interaction. it takes two tokens, the actor (0) and target object (1) of the interaction.'),
                    enabled_by_default=True
                ),
                new_pie_menu_icon=OptionalTunable(
                    description='If this display name overrides the default display name, this will be the icon that is shown. If this is not tuned then the default pie menu icon for this interaction will be\n                    used.\n                    ',
                    tunable=TunableIconVariant(
                        description='The icon to display in the pie menu.',
                        icon_pack_safe=True
                    )
                ),
                new_display_tooltip=OptionalTunable(
                    description='Tooltip to show on this pie menu option.',
                    tunable=TunableLocalizedStringFactory()
                ),
                new_pie_menu_category=TunableReference(
                    description='Pie menu category to put interaction under.',
                    manager=services.get_instance_manager(Types.PIE_MENU_CATEGORY),
                    allow_none=True
                ),
                parent_name=OptionalTunable(
                    description='If enabled, we will insert the name into this parent string in the pie menu.',
                    tunable=TunableLocalizedStringFactory(
                        description='The localized parent name of this interaction. token 0 is actor, token 1 is normal pie name'
                    )
                )
            )
        ),
        'pack': TunableEnumEntry(
            description='The pack used to test.',
            tunable_type=Pack,
            default=Pack.BASE_GAME
        ),
    }

    __slots__ = ('go_here_interaction_reference', 'tested_display_overrides', 'pack')

    @classmethod
    def _tuning_loaded_callback(cls):
        if is_available_pack(cls.pack):
            if cls.go_here_interaction_reference is not None and cls.tested_display_overrides is not None:
                inject_tested_display_name_overrides(cls.go_here_interaction_reference,
                                                     cls.tested_display_overrides)
            else:
                message2 = f'No Go Here Interaction and/or Testable Display Overrides injectable. Please check snippet.'
                logger.error(message2, owner='TwelfthDoctor1')

                if apprentice_logger is not None and apprentice_logger is not False:
                    apprentice_logger.error(message2, owner='TwelfthDoctor1')

                if master_logger is not None and master_logger is not False:
                    master_logger.error(message2, owner='TwelfthDoctor1')
        else:
            message3 = f'Pack: {cls.pack} Not Available to allow injection to proceed. This injection instance will be ignored.'
            logger.info(message3, owner='TwelfthDoctor1')

            if apprentice_logger is not None and apprentice_logger is not False:
                apprentice_logger.info(message3, owner='TwelfthDoctor1')

            if master_logger is not None and master_logger is not False:
                master_logger.info(message3, owner='TwelfthDoctor1')


class TD1TMSGoHereInteractionInjectorV2(metaclass=HashedTunedInstanceMetaclass,
                                        manager=services.get_instance_manager(Types.SNIPPET)):
    INSTANCE_TUNABLES = {
        'go_here_int': TunableList(
            description='A list of things to be injected.',
            tunable=TunableTuple(
                description='A Tuple holding things to inject to the specified GoHere Interaction.',
                go_here_interaction_reference=TunableReference(
                    description='The Instance ID of the specified Go Here Super Interaction.',
                    manager=services.get_instance_manager(Types.INTERACTION),
                    class_restrictions=('GoHereSuperInteraction',)
                ),
                tested_display_overrides=TunableList(
                    description='The tested display overrides to inject into the specified Go Here Super Interaction.',
                    tunable=TunableTuple(
                        description='A tuple of a test and the name that would be chosen if the test passes.',
                        test=tests.TunableTestSet(
                            description='The test to run to see if the display_name should be overridden.'
                        ),
                        new_display_name=OptionalTunable(
                            description='If enabled, we will override the display name. Sometimes you might not want to do this, such as with crafting interactions that show the recipe name.',
                            tunable=TunableLocalizedStringFactory(
                                description='The localized name of this interaction. it takes two tokens, the actor (0) and target object (1) of the interaction.'),
                            enabled_by_default=True
                        ),
                        new_pie_menu_icon=OptionalTunable(
                            description='If this display name overrides the default display name, this will be the icon that is shown. If this is not tuned then the default pie menu icon for this interaction will be\n                    used.\n                    ',
                            tunable=TunableIconVariant(
                                description='The icon to display in the pie menu.',
                                icon_pack_safe=True
                            )
                        ),
                        new_display_tooltip=OptionalTunable(
                            description='Tooltip to show on this pie menu option.',
                            tunable=TunableLocalizedStringFactory()
                        ),
                        new_pie_menu_category=TunableReference(
                            description='Pie menu category to put interaction under.',
                            manager=services.get_instance_manager(Types.PIE_MENU_CATEGORY),
                            allow_none=True
                        ),
                        parent_name=OptionalTunable(
                            description='If enabled, we will insert the name into this parent string in the pie menu.',
                            tunable=TunableLocalizedStringFactory(
                                description='The localized parent name of this interaction. token 0 is actor, token 1 is normal pie name'
                            )
                        )
                    )
                ),
                pack=TunableEnumEntry(
                    description='The pack used to test.',
                    tunable_type=Pack,
                    default=Pack.BASE_GAME
                ),
            )
        )
    }

    __slots__ = 'go_here_int'

    @classmethod
    def _tuning_loaded_callback(cls):
        if cls.go_here_int is not None:
            for data in cls.go_here_int:
                if is_available_pack(data.pack):
                    if data.go_here_interaction_reference is not None and data.tested_display_overrides is not None:
                        inject_tested_display_name_overrides(data.go_here_interaction_reference,
                                                             data.tested_display_overrides)
                    else:
                        message2 = f'No Go Here Interaction and/or Testable Display Overrides injectable. Please check snippet.'
                        logger.error(message2, owner='TwelfthDoctor1')

                        if apprentice_logger is not None and apprentice_logger is not False:
                            apprentice_logger.error(message2, owner='TwelfthDoctor1')

                        if master_logger is not None and master_logger is not False:
                            master_logger.error(message2, owner='TwelfthDoctor1')
                else:
                    message3 = f'Pack: {data.pack} Not Available to allow injection to proceed. This injection instance will be ignored.'
                    logger.info(message3, owner='TwelfthDoctor1')

                    if apprentice_logger is not None and apprentice_logger is not False:
                        apprentice_logger.info(message3, owner='TwelfthDoctor1')

                    if master_logger is not None and master_logger is not False:
                        master_logger.info(message3, owner='TwelfthDoctor1')


def inject_tested_display_name_overrides(interaction, overrides_to_inject):
    # for overrides_int in interaction.display_name_overrides.overrides:
    interaction.display_name_overrides.overrides += overrides_to_inject

    message1 = f'Go Here Interaction: {interaction} being injected with {overrides_to_inject}, \n\nresulting in {interaction.display_name_overrides.overrides}'
    logger.info(message1, owner='TwelfthDoctor1')

    if apprentice_logger is not None and apprentice_logger is not False:
        apprentice_logger.info(message1, owner='TwelfthDoctor1')

    if master_logger is not None and master_logger is not False:
        master_logger.info(message1, owner='TwelfthDoctor1')
