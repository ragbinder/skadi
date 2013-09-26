from common import DEMO_FILE_PATH
from skadi import demo as d


def main():
    game = d.construct(DEMO_FILE_PATH)

    player_names = []
    midas_on_cd = {}

    for player in game.file_info.game_info.dota.player_info:
        name = player.player_name.encode('UTF-8')
        player_names.append(name)
        midas_on_cd[name] = []

    for tick, user_messages, game_events, world, modifiers in game.stream(tick=0):

        players_ehandle, players_states = world.find_by_dt('DT_DOTA_PlayerResource')
        rules_ehandle, rules_state = world.find_by_dt('DT_DOTAGamerulesProxy')

        if rules_state[('DT_DOTAGamerulesProxy', 'DT_DOTAGamerules.m_flGameStartTime')] != 0.0:
            for player_num in range(10):
                player_id = str(player_num).zfill(4)
                hero = world.find(
                    players_states[('DT_DOTA_PlayerResource', 'm_hSelectedHero.{ID}'.format(ID=player_id))])
                for item_num in range(6):
                    item_id = str(item_num).zfill(4)
                    try:
                        item = world.find(hero[('DT_DOTA_UnitInventory', 'm_hItems.{ID}'.format(ID=item_id))])
                        if item[('DT_BaseEntity', 'm_iName')] == 'item_hand_of_midas':
                            item_cd = item[('DT_DOTABaseAbility', 'm_fCooldown')]
                            game_time = rules_state[('DT_DOTAGamerulesProxy', 'DT_DOTAGamerules.m_fGameTime')]
                            midas_on_cd[player_names[player_num]].append(item_cd > game_time)
                    except KeyError:
                        pass

    for player in player_names:
        if not midas_on_cd[player]:
            print '{player:''>20} : no midas'.format(player=player)
        else:
            print '{player:''>20} : {midaseff}'.format(player=player, midaseff=str(
                (float(midas_on_cd[player].count(True)) / len(midas_on_cd[player])) * 100))


if __name__ == '__main__':
    main()