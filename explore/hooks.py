import os
import matplotlib.pyplot as plt
from matplotlib.pyplot import savefig
import matplotlib.offsetbox as ob
from common import HERO_ICONS_PATH, MINIMAP_PATH, HEROID, DEMO_FILE_PATH, worldcoordfromcell, imagecoordfromworld
from skadi import demo as d

'''
This script should plot all the hooks that occured in a game with pudge.  It uses the modifer placed on a hooked
target as the indicator for a hook.  I import several items from common, which is my location for utility scripts
and dicts.  it can be found at https://github.com/garth5689/skadi/blob/explore/explore You will also need the folder
of Hero Icons to plot the targets.  Hooks that do not hit a hero, but do hit a creep are red lines.  Hooks that miss
completely, or kill a hero on impact are not implemented yet.  These are features for a future version.
'''

def main():
    game = d.construct(DEMO_FILE_PATH)
    game_time = []
    hooks = []

    for tick, user_messages, game_events, world, modifiers in game.stream(tick=0):

        rules_ehandle, rules_state = world.find_by_dt('DT_DOTAGamerulesProxy')

        if rules_state[('DT_DOTAGamerulesProxy', 'DT_DOTAGamerules.m_flGameStartTime')] != 0.0:

            time = rules_state[('DT_DOTAGamerulesProxy', 'DT_DOTAGamerules.m_fGameTime')] - \
                   rules_state[('DT_DOTAGamerulesProxy', 'DT_DOTAGamerules.m_flGameStartTime')]
            game_time.append(time / 60)

            # Here we want to start going through the modifiers.
            # We are looking for 'modifier_pudge_meat_hook'. 
            # Once this modifier is encountered, we find the location of pudge and the target
            # and the target's model index.  We will use this for plotting later.
            for parent, parent_modifiers in modifiers.by_parent.iteritems():
                for mod_num, mod_dict in parent_modifiers.iteritems():
                    if mod_dict['name'] == 'modifier_pudge_meat_hook':
                        if not hooks:
                            # Each hook will be a dict with the following information to make plotting easy.
                            hooks.append({'tick': tick, 'target': parent,
                                          'target_index': world.find(parent)[('DT_DOTA_BaseNPC', 'm_iUnitNameIndex')],
                                          'time': time / 60.0,
                                          'pudge_pos': worldcoordfromcell(world.find(mod_dict['caster'])),
                                          'target_pos': worldcoordfromcell(world.find(parent))})
                        elif tick - hooks[-1]['tick'] > 100:
                            hooks.append({'tick': tick, 'target': parent,
                                          'target_index': world.find(parent)[('DT_DOTA_BaseNPC', 'm_iUnitNameIndex')],
                                          'time': time / 60.0,
                                          'pudge_pos': worldcoordfromcell(world.find(mod_dict['caster'])),
                                          'target_pos': worldcoordfromcell(world.find(parent))})
                        else:
                            pass
    
    # In my replay, there was an error with me hooking an allied hero.  This hook kept showing up in each tick,
    # so I removed it manually.
    # hooks = [hooks[i] for i in range(len(hooks)) if hooks[i]['target'] != 832840]
    return hooks


def hook_plotting(hooks):

    # Add our map image, scale & color axes appropriately, and make the axes take up the whole figure
    map_img = plt.imread(MINIMAP_PATH)
    fig, ax = plt.subplots(figsize=(10.25, 10.25))
    ax.set_position([0, 0, 1, 1])
    plt.imshow(map_img)
    fig.patch.set_facecolor('black')
    ax.patch.set_facecolor('black')
    ax.axis((0, 1024, 1024, 0))
    
    # Each hero icon is plotted as an OffsetImage.  Basically the image is an OffsetImage, which is
    # then added to the plot as an OffsetBox.
    pudge_img = plt.imread(os.path.abspath(os.path.join(HERO_ICONS_PATH, 'npc_dota_hero_pudge.png')))
    pudge_oi = ob.OffsetImage(pudge_img, zoom=0.75)

    for hook in hooks:

        px, py = imagecoordfromworld(hook['pudge_pos'][0], hook['pudge_pos'][1])
        tx, ty = imagecoordfromworld(hook['target_pos'][0], hook['target_pos'][1])

        ax.plot([px, tx], [py, ty], color='r', zorder=3, linewidth=5)
        pudge_ab = ob.AnnotationBbox(pudge_oi, (px, py))
        pudge_ab.patch.set_alpha(0)
        pudge_art = ax.add_artist(pudge_ab)
        pudge_art.set(zorder=4)

        #Can't remember right now why I had a KeyError exception here.
        try:
            hero_img_name = HEROID[hook['target_index']]
            target_img = plt.imread(
                os.path.abspath(os.path.join(HERO_ICONS_PATH, '{hero}.png'.format(hero=hero_img_name))))
            target_oi = ob.OffsetImage(target_img, zoom=0.75)
            target_ab = ob.AnnotationBbox(target_oi, (tx, ty))
            target_ab.patch.set_alpha(0)
            target_art = ax.add_artist(target_ab)
            target_art.set(zorder=5)
        except KeyError:
            pass
    
    #Replace this with a suitable save location if you want to save
    savefig('/Users/Andrew/Desktop/hooks.png', dpi=100)


if __name__ == '__main__':
    hooks = main()
    hook_plotting(hooks)
