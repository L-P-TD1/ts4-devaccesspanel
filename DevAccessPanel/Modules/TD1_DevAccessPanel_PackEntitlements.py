"""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
TwelfthDoctor1's Developer/Debug Access Panel

> PackENtitlements Module

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
import services
from sims4.common import Pack, get_available_packs
from sims4.commands import Command, CommandType, CheatOutput, Output
from sims4.localization import LocalizationHelperTuning
from ui.ui_dialog_notification import UiDialogNotification

# Importation of MasterApprentice Logger
try:
    from MasterApprenticeLib.TD1_Lib_ApprenticeLogger import ApprenticeLogger
    apprentice_logger = ApprenticeLogger('TD1 Developer/Debug Access Panel Pack Entitlements', main_owner='TwelfthDoctor1')

except ImportError:
    apprentice_logger = False

try:
    from MasterApprenticeLib.TD1_Lib_MasterLogger import MasterLogger
    master_logger = MasterLogger('TD1 Developer/Debug Access Panel Pack Entitlements', main_owner='TwelfthDoctor1')

except ImportError:
    master_logger = False


class TD1DevAccessPanel_PackEntitlements:
    pass

pack_list = []

expansion_pack_list = []

game_pack_list = []

stuff_pack_list = []

kits_list = []

misc_packs_list = []

all_pack_type = ['BASE_GAME', 'EP', 'GP', 'SP', 'FP']

is_installed = []

all_packs_list = []

all_ep_list = []

all_gp_list = []

all_sp_list = []

all_misc_packs_list = []


def get_all_packs():
    return tuple(pack for pack in Pack)


@Command('td1devaccess.list_packs', 'mtx.list_packs', command_type=CommandType.Live)
def list_packs_on_entitlement(_connection=None):
    output = CheatOutput(_connection)
    client = services.client_manager().get_first_client()

    # Section 1: Master Pack List Collection & Sorting
    for pack in get_all_packs():
        if pack is Pack.BASE_GAME:
            all_packs_list.append(pack)  # <- Base Game Holder (Compulsory)
        elif str(pack).find("EP") != -1:
            all_ep_list.append(pack)  # <- EP Holder
        elif str(pack).find("GP") != -1:
            all_gp_list.append(pack)  # <- GP Holder
        elif str(pack).find("SP") != -1:
            all_sp_list.append(pack)  # <- SP Holder
        else:
            all_misc_packs_list.append(pack)  # <- FP Holder (Only FP01)

    all_packs_list.extend(all_ep_list)
    all_packs_list.extend(all_gp_list)
    all_packs_list.extend(all_sp_list)
    all_packs_list.extend(all_misc_packs_list)
    all_packs_list.append(Pack.BASE_GAME)

    # Section 2: User Pack List Collection & Sorting
    for pack in get_available_packs():
        if pack is Pack.BASE_GAME:
            pack_list.append(pack)  # <- Base Game Holder (Compulsory)
        elif str(pack).find("EP") != -1:
            expansion_pack_list.append(pack)  # <- EP Holder
        elif str(pack).find("GP") != -1:
            game_pack_list.append(pack)  # <- GP Holder
        elif str(pack).find("SP") != -1:
            stuff_pack_list.append(pack)  # <- SP Holder
        else:
            misc_packs_list.append(pack)  # <- FP Holder (Only FP01)

    pack_list.extend(expansion_pack_list)
    pack_list.extend(game_pack_list)
    pack_list.extend(stuff_pack_list)
    pack_list.extend(misc_packs_list)
    pack_list.append(Pack.BASE_GAME)

    # output('{}'.format(all_packs_list[0:71]))
    # output('')
    # output('{}'.format(pack_list[0:71]))

    # Section 3: Dealing With Pack Status
    for master_pack in all_packs_list:
        status = None
        init_status = None
        for pack in pack_list:
            if pack is not Pack.BASE_GAME:
                init_status = True
            if pack is master_pack:
                is_installed.append("Installed")
                status = True
                output('{}: Installed'.format(master_pack))
            else:
                if init_status is True:
                    if status is not True:
                        if pack is Pack.BASE_GAME:
                            is_installed.append("Not Installed/Disabled")
                            output('{}: Not Installed/Disabled'.format(master_pack))

    all_packs_list.pop()
    pack_list.pop()

    # Section 4: Printing on Console (Cheat) & Setting it for Notification
    output('Packs List')
    output('\nNote: Placeholder Packs will show up here. This does not mean that they will be released.\n')
    incrementor = 1
    ep_merge = None
    gp_merge = None
    sp_merge = None
    misc_merge = None
    ep_text = None
    gp_text = None
    sp_text = None
    misc_text = None

    for master_pack in all_packs_list:
        num = len(is_installed)
        if incrementor > num:
            return
        status = is_installed[incrementor]
        output('{}: {}'.format(master_pack, status))

        if str(master_pack).find("EP") != -1:
            if ep_merge is None:
                ep_merge = str(master_pack) + ": " + str(status)
                ep_text = ep_merge
            else:
                ep_merge = "\n" + str(master_pack) + ": " + str(status)
                ep_text += ep_merge

        elif str(master_pack).find("GP") != -1:
            if gp_merge is None:
                gp_merge = str(master_pack) + ": " + str(status)
                gp_text = gp_merge
            else:
                gp_merge = "\n" + str(master_pack) + ": " + str(status)
                gp_text += gp_merge

        elif str(master_pack).find("SP") != -1:
            if sp_merge is None:
                sp_merge = str(master_pack) + ": " + str(status)
                sp_text = sp_merge
            else:
                sp_merge = "\n" + str(master_pack) + ": " + str(status)
                sp_text += sp_merge

        else:
            if misc_merge is None:
                misc_merge = str(master_pack) + ": " + str(status)
                misc_text = misc_merge
            else:
                misc_merge = "\n" + str(master_pack) + ": " + str(status)
                misc_text += misc_merge

        incrementor += 1

        if apprentice_logger is not None and apprentice_logger is not False:
            apprentice_logger.info("TD1 DevAccessPanel Pack Entitlements\n\n{}\n{}\n{}\n{}".format(
                misc_text, ep_text, gp_text, sp_text
            ))

        if master_logger is not None and master_logger is not False:
            master_logger.info("TD1 DevAccessPanel Pack Entitlements\n\n{}\n{}\n{}\n{}".format(
                misc_text, ep_text, gp_text, sp_text
            ))

    # Section 5: Setting Up the Notification
    message_title_1 = lambda **_: LocalizationHelperTuning.get_raw_text("Pack Entitlements: BG & FPs")
    message_text_1 = lambda **_: LocalizationHelperTuning.get_raw_text(str(misc_text))

    notification_1 = UiDialogNotification.TunableFactory().default(
        client.active_sim,
        text=message_text_1,
        title=message_title_1
    )

    message_title_2 = lambda **_: LocalizationHelperTuning.get_raw_text("Pack Entitlements: EPs")
    message_text_2 = lambda **_: LocalizationHelperTuning.get_raw_text(str(ep_text))

    notification_2 = UiDialogNotification.TunableFactory().default(
        client.active_sim,
        text=message_text_2,
        title=message_title_2
    )

    message_title_3 = lambda **_: LocalizationHelperTuning.get_raw_text("Pack Entitlements: GPs")
    message_text_3 = lambda **_: LocalizationHelperTuning.get_raw_text(str(gp_text))

    notification_3 = UiDialogNotification.TunableFactory().default(
        client.active_sim,
        text=message_text_3,
        title=message_title_3
    )

    message_title_4 = lambda **_: LocalizationHelperTuning.get_raw_text("Pack Entitlements: SPs & Kits")
    message_text_4 = lambda **_: LocalizationHelperTuning.get_raw_text(str(sp_text))

    notification_4 = UiDialogNotification.TunableFactory().default(
        client.active_sim,
        text=message_text_4,
        title=message_title_4
    )

    notification_1.show_dialog()
    notification_2.show_dialog()
    notification_3.show_dialog()
    notification_4.show_dialog()

    pack_list.clear()
    all_packs_list.clear()
    expansion_pack_list.clear()
    all_ep_list.clear()
    game_pack_list.clear()
    all_gp_list.clear()
    stuff_pack_list.clear()
    all_sp_list.clear()
    misc_packs_list.clear()
    all_misc_packs_list.clear()
