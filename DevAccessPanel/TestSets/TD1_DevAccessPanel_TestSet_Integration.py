"""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
TwelfthDoctor1's Developer/Debug Access Panel

> Integration TestSet

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
from sims4.tuning.tunable import HasTunableSingletonFactory, AutoFactoryInit, TunableEnumEntry, Tunable
from DevAccessPanel.MainLib.TD1_DevAccessPanel_ModuleHandler import TD1AccessPanelModuleHandler
from DevAccessPanel.MainLib.TD1_DevAccessPanel_ModCheck import IntegrationEnums, is_available_integration
from DevAccessPanel.MainLib.TD1_DevAccessPanel_Config import get_option_value


class TD1DevAccessPanelIntegrationTest(HasTunableSingletonFactory, AutoFactoryInit, BaseTest):

    FACTORY_TUNABLES = {
        'integration': TunableEnumEntry(
            description='The Mod Integration to test for.',
            tunable_type=IntegrationEnums,
            default=IntegrationEnums.NONE
        ),
        'is_installed': Tunable(
            description='Modifier to determine if the mod is installed.',
            tunable_type=bool,
            default=True
        ),
    }

    __slots__ = ('integration', 'is_installed')

    def get_expected_args(self):
        return {}

    @cached_test
    def __call__(self):
        if self.integration is not None:
            if TD1AccessPanelModuleHandler.ACCESSPANEL_OVERRIDE_INTEGRATION_TESTSET is True or get_option_value('override_integration_testset') is True:
                return TestResult.TRUE
            if is_available_integration(self.integration):
                if self.is_installed is True:
                    return TestResult.TRUE
                else:
                    return TestResult(False, f'{self.integration} exists in integration list.', tooltip=self.tooltip)
            else:
                if self.is_installed is False:
                    return TestResult.TRUE
                else:
                    return TestResult(False, f'{self.integration} is not found within the integration list.', tooltip=self.tooltip)
        else:
            return TestResult(False, f'No integration specified.', tooltip=self.tooltip)
