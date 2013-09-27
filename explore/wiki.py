import os
import io
from collections import defaultdict


def wiki_scrape(demo):
    dt_set = defaultdict()

    stream = demo.stream(tick=5000)

    for i in range(len(stream.world.by_dt.keys())):
        dt = str(stream.world.by_dt.keys()[i])
        dt_set[dt] = set()
        __, state = stream.world.find_by_dt(dt)
        for j in range(len(state.keys())):
            prop = str(state.keys()[j])
            dt_set[dt].add(prop)

    return dt_set


def wiki_create(dt_set):
    base_path = '/Users/Andrew/Documents/Computer/Workspace/SkadiWiki'

    with io.open(os.path.join(base_path, 'Home.md'), 'ab+') as homefile:
        dtkeys = dt_set.keys().sort()
        for i in dtkeys:
            dt_name = str(dtkeys[i])
            dt_filename = ''.join([str(dtkeys[i]), '.md'])
            homefile.write(''.join(['* [', dt_name, '](https://github.com/garth5689/skadi/wiki/', dt_name, ') \n']))
            with io.open(os.path.join(base_path, dt_filename), 'ab+') as dtfile:
                dtfile.write(''.join(['### Full list of ', dt_name, ' properties \n\n']))
                propkeys = dt_set[dt_set.keys()[i]].sort()
                for __ in range(len(propkeys)):
                    dtfile.write(''.join(['* `', str(propkeys.pop()).replace("u'", "'"), '`: \n']))
