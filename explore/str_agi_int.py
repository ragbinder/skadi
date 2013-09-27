import matplotlib.pyplot as plt
from common import DEMO_FILE_PATH
from skadi import demo as d


def stragiint():
    game = d.construct(DEMO_FILE_PATH)

    strength = []
    agi = []
    intel = []
    str_tot = []
    agi_tot = []
    int_tot = []
    game_time = []

    for tick, user_messages, game_events, world, modifiers in game.stream(tick=0):

        players_ehandle, players_state = world.find_by_dt('DT_DOTA_PlayerResource')
        rules_ehandle, rules_state = world.find_by_dt('DT_DOTAGamerulesProxy')

        if rules_state[('DT_DOTAGamerulesProxy', 'DT_DOTAGamerules.m_flGameStartTime')] != 0.0:
            hero = world.find(players_state[('DT_DOTA_PlayerResource', 'm_hSelectedHero.0001')])
            agi.append(hero[('DT_DOTA_BaseNPC_Hero', 'm_flAgility')])
            strength.append(hero[('DT_DOTA_BaseNPC_Hero', 'm_flStrength')])
            intel.append(hero[('DT_DOTA_BaseNPC_Hero', 'm_flIntellect')])
            agi_tot.append(hero[('DT_DOTA_BaseNPC_Hero', 'm_flAgilityTotal')])
            int_tot.append(hero[('DT_DOTA_BaseNPC_Hero', 'm_flIntellectTotal')])
            str_tot.append(hero[('DT_DOTA_BaseNPC_Hero', 'm_flStrengthTotal')])

            time = rules_state[('DT_DOTAGamerulesProxy', 'DT_DOTAGamerules.m_fGameTime')] \
                   - rules_state[('DT_DOTAGamerulesProxy', 'DT_DOTAGamerules.m_flGameStartTime')]
            game_time.append(time / 60)

    return game_time, strength, agi, intel, str_tot, agi_tot, int_tot


def stragiintplotting(game_time, strength, agi, intel, str_tot, agi_tot, int_tot):
    fig, ax = plt.subplots()
    fig.patch.set_facecolor('white')
    ax.set_ylabel('Attributes')
    ax.set_xlabel('Game Time [min]')
    ax.axis((0, 40, 0, 100))
    ax.plot(game_time, agi, 'g', label='agi base', linewidth=3.0)
    ax.plot(game_time, agi_tot, 'g--', label='agi total', linewidth=3.0)
    ax.plot(game_time, intel, 'b', label='int base', linewidth=3.0)
    ax.plot(game_time, int_tot, 'b--', label='int total', linewidth=3.0)
    ax.plot(game_time, strength, 'r', label='str base', linewidth=3.0)
    ax.plot(game_time, str_tot, 'r--', label='str total', linewidth=3.0)
    ax.legend(loc='upper left')
    plt.show()


if __name__ == '__main__':
    game_time, strength, agi, intel, str_tot, agi_tot, int_tot = stragiint()
    stragiintplotting(game_time, strength, agi, intel, str_tot, agi_tot, int_tot)