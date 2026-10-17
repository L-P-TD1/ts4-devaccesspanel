"""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
TwelfthDoctor1's Developer/Debug Access Panel

> DevAccessPanel TestSet

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
import enum
from event_testing.results import TestResult
from event_testing.test_base import BaseTest
from caches import cached_test
from sims4.tuning.tunable import HasTunableSingletonFactory, AutoFactoryInit, TunableEnumEntry, Tunable
from DevAccessPanel.MainLib.TD1_DevAccessPanel_ModuleHandler import TD1AccessPanelModuleHandler
from DevAccessPanel.MainLib.TD1_DevAccessPanel_Config import get_option_value


class ModVersionEnums(enum.Int):
    NONE = 0
    RELEASE = 1
    DEVELOPER = 2
    BETA = 3
    DEVELOPER_RELEASE = 4
    BETA_RELEASE = 5


class TD1DevAccessPanelVersionType:
    ACCESSPANEL_VERSION_TYPE = TunableEnumEntry(
        description='The Version Type for the mod.',
        tunable_type=ModVersionEnums,
        default=ModVersionEnums.RELEASE
    )


def is_available_version(version_type):
    if version_type == TD1DevAccessPanelVersionType.ACCESSPANEL_VERSION_TYPE:
        return True
    else:
        return False


class TD1DevAccessPanelVersionTest(HasTunableSingletonFactory, AutoFactoryInit, BaseTest):

    FACTORY_TUNABLES = {
        'version': TunableEnumEntry(
            description='The Pack to test for.',
            tunable_type=ModVersionEnums,
            default=ModVersionEnums.NONE
        ),
        'whitelist_or_blacklist': Tunable(
            description='Modifier to determine if the the specified version is to be allowed if it exist.',
            tunable_type=bool,
            default=True
        ),
    }

    __slots__ = ('version', 'whitelist_or_blacklist')

    def get_expected_args(self):
        return {}

    @cached_test
    def __call__(self):
        if self.version is not None:
            if TD1AccessPanelModuleHandler.ACCESSPANEL_OVERRIDE_VERSION_TESTSET is True or get_option_value('override_version_testset') is True:
                return TestResult.TRUE
            if is_available_version(self.version):
                if self.whitelist_or_blacklist is True:
                    return TestResult.TRUE
                else:
                    return TestResult(False, f'{self.version} is the current version.', tooltip=self.tooltip)
            else:
                if self.whitelist_or_blacklist is False:
                    return TestResult.TRUE
                else:
                    return TestResult(False, f'{self.version} is not the current version.', tooltip=self.tooltip)
        else:
            return TestResult(False, f'No pack specified.', tooltip=self.tooltip)
