"""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
TwelfthDoctor1's Developer/Debug Access Panel

(C) Copyright TD1 & TWoCC 2020 - 2021
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Licensed under CC-BY-NC-ND 4.0

https://creativecommons.org/licenses/by-nc-nd/4.0/

Codes from other parties are not part of the License and Copyright.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The CoreLib Module holds Python/Base Core Library Scripts.

> Decorator Module
    The Decorator Injector is the old injector method used to power on_load_complete processes.

> Exception Module
    This module handles exception based errors (if required).
    Usage can be in @exception_checker or exception_checker()

> MenuUI Module
    The MenuUI module whose origins comes from the InteractionPicker is a custom picker
    capable of handling Icon State Switching.

    There is also a Base Icon Handling that can be set with a MeuUIBaseIconEnum that would then
    be translated into a IconData to be parsed to the Picker.

    The MenuUI has 2 UI Classes:
    - MenuUI
    - SettingsUI

    The MenuUI is used primarily for most Menus as they do not require specific configurations or
    requirements.

    The SettingsUI is a specialised MenuUI that is capable of handling config options and displaying
    the config in Enabled, Disabled, Disallowed and Variation States.

    Enabled and Disabled States are used for Boolean Config Options (True/False).

    Variation State is used for Integer, Float and String Config Options.

    Disallowed State is when a Config option is only allowed to be used in a certain Version Type
    (typically DEVELOPER VersionType).
"""