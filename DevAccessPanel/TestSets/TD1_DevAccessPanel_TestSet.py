from event_testing.tests import _TunableTestSetBase, TunableTestVariant, TestSetInstance
from DevAccessPanel.TestSets.TD1_DevAccessPanel_TestSet_Pack import TD1DevAccessPanelPackTest
from DevAccessPanel.TestSets.TD1_DevAccessPanel_TestSet_Integration import TD1DevAccessPanelIntegrationTest
from DevAccessPanel.TestSets.TD1_DevAccessPanel_TestSet_Version import TD1DevAccessPanelVersionTest
from DevAccessPanel.TestSets.TD1_DevAccessPanel_TestSet_ConfigOption import TD1DevAccessPanelConfigOptionTest


class TD1DevAccessPanelTunableTestSet(_TunableTestSetBase, is_fragment=True):

    def __init__(self, **kwargs):
        TunableTestVariant.TEST_VARIANTS['pack_test'] = TD1DevAccessPanelPackTest.TunableFactory
        TunableTestVariant.TEST_VARIANTS['integration_test'] = TD1DevAccessPanelIntegrationTest.TunableFactory
        TunableTestVariant.TEST_VARIANTS['version_test'] = TD1DevAccessPanelVersionTest.TunableFactory
        TunableTestVariant.TEST_VARIANTS['config_type_test'] = TD1DevAccessPanelConfigOptionTest.TunableFactory
        super().__init__(test_locked_args={}, **kwargs)


class TD1DevAccessPanelTestSetInstance(TestSetInstance):

    INSTANCE_TUNABLES = {'test': TD1DevAccessPanelTunableTestSet()}
