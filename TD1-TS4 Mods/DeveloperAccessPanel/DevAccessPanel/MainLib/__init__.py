"""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
TwelfthDoctor1's Developer/Debug Access Panel

(C) Copyright TD1 & TWoCC 2020 - 2021
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Licensed under CC-BY-NC-ND 4.0

https://creativecommons.org/licenses/by-nc-nd/4.0/

Codes from other parties are not part of the License and Copyright.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The MainLib Module holds core functionalities of the script library.

> Injector Module
    Sole purpose is to inject into SimInfoMananger for Startup Functions.
    Also useable as a Backup Injector.

> Config Module
    This module handles the data handling of the configuration file.
    It is also able to auto-generate a config file if it does not exist.

> ModuleHandler Module
    Core functionalities of the mod are kept here.
    Parts of this module work hand in hand with other modules to provide
    information or to call other functions.

> ModCheck Module
    This module handles Integration and error bases for Mod Conflicts by checking
    if a specified script is present using try except method.
"""