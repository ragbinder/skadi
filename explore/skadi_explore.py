import io
import os
from itertools import islice
from collections import defaultdict

from matplotlib import pyplot as plt

from common import *
from skadi import demo as d


def startup():
    demo_file = d.construct(DEMO_FILE_PATH)

    return demo_file


def game_time_calc(state_rules):
    if state_rules[('DT_DOTAGamerulesProxy', 'DT_DOTAGamerules.m_flGameStartTime')] != 0.0:
        time = state_rules[('DT_DOTAGamerulesProxy', 'DT_DOTAGamerules.m_fGameTime')] - state_rules[
            ('DT_DOTAGamerulesProxy', 'DT_DOTAGamerules.m_flGameStartTime')]
        game_time_temp = time / 60
        game_time_real_temp = state_rules[('DT_DOTAGamerulesProxy', 'DT_DOTAGamerules.m_fGameTime')]
    else:
        game_time_temp = -999
        game_time_real_temp = -999

    return game_time_temp, game_time_real_temp


def nstime_test(demo):
    game_time = []
    game_time_real = []
    time_of_day = []
    NS_Night = []

    for game in islice(demo.stream(tick=0), 0, None, 30):

        __, __, __, world, __ = game

        __, state = world.find_by_dt('DT_DOTAGamerulesProxy')

        gt, gtr = game_time_calc(state)
        game_time.append(gt)
        game_time_real.append(gtr)

        try:
            time_of_day.append(state[('DT_DOTAGamerulesProxy', 'DT_DOTAGamerules.m_iNetTimeOfDay')])
        except KeyError:
            time_of_day.append(-999)

        try:
            NS_Night.append(state[('DT_DOTAGamerulesProxy', 'DT_DOTAGamerules.m_bIsNightstalkerNight')])
        except KeyError:
            NS_Night.append(-999)

    return game_time, game_time_real, time_of_day, NS_Night


def nstime_plotting(game_time, game_time_real, time_of_day, NS_Night):
    fig, ax1 = plt.subplots()
    fig.patch.set_facecolor('white')
    ax1.plot(game_time, time_of_day, 'k')
    l1 = ax1.plot(game_time, time_of_day, 'k', label='m_iNetTimeOfDay')
    ax1.axis((0, 50, 0, 70000))
    ax1.set_ylabel('m_iNetTimeOfDay')
    ax1.set_xlabel('Game Time [min]')
    ax1.set_title('Na`Vi vs. Alliance TI3 Finals Game #4 ID#271123757')
    ax2 = ax1.twinx()
    ax2.axis((0, 50, 0, 2))
    ax2.set_ylabel('m_bIsNightstalkerNight')
    l2 = ax2.plot(game_time, NS_Night, 'r--', label='m_bIsNightstalkerNight')
    lns = l1 + l2
    labs = [i.get_label() for i in lns]
    ax1.legend(lns, labs, loc='upper right')
    plt.show()


def totalgoldearned_test(demo):
    total_gold_earned = {}
    game_time = []
    game_time_real = []
    player_names = []
    hero_png = []

    world = demo.stream(tick=40000).world
    __, state_player = world.find_by_dt('DT_DOTA_PlayerResource')

    for i in range(10):
    #         total_gold_earned[str(i).zfill(4)]=[]
        hero_png.append(''.join([HEROID[world.find(
            state_player[('DT_DOTA_PlayerResource', '.'.join(['m_hSelectedHero', str(i).zfill(4)]))])[
            ('DT_DOTA_BaseNPC', u'm_iUnitNameIndex')]], '.png']))
        player_names.append(
            str(state_player[('DT_DOTA_PlayerResource', '.'.join(['m_iszPlayerNames', str(i).zfill(4)]))]))

    for game in islice(demo.stream(tick=0), 0, None, 60):

        __, __, __, world, __ = game

        __, state_rules = world.find_by_dt('DT_DOTAGamerulesProxy')
        __, state_player = world.find_by_dt('DT_DOTA_PlayerResource')

        gt, gtr = game_time_calc(state_rules)
        game_time.append(gt)
        game_time_real.append(gtr)

        for player_id in range(10):

            id_name = str(player_id).zfill(4)

            try:
                total_gold_earned[id_name].append(
                    state_player[('DT_EndScoreAndSpectatorStats', '.'.join(['m_iTotalEarnedGold', id_name]))])
            except KeyError:
                total_gold_earned[id_name].append(-999)

    return game_time, game_time_real, total_gold_earned, player_names, hero_png


def totalgoldearnedplotting(game_time, game_time_real, total_gold_earned, player_names, hero_png):
    fig, ax = plt.subplots()
    fig.patch.set_facecolor('white')
    ax.set_ylabel('m_iTotalEarnedGold')
    ax.set_xlabel('Game Time [min]')
    for i, key in enumerate(total_gold_earned.keys()):
        ax.plot(game_time, total_gold_earned[key], color=PLAYER_COLORS[i], linewidth=3.0, label=player_names[i])
    ax.axis((0, 40, 0, 25000))
    ax.legend(loc='upper left', labelspacing=.5, handletextpad=2)
    ax.set_title('Total Gold Earned [gold] vs. Time [min]')
    plt.show()


def stragiint_test(demo):
    strength = []
    agi = []
    intel = []
    str_tot = []
    agi_tot = []
    int_tot = []
    game_time = []
    game_time_real = []

    for game in islice(demo.stream(tick=0), 0, None, 30):

        __, __, __, world, __ = game
        __, state_rules = world.find_by_dt('DT_DOTAGamerulesProxy')
        __, state_player = world.find_by_dt('DT_DOTA_PlayerResource')

        gt, gtr = game_time_calc(state_rules)
        game_time.append(gt)
        game_time_real.append(gtr)

        if state_player[('DT_DOTA_PlayerResource', 'm_hSelectedHero.0001')] != 2097151:
            hero = world.find(state_player[('DT_DOTA_PlayerResource', 'm_hSelectedHero.0001')])
            agi.append(hero[('DT_DOTA_BaseNPC_Hero', 'm_flAgility')])
            strength.append(hero[('DT_DOTA_BaseNPC_Hero', 'm_flStrength')])
            intel.append(hero[('DT_DOTA_BaseNPC_Hero', 'm_flIntellect')])
            agi_tot.append(hero[('DT_DOTA_BaseNPC_Hero', 'm_flAgilityTotal')])
            int_tot.append(hero[('DT_DOTA_BaseNPC_Hero', 'm_flIntellectTotal')])
            str_tot.append(hero[('DT_DOTA_BaseNPC_Hero', 'm_flStrengthTotal')])
        else:
            strength.append(-999)
            agi.append(-999)
            intel.append(-999)
            str_tot.append(-999)
            agi_tot.append(-999)
            int_tot.append(-999)

    return game_time, game_time_real, strength, agi, intel, str_tot, agi_tot, int_tot


def stragiintplotting(game_time, game_time_real, strength, agi, intel, str_tot, agi_tot, int_tot):
    fig, ax = plt.subplots()
    fig.patch.set_facecolor('white')
    ax.set_ylabel('Attributes')
    ax.set_xlabel('Game Time [min]')
    ax.set_title('Na`Vi vs. Alliance TI3 Finals Game #4 ID#271123757 Alchemist Attributes')
    ax.axis((0, 40, 0, 100))
    ax.plot(game_time, agi, 'g', label='agi base', linewidth=3.0)
    ax.plot(game_time, agi_tot, 'g--', label='agi total', linewidth=3.0)
    ax.plot(game_time, intel, 'b', label='int base', linewidth=3.0)
    ax.plot(game_time, int_tot, 'b--', label='int total', linewidth=3.0)
    ax.plot(game_time, strength, 'r', label='str base', linewidth=3.0)
    ax.plot(game_time, str_tot, 'r--', label='str total', linewidth=3.0)
    ax.legend(loc='upper left')
    plt.show()


def bbcd_test(demo):
    bbcd = []
    game_time = []
    game_time_real = []

    for game in islice(demo.stream(tick=0), 0, None, 30):

        __, __, __, world, __ = game

        __, state_rules = world.find_by_dt('DT_DOTAGamerulesProxy')
        __, state_player = world.find_by_dt('DT_DOTA_PlayerResource')

        gt, gtr = game_time_calc(state_rules)
        game_time.append(gt)
        game_time_real.append(gtr)

        if state_player[('DT_DOTA_PlayerResource', 'm_hSelectedHero.0001')] != 2097151:
            bbcd.append(state_player[('DT_DOTA_PlayerResource', 'm_flBuybackCooldownTime.0001')])
        else:
            bbcd.append(-999)

    return game_time, game_time_real, bbcd


def bbcd_plotting(bbcd, game_time, game_time_real):
    fig, ax = plt.subplots()
    fig.patch.set_facecolor('white')
    ax.set_ylabel('m_flBuybackCooldownTime')
    ax.set_xlabel('Game Time [min]')
    ax.set_title('Na`Vi vs. Alliance TI3 Finals Game #4 ID#271123757 Alchemist Buyback Cooldown')
    ax.axis((0, 40, 0, 3500))
    ax.plot(game_time, bbcd, 'k', linewidth=3.0)
    ax.plot(game_time, game_time_real, 'r', linewidth=3.0)
    plt.show()


def recdmg_test(demo):
    recdmg = []
    game_time = []
    game_time_real = []
    ticks = []
    health = []
    #     items=[[] for __ in range(14)]

    for game in demo.stream(tick=0):
        tick, __, __, world, __ = game

        __, state_rules = world.find_by_dt('DT_DOTAGamerulesProxy')
        __, state_player = world.find_by_dt('DT_DOTA_PlayerResource')

        if state_player[('DT_DOTA_PlayerResource', 'm_hSelectedHero.0006')] != 2097151:
            gt, gtr = game_time_calc(state_rules)
            game_time.append(gt)
            game_time_real.append(gtr)
            ticks.append(tick)
            hero = world.find(state_player[('DT_DOTA_PlayerResource', 'm_hSelectedHero.0006')])
            recdmg.append(hero[('DT_DOTA_BaseNPC_Hero', 'm_iRecentDamage')])
            health.append(hero[('DT_DOTA_BaseNPC', 'm_iHealth')])

    return ticks, game_time, game_time_real, recdmg, health


def recdmg_plotting(game_time, game_time_real, recdmg, health):
    fig, ax1 = plt.subplots()
    fig.patch.set_facecolor('white')
    ax1.set_ylabel('m_iRecentDamage')
    ax1.set_xlabel('Game Time [min]')
    ax1.axis((0, 40, 0, 1500))
    ax1.plot(game_time, recdmg, 'k', linewidth=3.0)
    ax1.plot(game_time, health, 'r', linewidth=3.0)
    plt.show()


def invis_test(demo):
    game_time = []
    game_time_real = []
    ticks = []
    player_state = []
    #     items=[[] for __ in range(14)]

    for game in demo.stream(tick=0):
        tick, __, __, world, __ = game

        __, state_rules = world.find_by_dt('DT_DOTAGamerulesProxy')
        __, state_player = world.find_by_dt('DT_DOTA_PlayerResource')

        if state_player[('DT_DOTA_PlayerResource', 'm_hSelectedHero.0002')] != 2097151:
            gt, gtr = game_time_calc(state_rules)
            game_time.append(gt)
            game_time_real.append(gtr)

            ticks.append(tick)
            hero = world.find(state_player[('DT_DOTA_PlayerResource', 'm_hSelectedHero.0002')])
            player_state.append(hero[(u'DT_DOTA_BaseNPC', u'm_nUnitState')])

    return ticks, game_time, game_time_real, player_state


def invis_plotting(ticks, game_time, game_time_real, player_state):
    fig, ax = plt.subplots()
    fig.patch.set_facecolor('white')
    ax.set_ylabel('m_nUnitState')
    ax.set_xlabel('Game Time [tick]')
    ax.set_title('m_nUnitState vs. Time [min]  Match# 298738006')
    ax.plot(ticks, player_state, 'k', linewidth=3.0)
    plt.show()


def gamestate(demo):
    for game in demo.stream(tick=0):
        tick, __, __, world, __ = game

        __, state = world.find_by_dt('DT_DOTAGamerulesProxy')

        print str(tick).zfill(6), ':', state[('DT_DOTAGamerulesProxy', 'DT_DOTAGamerules.m_nGameState')]


def neutrals(demo):
    from sets import Set

    creep_set = Set()

    for game in islice(demo.stream(tick=0), 0, None, 1800):
        __, __, __, world, __ = game

        neutrals = world.find_all_by_dt("DT_DOTA_BaseNPC_Creep_Neutral")
        for creep in neutrals:
            creep_set.add(world.find(creep)[('DT_BaseEntity', 'm_nModelIndex')])

    for creep in creep_set:
        print '{index}:{model}'.format(index=creep,
                                       model=demo.stream(tick=0).string_tables['modelprecache'].by_index[creep][0])


def wiki_scrape(demo):
    DT_Set = defaultdict()

    stream = demo.stream(tick=5000)

    for i in range(len(stream.world.by_dt.keys())):
        DT = str(stream.world.by_dt.keys()[i])
        DT_Set[DT] = set()
        __, state = stream.world.find_by_dt(DT)
        for j in range(len(state.keys())):
            prop = str(state.keys()[j])
            DT_Set[DT].add(prop)

    return DT_Set


def items(world):
    heroes = world.find_all_by_dt("DT_DOTA_Unit_Hero*")

    for no, hero in enumerate(heroes):
        print 'hero #', no
        for i in range(14):
            item_ehandle = world.find(hero)[('DT_DOTA_UnitInventory', '.'.join(['m_hItems', str(i).zfill(4)]))]

            if item_ehandle != 2097151:
                print world.find(item_ehandle)[('DT_BaseEntity', 'm_iName')].replace('item_', '')


def wiki_create(DT_Set):
    base_path = '/Users/Andrew/Documents/Computer/Workspace/SkadiWiki'

    with io.open(os.path.join(base_path, 'Home.md'), 'ab+') as homefile:
        DTKeys = DT_Set.keys().sort()
        for i in DTKeys:
            DT_Name = str(DTKeys[i])
            DT_FileName = ''.join([str(DTKeys[i]), '.md'])
            homefile.write(''.join(['* [', DT_Name, '](https://github.com/garth5689/skadi/wiki/', DT_Name, ') \n']))
            with io.open(os.path.join(base_path, DT_FileName), 'ab+') as dtfile:
                dtfile.write(''.join(['### Full list of ', DT_Name, ' properties \n\n']))
                PropKeys = DT_Set[DT_Set.keys()[i]].sort()
                for __ in range(len(PropKeys)):
                    dtfile.write(''.join(['* `', str(PropKeys.pop()).replace("u'", "'"), '`: \n']))


if __name__ == '__main__':
    demo = startup()
    game_time, game_time_real, bbcd = bbcd_test(demo)