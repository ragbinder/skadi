import matplotlib.pyplot as plt

from common import DEMO_FILE_PATH
from skadi import demo as d


def ns_night():
    game = d.construct(DEMO_FILE_PATH)

    game_time = []
    time_of_day = []
    ns_night = []

    for tick, user_messages, game_events, world, modifiers in game.stream(tick=0):

        rules_ehandle, rules_state = world.find_by_dt('DT_DOTAGamerulesProxy')

        if rules_state[('DT_DOTAGamerulesProxy', 'DT_DOTAGamerules.m_flGameStartTime')] != 0.0:
            time = rules_state[('DT_DOTAGamerulesProxy', 'DT_DOTAGamerules.m_fGameTime')] \
                   - rules_state[('DT_DOTAGamerulesProxy', 'DT_DOTAGamerules.m_flGameStartTime')]
            game_time.append(time / 60)

            time_of_day.append(rules_state[('DT_DOTAGamerulesProxy', 'DT_DOTAGamerules.m_iNetTimeOfDay')])
            ns_night.append(rules_state[('DT_DOTAGamerulesProxy', 'DT_DOTAGamerules.m_bIsNightstalkerNight')])

    return game_time, time_of_day, ns_night


def ns_night_plotting(game_time, time_of_day, ns_night):
    fig, ax1 = plt.subplots()
    fig.patch.set_facecolor('white')
    ax1.plot(game_time, time_of_day, 'k')
    l1 = ax1.plot(game_time, time_of_day, 'k', label='m_iNetTimeOfDay')
    ax1.axis((0, 50, 0, 70000))
    ax1.set_ylabel('m_iNetTimeOfDay')
    ax1.set_xlabel('Game Time [min]')
    ax2 = ax1.twinx()
    ax2.axis((0, 50, 0, 2))
    ax2.set_ylabel('m_bIsNightstalkerNight')
    l2 = ax2.plot(game_time, ns_night, 'r--', label='m_bIsNightstalkerNight')
    lns = l1 + l2
    labs = [i.get_label() for i in lns]
    ax1.legend(lns, labs, loc='upper right')
    plt.show()


if __name__ == '__main__':
    game_time, time_of_day, ns_night = ns_night()
    ns_night_plotting(game_time, time_of_day, ns_night)