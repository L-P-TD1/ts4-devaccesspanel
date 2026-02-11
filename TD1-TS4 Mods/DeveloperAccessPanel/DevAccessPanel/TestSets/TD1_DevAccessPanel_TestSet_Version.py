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
