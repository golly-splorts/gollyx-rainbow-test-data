import random
import os
import json

for season0 in [0, 1, 2, 3, 4, 5]:
    seasfile = f"season{season0}/season.json"
    seedfile = f"season{season0}/seed.json"

    with open(seasfile, "r") as f:
        seas = json.load(f)

    with open(seedfile, "r") as f:
        seed = json.load(f)

    leagues = ['Unwest League', 'West League']

    new_seed_table = {}

    # Assemble a new seed table
    last_day = seas[-1]
    for league in leagues:
        league_tup = []
        for game in last_day:
            if game['league'] == league:
                for i in range(4):
                    # name
                    name_key = f"team{i+1}Name"
                    name_val = game[name_key]

                    # abbr
                    abbr_key = f"team{i+1}Abbr"
                    abbr_val = game[abbr_key]

                    # w23l record on next to last day
                    w23l_key = f"team{i+1}W23L"
                    w23l_val = game[w23l_key]

                    # total points on next to last day
                    tp_key = f"team{i+1}TotalPoints"
                    tp_val = game[tp_key]

                    # team rank for last day
                    rank_key = f"team{i+1}Rank"
                    rank_val = game[rank_key]

                    # team points for last day
                    pts_key = f"team{i+1}Score"
                    pts_val = game[pts_key]

                    # update w23l
                    t = w23l_val
                    t[rank_val] += 1
                    w23l_val = t

                    # turn w23l into rainbows
                    rainbows = 11 * w23l_val[0] + 7 * w23l_val[1] + 3 * w23l_val[2]

                    # update total points
                    points = tp_val + pts_val

                    league_tup.append((name_val, rainbows, points, random.randint(1, 100)))

        league_tup.sort(key=lambda x: (x[1], x[2], x[3]), reverse=True)
        league_seed_table = [s[0] for s in league_tup]
        league_seed_table = league_seed_table[:4]
        new_seed_table[league] = league_seed_table

    print(new_seed_table)
    with open(f'season{season0}/seed.json', 'w') as f:
        json.dump(new_seed_table, f, indent=4)
