import services
import camera
from server_commands.argument_helpers import OptionalTargetParam, get_optional_target
from sims4.commands import Command, CommandType, Output
from sims4.resources import Types

is_enable = False


class ThirdPersonCamera:
    """
    A test class to figure whether it will force the camera to be in 3rd person perspective (Orbital).
    """
    def __init__(self, follow=False):
        self.active_sim = services.client_manager().get_first_client().active_sim
        self.follow = follow

    def loop(self):
        while is_enable is True:
            if self.active_sim is not None:
                camera.focus_on_sim(self.active_sim, self.follow)


@Command('td1devaccess.force_third_person', command_type=CommandType.Live)
def force_third_person(enable=False, follow=False, _connection=None):
    is_enable = enable
    global is_enable

    cam = ThirdPersonCamera(follow=follow)
    cam.loop()
