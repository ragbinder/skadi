from common import DEMO_FILE_PATH
from skadi import demo as d

'''
This script will take all players, check if they have a hand of midas, and if so, check how often it is on cooldown.
This is a pseduo-metric to determine how efficient they are at using their midas every time it is available, for maximum
gain.  This does not take into account strategic uses, such as possessed neutral greeps, etc.  If a player did not get
a midas during the game, it will print their name with 'no midas'.
'''

def main():
    game = d.construct(DEMO_FILE_PATH)

    player_names = []
    midas_on_cd = {}

    # Get all the player names
    for player in game.file_info.game_info.dota.player_info:
        name = player.player_name.encode('UTF-8')
        player_names.append(name)
        midas_on_cd[name] = []

    for tick, user_messages, game_events, world, modifiers in game.stream(tick=0):

        players_ehandle, players_states = world.find_by_dt('DT_DOTA_PlayerResource')
        rules_ehandle, rules_state = world.find_by_dt('DT_DOTAGamerulesProxy')

        if rules_state[('DT_DOTAGamerulesProxy', 'DT_DOTAGamerules.m_flGameStartTime')] != 0.0:
            # For each player, 
            for player_num in range(10):
                player_id = str(player_num).zfill(4)
                hero = world.find(
                    players_states[('DT_DOTA_PlayerResource', 'm_hSelectedHero.{ID}'.format(ID=player_id))])
                # For each item in that player's inventory
                for item_num in range(6):
                    item_id = str(item_num).zfill(4)
                    
                    # Try querying their hand of midas cooldown.  If they don't have a hand of midas, we'll
                    # except that KeyError and continue to the next player.
                    try:
                        item = world.find(hero[('DT_DOTA_UnitInventory', 'm_hItems.{ID}'.format(ID=item_id))])
                        if item[('DT_BaseEntity', 'm_iName')] == 'item_hand_of_midas':
                            # If they do have a miads, we'll add an item to the boolean
                            # list to determine if it's on cooldown or not.
                            item_cd = item[('DT_DOTABaseAbility', 'm_fCooldown')]
                            game_time = rules_state[('DT_DOTAGamerulesProxy', 'DT_DOTAGamerules.m_fGameTime')]
                            midas_on_cd[player_names[player_num]].append(item_cd > game_time)
                    except KeyError:
                        pass

    for player in player_names:
        if not midas_on_cd[player]:
            print '{player:''>20} : no midas'.format(player=player)
        else:
            # If midas_on_cd isn't empty, print the efficiency as a percentage
            print '{player:''>20} : {midaseff}'.format(player=player, midaseff=str(
                (float(midas_on_cd[player].count(True)) / len(midas_on_cd[player])) * 100))


if __name__ == '__main__':
    main()
