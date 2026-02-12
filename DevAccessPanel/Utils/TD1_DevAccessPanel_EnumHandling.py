# Importation of MasterApprentice Logger

try:
    from MasterApprenticeLib.TD1_Lib_ApprenticeLogger import ApprenticeLogger

    apprentice_logger = ApprenticeLogger('TD1 Custom Enums Injector', main_owner='TwelfthDoctor1')

except ImportError:
    apprentice_logger = False

try:
    from MasterApprenticeLib.TD1_Lib_MasterLogger import MasterLogger

    master_logger = MasterLogger('TD1 Custom Enums Injector', main_owner='TwelfthDoctor1')

except ImportError:
    master_logger = False


def add_custom_enums(enum_class: object, data_lib: dict):
    """
    Inject a custom enum to a specified enum class.

    Do note that the class of the enum is a DynamicEnum.
    :param enum_class:
    :param data_lib: dictionary where key => enum name and value => enum in FNV24
    :return:
    """
    with enum_class.make_mutable():
        for (name, number) in data_lib.items():
            enum_class._add_new_enum_value(name, number)

            message = f"{enum_class.__name__} Custom Enum: {name} | {number} is now injected."

            if apprentice_logger is not None and apprentice_logger is not False:
                apprentice_logger.info(message)

            if master_logger is not None and master_logger is not False:
                master_logger.info(message)
