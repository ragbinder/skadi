import matplotlib.pyplot as plt

from common import DEMO_FILE_PATH
from skadi import demo as d


def bbcd():
    game = d.construct(DEMO_FILE_PATH)

    bbcd = []
    game_time = []

    for tick, user_messages, game_events, world, modifiers in game.stream(tick=0):

        players_ehandle, players_state = world.find_by_dt('DT_DOTA_PlayerResource')
        rules_ehandle, rules_state = world.find_by_dt('DT_DOTAGamerulesProxy')

        if rules_state[('DT_DOTAGamerulesProxy', 'DT_DOTAGamerules.m_flGameStartTime')] != 0.0:
            time = rules_state[('DT_DOTAGamerulesProxy', 'DT_DOTAGamerules.m_fGameTime')] \
                   - rules_state[('DT_DOTAGamerulesProxy', 'DT_DOTAGamerules.m_flGameStartTime')]
            game_time.append(time / 60)

            bbcd.append(players_state[('DT_DOTA_PlayerResource', 'm_flBuybackCooldownTime.0001')])

    return game_time, bbcd


def bbcd_plotting(game_time, bbcd):
    fig, ax = plt.subplots()
    fig.patch.set_facecolor('white')
    ax.set_ylabel('m_flBuybackCooldownTime')
    ax.set_xlabel('Game Time [min]')
    ax.axis((0, 40, 0, 3500))
    ax.plot(game_time, bbcd, 'k', linewidth=3.0)
    plt.show()


if __name__ == '__main__':
    game_time, bbcd = bbcd()
    bbcd_plotting(game_time, bbcd)