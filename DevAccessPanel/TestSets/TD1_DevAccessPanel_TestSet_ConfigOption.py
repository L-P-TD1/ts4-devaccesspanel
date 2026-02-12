from event_testing.results import TestResult
from event_testing.test_base import BaseTest
from caches import cached_test
from sims4.tuning.tunable import HasTunableSingletonFactory, AutoFactoryInit, Tunable, TunableThreshold
from DevAccessPanel.MainLib.TD1_DevAccessPanel_Config import get_option_value
from DevAccessPanel.UtilLib.ConfigTemplate import CONFIG_DEFAULT


class TD1DevAccessPanelConfigOptionTest(HasTunableSingletonFactory, AutoFactoryInit, BaseTest):

    FACTORY_TUNABLES = {
        'config_type': Tunable(
            description='The Mod Integration to test for.',
            tunable_type=str,
            default=""
        ),
        'is_enabled': Tunable(
            description='Modifier to determine if the option is set to True or not. Boolean Only.',
            tunable_type=bool,
            default=True
        ),
        'is_matching_str': Tunable(
            description='Test to determine if the config option matches the specified option here. String Only.',
            tunable_type=str,
            default=''
        ),
        'is_matching_num': TunableThreshold(
            description='Test to determine if the specified value and config option satisfy the test. Integer and Float only.'
        )
    }
    __slots__ = ('config_type', 'is_enabled', 'is_matching_str', 'is_matching_num')

    def get_expected_args(self):
        return {}

    @cached_test
    def __call__(self):
        if self.config_type is not None and self.config_type in CONFIG_DEFAULT:
            status = get_option_value(self.config_type)
            if type(status) == bool:
                if status is self.is_enabled:
                    return TestResult.TRUE
                return TestResult(False, f'{self.config_type} is currently {status} instead of {self.is_enabled}.',
                                  tooltip=self.tooltip)
            elif type(status) == int or type(status) == float:
                if self.is_matching_num.compare(status):
                    return TestResult.TRUE
                return TestResult(False,
                                  f'{self.config_type} does not match the specified value {self.is_matching_num}',
                                  tooltip=self.tooltip)
            else:
                if status == self.is_matching_str:
                    return TestResult.TRUE
                return TestResult(False,
                                  f'{self.config_type} does not match the specified value {self.is_matching_str}.',
                                  tooltip=self.tooltip)
        else:
            return TestResult(False, 'No Config Type specified or Config Type does not exist.', tooltip=self.tooltip)
