import os
import sys
from itertools import islice
from math import sqrt

PWD = os.path.dirname(__file__)
ROOT = os.path.abspath(os.path.join(PWD, '..'))
sys.path.append(ROOT)

DEMO_FILE_PATH = os.path.abspath(os.path.join(PWD, 'data/test.dem'))
MAX_COORD_INTEGER = 16384

from skadi import demo as d

def main():
    game = d.construct(DEMO_FILE_PATH)
    
    player_names = []
    player_coords={}
    dist={}

    for player in game.file_info.game_info.dota.player_info:
        name = player.player_name.encode('UTF-8')
        player_names.append(name)
        player_coords[name]=[]
        dist[name]=0
        
    for tick, user_messages, game_events, world, modifiers in islice(game.stream(tick=0),0,None,30):
        
        players_ehandle, players_states = world.find_by_dt('DT_DOTA_PlayerResource')
        rules_ehandle, rules_state = world.find_by_dt('DT_DOTAGamerulesProxy')
        
        if rules_state[('DT_DOTAGamerulesProxy','DT_DOTAGamerules.m_flGameStartTime')]!=0.0:
            for number, player in enumerate(player_names):
                player_id = str(number).zfill(4)
                hero=world.find(players_states[('DT_DOTA_PlayerResource','m_hSelectedHero.{ID}'.format(ID=player_id))])
                player_coords[player].append(coordFromCell(hero))

    for player in player_names:
        for time in range(1,len(player_coords[player])):
                x2,y2=player_coords[player][time]
                x1,y1=player_coords[player][time-1]
                dist[player]+=sqrt((y2-y1)**2+(x2-x1)**2)
        
        print '{player:''>20} : {dist}'.format(player=player,dist=dist[player])
            
def coordFromCell(entity):
    cellwidth = 1 << entity[('DT_BaseEntity', 'm_cellbits')]
    x = ((entity[('DT_DOTA_BaseNPC', 'm_cellX')] * cellwidth) - MAX_COORD_INTEGER) + entity[('DT_DOTA_BaseNPC', 'm_vecOrigin')][0]
    y = ((entity[('DT_DOTA_BaseNPC', 'm_cellY')] * cellwidth) - MAX_COORD_INTEGER) + entity[('DT_DOTA_BaseNPC', 'm_vecOrigin')][1]
    return (x, y)

if __name__ == '__main__':
    main()