# Importation of MasterApprentice Logger

try:
    from MasterApprenticeLib.TD1_Lib_ApprenticeLogger import ApprenticeLogger

    apprentice_logger = ApprenticeLogger('TD1 Core Services Manager', main_owner='TwelfthDoctor1')

except ImportError:
    apprentice_logger = False

try:
    from MasterApprenticeLib.TD1_Lib_MasterLogger import MasterLogger

    master_logger = MasterLogger('TD1 Core Services Manager', main_owner='TwelfthDoctor1')

except ImportError:
    master_logger = False


class CoreServiceError(BaseException):
    def __init__(self, *args, **kwargs):
        pass

    @staticmethod
    def __new__(cls, *args, **kwargs):
        pass


class BaseServiceError(BaseException):
    def __init__(self, *args, **kwargs):
        pass

    @staticmethod
    def __new__(cls, *args, **kwargs):
        pass


class TD1CoreServiceHandler:
    """
    TD1 Core Services Handler. Responsible for handling services and logging aid.
    """

    def __init__(self, name, desc, owner, allow_debug=False):
        self.name = name
        self.desc = desc
        self.owner = owner
        self.service_state = False
        self.allow_debug = allow_debug
        self.master_logger = MasterLogger(self.name, self.owner) if master_logger is not False and master_logger is \
            not None else None

    def get_name(self):
        """
        Gets the service name.
        :return: Service Name
        """
        return self.name

    def log_service(self, message):
        """
        Logs service data to MasterLogger.
        :param message: Message to send.
        :return: None
        """
        if master_logger is not None and master_logger is not False:
            self.master_logger.log(
                f"[{self.name} SERVICE LOGGING]\n\n{message}"
            )

    def debug_service(self, message):
        """
        Logs Debug service data to MasterLogger.
        :param message: Message to send.
        :return: None
        """
        if master_logger is not None and master_logger is not False:
            self.master_logger.debug(
                f"[{self.name} SERVICE DEBUG]\n\n{message}"
            )

    def inform_service(self, message):
        """
        Logs Information service data to MasterLogger.
        :param message: Message to send.
        :return: None
        """
        if master_logger is not None and master_logger is not False:
            self.master_logger.info(
                f"[{self.name} SERVICE INFO]\n\n{message}"
            )

    def warn_service(self, message):
        """
        Logs Warning Information service data to MasterLogger.
        :param message: Message to send.
        :return: None
        """
        if master_logger is not None and master_logger is not False:
            self.master_logger.info(
                f"[{self.name} SERVICE WARNING]\n\n{message}"
            )

    def error_service(self, message):
        """
        Logs error service data to MasterLogger.
        :param message: Message to send.
        :return: None
        """
        if master_logger is not None and master_logger is not False:
            self.master_logger.error(
                f"[{self.name} SERVICE ERROR]\n\n{message}"
            )

    def raise_service_error(self, message):
        """
        Logs error service data to MasterLogger.
        :param message: Message to send.
        :return: None
        """
        if master_logger is not None and master_logger is not False:
            self.master_logger.error(
                f"[{self.name} SERVICE ERROR WITH ASSERT]\n\n{message}"
            )

        raise CoreServiceError(f"[{self.name} SERVICE ERROR WITH ASSERT]\n\n{message}")

    def declare_state(self, state):
        """
        Declare state to determine service outcome.
        :param state: True/False
        :return: None
        """
        if self.service_state is not state:
            self.service_state = state

            self.inform_service(f"{self.name} Service is now {'Enabled' if state is True else 'Disabled'}.")
            return

        else:
            self.inform_service(f"{self.name} Service is already {'Enabled' if state is True else 'Disabled'}, remaining on current state.")

    def start_service(self):
        return self.declare_state(True)

    def stop_service(self):
        return self.declare_state(False)


class TD1ModuleDocHandler(TD1CoreServiceHandler):
    pass
