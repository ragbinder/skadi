import os
import sys
import matplotlib.pyplot as plt
from matplotlib.pyplot import savefig
import matplotlib.offsetbox as ob

PWD = os.path.dirname(__file__)
ROOT = os.path.abspath(os.path.join(PWD, '..'))
sys.path.append(ROOT)

DEMO_FILE_PATH = os.path.abspath(os.path.join(PWD, 'data/test.dem'))
MAX_COORD_INTEGER = 16384

HEROID = {'npc_dota_hero_abaddon': 102, 'npc_dota_hero_alchemist': 73, 'npc_dota_hero_ancient_apparition': 68,
          'npc_dota_hero_antimage': 1, 'npc_dota_hero_axe': 2, 'npc_dota_hero_bane': 3, 'npc_dota_hero_base': 0,
          'npc_dota_hero_batrider': 65, 'npc_dota_hero_beastmaster': 38, 'npc_dota_hero_bloodseeker': 4,
          'npc_dota_hero_bounty_hunter': 62, 'npc_dota_hero_brewmaster': 78, 'npc_dota_hero_bristleback': 99,
          'npc_dota_hero_broodmother': 61, 'npc_dota_hero_centaur': 96, 'npc_dota_hero_chaos_knight': 81,
          'npc_dota_hero_chen': 66, 'npc_dota_hero_clinkz': 56, 'npc_dota_hero_crystal_maiden': 5,
          'npc_dota_hero_dark_seer': 55, 'npc_dota_hero_dazzle': 50, 'npc_dota_hero_death_prophet': 43,
          'npc_dota_hero_disruptor': 87, 'npc_dota_hero_doom_bringer': 69, 'npc_dota_hero_dragon_knight': 49,
          'npc_dota_hero_drow_ranger': 6, 'npc_dota_hero_earthshaker': 7, 'npc_dota_hero_elder_titan': 103,
          'npc_dota_hero_enchantress': 58, 'npc_dota_hero_enigma': 33, 'npc_dota_hero_faceless_void': 41,
          'npc_dota_hero_furion': 53, 'npc_dota_hero_gyrocopter': 72, 'npc_dota_hero_huskar': 59,
          'npc_dota_hero_invoker': 74, 'npc_dota_hero_jakiro': 64, 'npc_dota_hero_juggernaut': 8,
          'npc_dota_hero_keeper_of_the_light': 90, 'npc_dota_hero_kunkka': 23, 'npc_dota_hero_legion_commander': 104,
          'npc_dota_hero_leshrac': 52, 'npc_dota_hero_lich': 31, 'npc_dota_hero_life_stealer': 54,
          'npc_dota_hero_lina': 25, 'npc_dota_hero_lion': 26, 'npc_dota_hero_lone_druid': 80, 'npc_dota_hero_luna': 48,
          'npc_dota_hero_lycan': 77, 'npc_dota_hero_magnataur': 97, 'npc_dota_hero_medusa': 94,
          'npc_dota_hero_meepo': 82, 'npc_dota_hero_mirana': 9, 'npc_dota_hero_morphling': 10,
          'npc_dota_hero_naga_siren': 89, 'npc_dota_hero_necrolyte': 36, 'npc_dota_hero_nevermore': 11,
          'npc_dota_hero_night_stalker': 60, 'npc_dota_hero_nyx_assassin': 88, 'npc_dota_hero_obsidian_destroyer': 76,
          'npc_dota_hero_ogre_magi': 84, 'npc_dota_hero_omniknight': 57, 'npc_dota_hero_phantom_assassin': 44,
          'npc_dota_hero_phantom_lancer': 12, 'npc_dota_hero_puck': 13, 'npc_dota_hero_pudge': 14,
          'npc_dota_hero_pugna': 45, 'npc_dota_hero_queenofpain': 39, 'npc_dota_hero_rattletrap': 51,
          'npc_dota_hero_razor': 15, 'npc_dota_hero_riki': 32, 'npc_dota_hero_rubick': 86,
          'npc_dota_hero_sand_king': 16, 'npc_dota_hero_shadow_demon': 79, 'npc_dota_hero_shadow_shaman': 27,
          'npc_dota_hero_shredder': 98, 'npc_dota_hero_silencer': 75, 'npc_dota_hero_skeleton_king': 42,
          'npc_dota_hero_skywrath_mage': 101, 'npc_dota_hero_slardar': 28, 'npc_dota_hero_slark': 93,
          'npc_dota_hero_sniper': 35, 'npc_dota_hero_spectre': 67, 'npc_dota_hero_spirit_breaker': 71,
          'npc_dota_hero_storm_spirit': 17, 'npc_dota_hero_sven': 18, 'npc_dota_hero_templar_assassin': 46,
          'npc_dota_hero_tidehunter': 29, 'npc_dota_hero_tinker': 34, 'npc_dota_hero_tiny': 19,
          'npc_dota_hero_treant': 83, 'npc_dota_hero_troll_warlord': 95, 'npc_dota_hero_tusk': 100,
          'npc_dota_hero_undying': 85, 'npc_dota_hero_ursa': 70, 'npc_dota_hero_vengefulspirit': 20,
          'npc_dota_hero_venomancer': 40, 'npc_dota_hero_viper': 47, 'npc_dota_hero_visage': 92,
          'npc_dota_hero_warlock': 37, 'npc_dota_hero_weaver': 63, 'npc_dota_hero_windrunner': 21,
          'npc_dota_hero_wisp': 91, 'npc_dota_hero_witch_doctor': 30, 'npc_dota_hero_zuus': 22,
          102: 'npc_dota_hero_abaddon', 73: 'npc_dota_hero_alchemist', 68: 'npc_dota_hero_ancient_apparition',
          1: 'npc_dota_hero_antimage', 2: 'npc_dota_hero_axe', 3: 'npc_dota_hero_bane', 0: 'npc_dota_hero_base',
          65: 'npc_dota_hero_batrider', 38: 'npc_dota_hero_beastmaster', 4: 'npc_dota_hero_bloodseeker',
          62: 'npc_dota_hero_bounty_hunter', 78: 'npc_dota_hero_brewmaster', 99: 'npc_dota_hero_bristleback',
          61: 'npc_dota_hero_broodmother', 96: 'npc_dota_hero_centaur', 81: 'npc_dota_hero_chaos_knight',
          66: 'npc_dota_hero_chen', 56: 'npc_dota_hero_clinkz', 5: 'npc_dota_hero_crystal_maiden',
          55: 'npc_dota_hero_dark_seer', 50: 'npc_dota_hero_dazzle', 43: 'npc_dota_hero_death_prophet',
          87: 'npc_dota_hero_disruptor', 69: 'npc_dota_hero_doom_bringer', 49: 'npc_dota_hero_dragon_knight',
          6: 'npc_dota_hero_drow_ranger', 7: 'npc_dota_hero_earthshaker', 103: 'npc_dota_hero_elder_titan',
          58: 'npc_dota_hero_enchantress', 33: 'npc_dota_hero_enigma', 41: 'npc_dota_hero_faceless_void',
          53: 'npc_dota_hero_furion', 72: 'npc_dota_hero_gyrocopter', 59: 'npc_dota_hero_huskar',
          74: 'npc_dota_hero_invoker', 64: 'npc_dota_hero_jakiro', 8: 'npc_dota_hero_juggernaut',
          90: 'npc_dota_hero_keeper_of_the_light', 23: 'npc_dota_hero_kunkka', 104: 'npc_dota_hero_legion_commander',
          52: 'npc_dota_hero_leshrac', 31: 'npc_dota_hero_lich', 54: 'npc_dota_hero_life_stealer',
          25: 'npc_dota_hero_lina', 26: 'npc_dota_hero_lion', 80: 'npc_dota_hero_lone_druid', 48: 'npc_dota_hero_luna',
          77: 'npc_dota_hero_lycan', 97: 'npc_dota_hero_magnataur', 94: 'npc_dota_hero_medusa',
          82: 'npc_dota_hero_meepo', 9: 'npc_dota_hero_mirana', 10: 'npc_dota_hero_morphling',
          89: 'npc_dota_hero_naga_siren', 36: 'npc_dota_hero_necrolyte', 11: 'npc_dota_hero_nevermore',
          60: 'npc_dota_hero_night_stalker', 88: 'npc_dota_hero_nyx_assassin', 76: 'npc_dota_hero_obsidian_destroyer',
          84: 'npc_dota_hero_ogre_magi', 57: 'npc_dota_hero_omniknight', 44: 'npc_dota_hero_phantom_assassin',
          12: 'npc_dota_hero_phantom_lancer', 13: 'npc_dota_hero_puck', 14: 'npc_dota_hero_pudge',
          45: 'npc_dota_hero_pugna', 39: 'npc_dota_hero_queenofpain', 51: 'npc_dota_hero_rattletrap',
          15: 'npc_dota_hero_razor', 32: 'npc_dota_hero_riki', 86: 'npc_dota_hero_rubick',
          16: 'npc_dota_hero_sand_king', 79: 'npc_dota_hero_shadow_demon', 27: 'npc_dota_hero_shadow_shaman',
          98: 'npc_dota_hero_shredder', 75: 'npc_dota_hero_silencer', 42: 'npc_dota_hero_skeleton_king',
          101: 'npc_dota_hero_skywrath_mage', 28: 'npc_dota_hero_slardar', 93: 'npc_dota_hero_slark',
          35: 'npc_dota_hero_sniper', 67: 'npc_dota_hero_spectre', 71: 'npc_dota_hero_spirit_breaker',
          17: 'npc_dota_hero_storm_spirit', 18: 'npc_dota_hero_sven', 46: 'npc_dota_hero_templar_assassin',
          29: 'npc_dota_hero_tidehunter', 34: 'npc_dota_hero_tinker', 19: 'npc_dota_hero_tiny',
          83: 'npc_dota_hero_treant', 95: 'npc_dota_hero_troll_warlord', 100: 'npc_dota_hero_tusk',
          85: 'npc_dota_hero_undying', 70: 'npc_dota_hero_ursa', 20: 'npc_dota_hero_vengefulspirit',
          40: 'npc_dota_hero_venomancer', 47: 'npc_dota_hero_viper', 92: 'npc_dota_hero_visage',
          37: 'npc_dota_hero_warlock', 63: 'npc_dota_hero_weaver', 21: 'npc_dota_hero_windrunner',
          91: 'npc_dota_hero_wisp', 30: 'npc_dota_hero_witch_doctor', 22: 'npc_dota_hero_zuus'}

from skadi import demo as d


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

            for parent, parent_modifiers in modifiers.by_parent.iteritems():
                for mod_num, mod_dict in parent_modifiers.iteritems():
                    if mod_dict['name'] == 'modifier_pudge_meat_hook':
                        if not hooks:
                            hooks.append(dict(tick=tick, target=parent,
                                              target_index=world.find(parent)[('DT_DOTA_BaseNPC', 'm_iUnitNameIndex')],
                                              time=time / 60.0,
                                              pudge_pos=worldcoordfromcell(world.find(mod_dict['caster'])),
                                              target_pos=worldcoordfromcell(world.find(parent))))
                        elif tick - hooks[-1]['tick'] > 100:
                            hooks.append(dict(tick=tick, target=parent,
                                              target_index=world.find(parent)[('DT_DOTA_BaseNPC', 'm_iUnitNameIndex')],
                                              time=time / 60.0,
                                              pudge_pos=worldcoordfromcell(world.find(mod_dict['caster'])),
                                              target_pos=worldcoordfromcell(world.find(parent))))
                        else:
                            pass
    hooks = [hooks[i] for i in range(len(hooks)) if hooks[i]['target'] != 832840]
    return hooks


def hook_plotting(hooks):
    map_img = plt.imread('/Users/Andrew/Documents/Computer/Workspace/Skadi/minimap.jpg')
    fig, ax = plt.subplots(figsize=(10.25, 10.25))
    ax.set_position([0, 0, 1, 1])
    plt.imshow(map_img)
    fig.patch.set_facecolor('black')
    ax.patch.set_facecolor('black')
    ax.axis((0, 1024, 1024, 0))

    pudge_img = plt.imread('/Users/Andrew/Documents/Computer/Workspace/Skadi/Hero_Icons/npc_dota_hero_pudge.png')
    pudge_oi = ob.OffsetImage(pudge_img, zoom=0.75)

    for hook in hooks:

        px, py = imagecoordfromworld(hook['pudge_pos'][0], hook['pudge_pos'][1])
        tx, ty = imagecoordfromworld(hook['target_pos'][0], hook['target_pos'][1])

        ax.plot([px, tx], [py, ty], color='r', zorder=3, linewidth=5)
        pudge_ab = ob.AnnotationBbox(pudge_oi, (px, py))
        pudge_ab.patch.set_alpha(0)
        pudge_art = ax.add_artist(pudge_ab)
        pudge_art.set(zorder=4)

        try:
            hero_img_name = HEROID[hook['target_index']]
            target_img = plt.imread(
                '/Users/Andrew/Documents/Computer/Workspace/Skadi/Hero_Icons/{hero}.png'.format(hero=hero_img_name))
            target_oi = ob.OffsetImage(target_img, zoom=0.75)
            target_ab = ob.AnnotationBbox(target_oi, (tx, ty))
            target_ab.patch.set_alpha(0)
            target_art = ax.add_artist(target_ab)
            target_art.set(zorder=5)
        except KeyError:
            pass

    savefig('/Users/Andrew/Desktop/hooks.png', dpi=100)


def worldcoordfromcell(entity):
    cellwidth = 1 << entity[('DT_BaseEntity', 'm_cellbits')]
    x = ((entity[('DT_DOTA_BaseNPC', 'm_cellX')] * cellwidth) - MAX_COORD_INTEGER) + \
        entity[('DT_DOTA_BaseNPC', 'm_vecOrigin')][0]
    y = ((entity[('DT_DOTA_BaseNPC', 'm_cellY')] * cellwidth) - MAX_COORD_INTEGER) + \
        entity[('DT_DOTA_BaseNPC', 'm_vecOrigin')][1]

    return x, y


def imagecoordfromworld(x, y):
    return (8576.0 + x) * 0.0626 + -18.1885, (8192.0 - y) * 0.0630 + -11.6453


if __name__ == '__main__':
    hooks = main()
    hook_plotting(hooks)