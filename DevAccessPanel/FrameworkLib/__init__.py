"""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
TwelfthDoctor1's Developer/Debug Access Panel

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
The FrameworkLib Module holds TD1-based framework injection parsing scripts.

> LootBuff Handler
    The LootBuff/Trait Injector is used to inject or replace buff and/or trait tunables on the
    specified buff(s) and/or trait(s).

> AF2/3 Injector
    The AF2/3 is an injector that injects affordances (or interactions) onto the specified object(s).

> DisplayChanger Injector
    The DisplayChanger Injector is used to inject custom tested_display_overrides onto the specified
    interaction.

> CheatSetter
    The CheatSetter is a XML-Python snippet script that changes the Cheat and Debug State of an Object,
    thereby hiding interactions into the Cheat Pie Menu or allowing them to be used on the Main Pie Menu.

> RankLocker
    The RankLocker is a snippet that changes the decay_rate of a statistic.

> TestInjector
    The TestInjector is a tests injector that is capable of inject custom tests ranging from global_tests, tests,
    test_autonomous onto an interaction and/or testset.

> CustomDeathHandling
    The CustomDeathHandler is an injector that injects custom Death DynamicEnums (which cannot be done via tuning)
    and injects custom DeathTracker Mappings crucial for the Enum and DeathSuperInteraction which references the
    DeathEnum.
"""