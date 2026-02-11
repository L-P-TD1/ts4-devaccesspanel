import services
from caches import cached_test
from event_testing.test_base import BaseTest
from event_testing.results import TestResult
from interactions import ParticipantType
from sims4.tuning.tunable import HasTunableSingletonFactory, AutoFactoryInit, TunableThreshold, TunableVariant, \
    TunableRange, TunableEnumEntry, TunableTuple, OptionalTunable, Tunable, TunableOperator
from tag import TunableTags
from TMS.MainLib.TD1_TMS_Config import get_option_value
from sims4.math import Threshold, Operator, MAX_INT32

# Importation of MasterApprentice Logger

try:
    from MasterApprenticeLib.TD1_Lib_ApprenticeLogger import ApprenticeLogger

    apprentice_logger = ApprenticeLogger('TD1 Custom Distance TestSet', main_owner='TwelfthDoctor1')

except ImportError:
    apprentice_logger = False

try:
    from MasterApprenticeLib.TD1_Lib_MasterLogger import MasterLogger

    master_logger = MasterLogger('TD1 Custom Distance TestSet', main_owner='TwelfthDoctor1')

except ImportError:
    master_logger = False


class TD1TMSCustomDistanceTest(HasTunableSingletonFactory, AutoFactoryInit, BaseTest):
    TYPE_PARTICIPANT = 0
    TYPE_TAGS = 1
    FACTORY_TUNABLES = {
        'config_type': Tunable(
            description='The config option to pull numerical values from.',
            tunable_type=str,
            default=""
        ),
        'comparison': TunableOperator(
            description='The comparison to perform against the config option value.',
            default=Operator.GREATER_OR_EQUAL
        ),
        'level_modifier': TunableVariant(
            description='Determine how difference in levels affects distance. A modifier of 10, for example, would mean that the distance between two objects is increased by 10 meters for every floor between them.',
            specific=TunableRange(
                description='A meter modifier to add to the distance multiplied by the number of floors between subject and target.',
                tunable_type=float,
                minimum=0,
                default=8
            ),
            locked_args={'no_modifier': 0, 'infinite': None},
            default='no_modifier'
        ),
        'subject': TunableEnumEntry(
            description='The subject of the test.',
            tunable_type=ParticipantType,
            default=ParticipantType.Actor
        ),
        'target': TunableVariant(
            description='The object to find the distance to. | participant_type: Allows you to specify the participant you want to check the distance to. | object_tags: Allows you to specify a list of tags to use to find objects to test the distance to.',
            participant_type=TunableTuple(
                participant=TunableEnumEntry(
                    description='Supplies the target(s) of the test using the tuned ParticipantType.',
                    tunable_type=ParticipantType,
                    default=ParticipantType.Object
                ),
                locked_args={'test_type': TYPE_PARTICIPANT}
            ),
            object_tags=TunableTuple(
                tags=TunableTags(
                    description='Supplies the target(s) of the test using any object that matches the tuned tags.'
                ),
                locked_args={'test_type': TYPE_TAGS}
            ),
            default='participant_type'
        ),
        'object_count_threshold': OptionalTunable(
            description='The number of objects that must pass the distance test for the overall test to succeed. If enabled then the tuned number of objects must pass the distance test for the test to succeed. If disabled then ALL of the objects must pass the distance test for the test to succeed.',
            tunable=TunableThreshold(
                description='The number of objects that must pass the distance test in order for the test to succeed.'
            )
        )
    }

    __slots__ = ("config_type", "comparison", "level_modifier", "subject", "target", "object_count_threshold")

    def get_expected_args(self):
        expected_args = {'subjects': self.subject}
        if self.target.test_type == TD1TMSCustomDistanceTest.TYPE_PARTICIPANT:
            expected_args['targets'] = self.target.participant
        return expected_args

    def get_matching_objects_gen(self):
        for obj in services.object_manager().get_objects_with_tags_gen(*self.target.tags):
            yield obj

    @cached_test
    def __call__(self, subjects=(), targets=()):
        match_count = 0
        for subject in subjects:
            if subject.is_sim:
                subject = subject.get_sim_instance()
            for target in self.get_matching_objects_gen() if self.target.test_type == TD1TMSCustomDistanceTest.TYPE_TAGS else targets:
                if target.is_sim:
                    target = target.get_sim_instance()
                if subject is None or target is None:
                    distance = MAX_INT32
                else:
                    distance = (target.position - subject.position).magnitude()
                    level_difference = abs(subject.routing_surface.secondary_id - target.routing_surface.secondary_id)
                    if level_difference:
                        if self.level_modifier is None:
                            distance = MAX_INT32
                        else:
                            distance += level_difference * self.level_modifier

                distance_base = get_option_value(self.config_type)

                if distance_base is None:
                    return TestResult(False, f"Config Option {self.config_type} does not exist in Config.", tooltip=self.tooltip)

                if str(distance_base).isdecimal() is False and str(distance_base).isnumeric() is False:
                    return TestResult(False, f'Config Option {self.config_type} -> {distance_base} is neither float nor integer.', tooltip=self.tooltip)

                distance_compare = Threshold(distance_base, self.comparison)

                if distance_compare.compare(distance):
                    match_count += 1
                    if self.object_count_threshold is not None and self.object_count_threshold.compare(match_count):
                        return TestResult.TRUE
                else:
                    if self.object_count_threshold is None:
                        return TestResult(False, 'Distance test failed, all objects did not pass.',
                                          tooltip=self.tooltip)
        if self.object_count_threshold is not None:
            return TestResult(False, 'Distance test failed. The required number of matches was not met.')
        return TestResult.TRUE

    def validate_tuning_for_objective(self, objective):
        if get_option_value(self.config_type) == 0:
            if apprentice_logger is not None and apprentice_logger is not False:
                apprentice_logger.error(
                    f'Error in objective {objective} in DistanceTest. Distance Threshold has value of 0.'
                )

                if master_logger is not None and master_logger is not False:
                    master_logger.error(
                        f'Error in objective {objective} in DistanceTest. Distance Threshold has value of 0.'
                    )

        if self.object_count_threshold is not None and self.object_count_threshold.value == 0:
            if apprentice_logger is not None and apprentice_logger is not False:
                apprentice_logger.error(
                    f'Error in objective {objective} in DistanceTest. Object Count Threshold has a value of 0'
                )

                if master_logger is not None and master_logger is not False:
                    master_logger.error(
                        f'Error in objective {objective} in DistanceTest. Object Count Threshold has a value of 0'
                    )
