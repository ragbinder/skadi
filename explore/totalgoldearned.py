from matplotlib import pyplot as plt
from common import DEMO_FILE_PATH, PLAYER_COLORS
from skadi import demo as d


def main():
    # first, construct the demo file so Skadi can access the information
    game = d.construct(DEMO_FILE_PATH)

    total_gold_earned = {}
    game_time = []
    player_names = []

    # This loop gets all the player names from the file info.  This information
    # could also be obtained through the DT_DOTA_PlayerResource.
    # This will also create dict keys using the player names.
    for player in game.file_info.game_info.dota.player_info:
        name = player.player_name.encode('UTF-8')
        player_names.append(name)
        total_gold_earned[name] = []

    # the tick specifies a certain point in the replay.  In this loop, a stream
    # is created to loop through the replay and grab the gold values throughout.

    for tick, user_messages, game_events, world, modifiers in game.stream(tick=0):

        # Here we access the respective DTs.  A DT is a dict where information
        # is stored.  In the DT_DOTAGamerulesProxy, we can find meta information
        # about the game.  This is how game time is calcluated.  The
        # DT_DOTA_PlayerResource contains the players gold totals.  The ehandle
        # is a replay-wide unique identifier to relate different values.

        players_ehandle, players_state = world.find_by_dt('DT_DOTA_PlayerResource')
        rules_ehandle, rules_state = world.find_by_dt('DT_DOTAGamerulesProxy')

        # Wait until game has started
        if rules_state[('DT_DOTAGamerulesProxy', 'DT_DOTAGamerules.m_flGameStartTime')] != 0.0:

            # Calculate game time
            time = rules_state[('DT_DOTAGamerulesProxy', 'DT_DOTAGamerules.m_fGameTime')] \
                   - rules_state[('DT_DOTAGamerulesProxy', 'DT_DOTAGamerules.m_flGameStartTime')]
            game_time.append(time / 60)

            # Append each player's gold value to the dict.  The DT_EndScore...
            # is the key we use to find each player's gold value.
            for number, player in enumerate(player_names):
                player_num = str(number).zfill(4)
                player_gold_DT = ('DT_EndScoreAndSpectatorStats', 'm_iTotalEarnedGold.{ID}'.format(ID=player_num))
                total_gold_earned[player].append(players_state[player_gold_DT])

    # Determine max gold for plot.
    maxgold = 0

    for gold in total_gold_earned.itervalues():
        if max(gold) > maxgold:
            maxgold = max(gold)

    # Plot results
    figure, axis = plt.subplots()
    figure.patch.set_facecolor('white')
    axis.set_ylabel('m_iTotalEarnedGold [gold]')
    axis.set_xlabel('Game Time [min]')
    for i in range(10):
        axis.plot(game_time, total_gold_earned[player_names[i]], \
                  color=PLAYER_COLORS[i], linewidth=3.0, label=player_names[i])
    axis.axis((0, game_time[-1], 0, maxgold))
    axis.legend(loc='upper left', labelspacing=0.5, handletextpad=2)
    axis.set_title('Total Gold Earned [gold] vs. Time [min]')
    plt.show()


if __name__ == '__main__':
    main()
