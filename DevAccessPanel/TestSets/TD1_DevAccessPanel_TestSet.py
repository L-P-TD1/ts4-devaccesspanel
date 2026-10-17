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
