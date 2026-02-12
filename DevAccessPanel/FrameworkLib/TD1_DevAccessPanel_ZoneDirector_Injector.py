"""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
TwelfthDoctor1's Developer/Debug Access Panel

> ZoneDirector Injector Tuning

(C) Copyright TD1 & TWoCC 2020 - 2021
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Licensed under CC-BY-NC-ND 4.0

https://creativecommons.org/licenses/by-nc-nd/4.0/

Codes from other parties are not part of the License and Copyright.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""
import services
from scheduler import SituationWeeklySchedule
from sims4.log import Logger
from sims4.resources import Types
from sims4.tuning.instances import HashedTunedInstanceMetaclass
from sims4.tuning.tunable import TunableReference, TunableList, TunableTuple, TunableVariant, \
    TunableEnumEntry, Tunable
from situations.additional_situation_sources import HolidayWalkbys, ZoneModifierSituations, NarrativeSituations
from situations.situation_curve import SituationCurve, ShiftlessDesiredSituations, SituationShiftStrictness

# Importation of MasterApprentice Logger

try:
    from MasterApprenticeLib.TD1_Lib_ApprenticeLogger import ApprenticeLogger

    apprentice_logger = ApprenticeLogger('TD1 ZoneDirector/Venue Injector', main_owner='TwelfthDoctor1')

except ImportError:
    apprentice_logger = False

try:
    from MasterApprenticeLib.TD1_Lib_MasterLogger import MasterLogger

    master_logger = MasterLogger('TD1 ZoneDirector/Venue Injector', main_owner='TwelfthDoctor1')

except ImportError:
    master_logger = False

logger = Logger('TD1 ZoneDirector/Venue Injector')


class TD1DevAccessPanelZoneDirectorInjector(metaclass=HashedTunedInstanceMetaclass,
                                            manager=services.get_instance_manager(Types.SNIPPET)):
    INSTANCE_TUNABLES = {
        'zone_director_reference': TunableReference(
            description='The ZoneDirector to be injected to.',
            manager=services.get_instance_manager(Types.ZONE_DIRECTOR),
            pack_safe=True,
            allow_none=False
        ),
        'situation_shifts': TunableList(
            description='A list of situation distributions and their strictness rules.',
            tunable=TunableTuple(
                shift_curve=TunableVariant(
                    curve_based=SituationCurve.TunableFactory(
                        get_create_params={'user_facing': True}
                    ),
                    shiftless=ShiftlessDesiredSituations.TunableFactory(
                        get_create_params={'user_facing': True}
                    ),
                    default='curve_based'
                ),
                shift_strictness=TunableEnumEntry(
                    description='Determine how situations on shift will be handled on shift change. Example: I want 3 customers between 10-12.  then after 12 I want only 1.  Having this checked will allow 3 customers to stay and will let situation duration kick the sim out when appropriate.  This will not create new situations if over the cap.',
                    tunable_type=SituationShiftStrictness,
                    default=SituationShiftStrictness.DESTROY
                ),
                additional_sources=TunableList(
                    description='Any additional sources of NPCs that we want to use to add into the possible situations of this shift curve.',
                    tunable=TunableVariant(
                        description='The different additional situation sources that we want to use to get additional situation possibilities that can be chosen.',
                        holiday=HolidayWalkbys.TunableFactory(),
                        zone_modifier=ZoneModifierSituations.TunableFactory(),
                        narrative=NarrativeSituations.TunableFactory(),
                        default='holiday'
                    )
                ),
                count_based_on_expected_sims=Tunable(
                    description='If checked then we will count based on the number of Sims that are expected to be in the Situation rather than the number of situations.',
                    tunable_type=bool,
                    default=False
                )
            )
        ),
    }

    __slots__ = ['zone_director_reference', 'situation_shifts']

    @classmethod
    def _tuning_loaded_callback(cls):
        if cls.situation_shifts is not None:
            cls.add_situation_shifts_to_zone_director(cls.zone_director_reference, cls.situation_shifts)

    # Injection Handling Section

    @staticmethod
    def add_situation_shifts_to_zone_director(zone_director, situation_shifts):
        zone_director.situation_shifts += situation_shifts

        logger.info("Zone Director: {} now has {}.".format(zone_director, situation_shifts))

        if apprentice_logger is not None and apprentice_logger is not False:
            apprentice_logger.info("Zone Director: {} now has {}.".format(zone_director, situation_shifts))

        if master_logger is not None and master_logger is not False:
            master_logger.info("Zone Director: {} now has {}.".format(zone_director, situation_shifts))


class TD1DevAccessPanelVenueInjector(metaclass=HashedTunedInstanceMetaclass,
                                     manager=services.get_instance_manager(Types.SNIPPET)):
    INSTANCE_TUNABLES = {
        'venue_reference': TunableReference(
            description="The Venue to be injected to.",
            manager=services.get_instance_manager(Types.VENUE),
            pack_safe=True,
            allow_none=False
        ),
        'background_event_schedule': SituationWeeklySchedule.TunableFactory(
            description='The Background Events that run on this venue. They run underneath any user facing Situations and there can only be one at a time. The schedule times and durations are windows in which background events can start.'
        ),
        'special_event_schedule': SituationWeeklySchedule.TunableFactory(
            description='The Special Events that run on this venue. These run on top of Background Events. We run only one user facing event at a time, so if the player started something then this may run in the background, otherwise the player will be invited to join in on this Venue Special Event.'
        ),

    }

    __slots__ = ('venue_reference', 'background_event_schedule', 'special_event_schedule')

    @classmethod
    def _tuning_loaded_callback(cls):
        if cls.venue_reference:
            if cls.background_event_schedule is not None:
                cls.inject_background_event_schedule(cls.venue_reference, cls.background_event_schedule)

            if cls.special_event_schedule is not None:
                cls.inject_special_event_schedule(cls.venue_reference, cls.special_event_schedule)

    @staticmethod
    def inject_background_event_schedule(venue, schedule):
        venue.background_event_schedule = venue.background_event_schedule + schedule

        logger.info(f"Injecting Venue:\n{venue}\n\nWith:\n{schedule}")

        if apprentice_logger is not None and apprentice_logger is not False:
            apprentice_logger.info(f"Injecting Venue:\n{venue}\n\nWith:\n{schedule}")

        if master_logger is not None and master_logger is not False:
            master_logger.info(f"Injecting Venue:\n{venue}\n\nWith:\n{schedule}")

    @staticmethod
    def inject_special_event_schedule(venue, schedule):
        venue.special_event_schedule = venue.special_event_schedule + schedule

        logger.info(f"Injecting Venue:\n{venue}\n\nWith:\n{schedule}")

        if apprentice_logger is not None and apprentice_logger is not False:
            apprentice_logger.info(f"Injecting Venue:\n{venue}\n\nWith:\n{schedule}")

        if master_logger is not None and master_logger is not False:
            master_logger.info(f"Injecting Venue:\n{venue}\n\nWith:\n{schedule}")
