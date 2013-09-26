import itertools
import os
import matplotlib.pyplot as plt
import matplotlib.offsetbox as ob
import numpy as np
import scipy.spatial as spatial
import matplotlib.patches as patches
from common import MINIMAP_PATH, HERO_ICONS_PATH, HEROID, DEMO_FILE_PATH, worldcoordfromcell, imagecoordfromworld
from skadi import demo as d

TURN_LEFT, TURN_RIGHT, TURN_NONE = (1, -1, 0)


def turn(p, q, r):
    return cmp((q[0] - p[0]) * (r[1] - p[1]) - (r[0] - p[0]) * (q[1] - p[1]), 0)


def _keep_left(hull, r):
    while len(hull) > 1 and turn(hull[-2], hull[-1], r) != TURN_LEFT:
        hull.pop()
    if not len(hull) or hull[-1] != r:
        hull.append(r)
    return hull


def convex_hull(points):
    """Returns points on convex hull of an array of points in CCW order."""
    points = sorted(points)
    l = reduce(_keep_left, points, [])
    u = reduce(_keep_left, reversed(points), [])
    return l.extend(u[i] for i in xrange(1, len(u) - 1)) or l


def main():
    game = d.construct(DEMO_FILE_PATH)

    hero_handles = []
    player_nums = [str(i).zfill(4) for i in range(10)]

    unit_ids = []
    rad_pos = []
    dire_pos = []

    for tick, user_messages, game_events, world, modifiers in itertools.islice(game.stream(tick=0), 0, None, 60):

        players_ehandle, players_state = world.find_by_dt('DT_DOTA_PlayerResource')
        rules_ehandle, rules_state = world.find_by_dt('DT_DOTAGamerulesProxy')

        if rules_state[('DT_DOTAGamerulesProxy', 'DT_DOTAGamerules.m_flGameStartTime')] != 0.0:

            if not hero_handles:
                for player_num in player_nums:
                    hero_handles.append(
                        players_state[('DT_DOTA_PlayerResource', 'm_hSelectedHero.{ID}'.format(ID=player_num))])

            temp_unit_ids = []
            temp_rad_pos = []
            temp_dire_pos = []

            for num, hero_handle in enumerate(hero_handles):
                hero = world.find(hero_handle)
                if hero[('DT_DOTA_BaseNPC', 'm_lifeState')] == 0:
                    if num <= 4:
                        dx, dy = worldcoordfromcell(hero)
                        x, y = imagecoordfromworld(dx, dy)
                        temp_rad_pos.append([x, y])
                        temp_unit_ids.append(hero[('DT_DOTA_BaseNPC', 'm_iUnitNameIndex')])
                    elif num >= 4:
                        dx, dy = worldcoordfromcell(hero)
                        x, y = imagecoordfromworld(dx, dy)
                        temp_dire_pos.append([x, y])
                        temp_unit_ids.append(hero[('DT_DOTA_BaseNPC', 'm_iUnitNameIndex')])

            if not (temp_unit_ids == [] and temp_rad_pos == [] and temp_dire_pos == []):
                unit_ids.append(temp_unit_ids)
                rad_pos.append(np.array(temp_rad_pos))
                dire_pos.append(np.array(temp_dire_pos))

    return unit_ids, rad_pos, dire_pos


def hull_plotting(unit_ids, rad_pos, dire_pos):
    for index in range(len(rad_pos)):
        fig, ax = plt.subplots(figsize=(10.25, 10.25))
        map_img = plt.imread(MINIMAP_PATH)
        ax.set_position([0, 0, 1, 1])
        plt.imshow(map_img)
        fig.patch.set_facecolor('black')
        ax.patch.set_facecolor('black')
        ax.axis((0, 1024, 1024, 0))

        for num, hero in enumerate(unit_ids[index]):
            hero_img_name = HEROID[hero]
            hero_img = plt.imread(
                os.path.abspath(os.path.join(HERO_ICONS_PATH, '{hero}.png'.format(hero=hero_img_name))))
            hero_oi = ob.OffsetImage(hero_img, zoom=0.75)
            if num < len(rad_pos[index]):
                hero_ab = ob.AnnotationBbox(hero_oi, (rad_pos[index][num, 0], rad_pos[index][num, 1]))
            else:
                hero_ab = ob.AnnotationBbox(hero_oi, (
                    dire_pos[index][num - len(rad_pos[index]), 0], dire_pos[index][num - len(rad_pos[index]), 1]))
            hero_ab.patch.set_alpha(0)
            hero_art = ax.add_artist(hero_ab)
            hero_art.set(zorder=5)

        if len(rad_pos[index]) >= 3:
            rad_hull = spatial.ConvexHull(rad_pos[index])
            rad_points = []
            for simplex in rad_hull.simplices:
                p1 = [rad_pos[index][simplex, 0][0], rad_pos[index][simplex, 1][0]]
                p2 = [rad_pos[index][simplex, 0][1], rad_pos[index][simplex, 1][1]]
                if p1 not in rad_points:
                    rad_points.append(p1)
                if p2 not in rad_points:
                    rad_points.append(p2)
            rad_points = convex_hull(rad_points)
            hull_poly = patches.Polygon(rad_points, fc='green', ec='green', alpha=0.4, lw=3)
            ax.add_artist(hull_poly)

        elif len(rad_pos[index]) == 2:
            plt.plot(rad_pos[index][:, 0], rad_pos[index][:, 1], 'g-', linewidth=3, alpha=0.4, zorder=3)

        if len(dire_pos[index]) >= 3:
            dire_hull = spatial.ConvexHull(dire_pos[index])
            dire_points = []
            for simplex in dire_hull.simplices:
                p1 = [dire_pos[index][simplex, 0][0], dire_pos[index][simplex, 1][0]]
                p2 = [dire_pos[index][simplex, 0][1], dire_pos[index][simplex, 1][1]]
                if p1 not in dire_points:
                    dire_points.append(p1)
                if p2 not in dire_points:
                    dire_points.append(p2)
            dire_points = convex_hull(dire_points)
            hull_poly = patches.Polygon(dire_points, fc='red', ec='red', alpha=0.4, lw=3)
            ax.add_artist(hull_poly)

        elif len(dire_pos[index]) == 2:
            plt.plot(dire_pos[index][:, 0], dire_pos[index][:, 1], 'g-', linewidth=3, alpha=0.4, zorder=3)

        plt.show()


if __name__ == '__main__':
    unit_ids, rad_pos, dire_pos = main()
    hull_plotting(unit_ids, rad_pos, dire_pos)