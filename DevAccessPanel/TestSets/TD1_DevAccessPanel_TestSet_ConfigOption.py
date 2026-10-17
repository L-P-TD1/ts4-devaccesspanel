"""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
TwelfthDoctor1's Developer/Debug Access Panel

> ConfigOption TestSet

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
