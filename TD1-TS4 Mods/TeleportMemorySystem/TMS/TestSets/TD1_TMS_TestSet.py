from event_testing.tests import _TunableTestSetBase, TunableTestVariant, TestSetInstance
from TMS.TestSets.TD1_TMS_TestSet_ConfigOption import TD1TMSConfigOptionTest
from TMS.TestSets.TD1_TMS_TestSet_CustomDistanceTest import TD1TMSCustomDistanceTest


class TD1TMSTunableTestSet(_TunableTestSetBase, is_fragment=True):

    def __init__(self, **kwargs):
        TunableTestVariant.TEST_VARIANTS['config_type_test'] = TD1TMSConfigOptionTest.TunableFactory
        TunableTestVariant.TEST_VARIANTS['global_distance_test'] = TD1TMSCustomDistanceTest.TunableFactory
        super().__init__(test_locked_args={}, **kwargs)


class TD1TMSTestSetInstance(TestSetInstance):

    INSTANCE_TUNABLES = {'test': TD1TMSTunableTestSet()}
