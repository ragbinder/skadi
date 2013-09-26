import re
from sets import Set
from common import DEMO_FILE_PATH
from skadi import demo as d


def main():
    # Construct a demo and make a set to store neutral model indices
    game = d.construct(DEMO_FILE_PATH)
    creep_set = Set()

    # Iterate through each tick of the replay, finding all instances of
    # 'DT_DOTA_BaseNPC_Creep_Neutral'.  These are the DTs that specify neutral
    # creep units.

    for tick, user_messages, game_events, world, modifiers in game.stream(tick=0):
        neutral = world.find_all_by_dt('DT_DOTA_BaseNPC_Creep_Neutral')

        # neutral at this point is a list of ehandles.  ehandles are unique
        # identifiers, so we want to use world.find(ehandle) to access the data
        #  Once we find them, world.find returns a dict.  
        # ('DT_BaseEntity', 'm_nModelIndex') is the key for that dict that returns
        # the model index.  All of the data stored in DTs is access this way,
        # using ehandles and keys.

        for creep in neutral:
            creep_set.add(world.find(creep)[('DT_BaseEntity', 'm_nModelIndex')])

    # Skip to the end of the replay and grab the table that allows us to convert
    # model index into a useful name.
    model_table = game.stream(tick=game.file_info.playback_ticks - 5).string_tables['modelprecache']
    creep_list = sorted(creep_set)

    for creep in creep_list:
        # This regex will take the name of the model, and strip the .mdl extension
        # this gives us a better idea of which creep is which.
        creep_name = re.findall('(?<=/)[a-z\_]+(?=\.mdl)', model_table.by_index[creep][0])[0]

        print '{0: <3}'.format(creep), ':', creep_name.encode('UTF-8')


if __name__ == '__main__':
    main()
