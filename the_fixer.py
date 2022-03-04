import json
import os
import copy


def main():
    for which in [18]:
        fix_season(which)


def fix_season(which_season0):

    print(f"\nthe_fixer is now checking {which_season0}...")

    nteams = 4

    loser_abbrs = ['BPT', 'DET']

    postseason_json_file = os.path.join(f'season{which_season0}', 'postseason.json')
    if not os.path.exists(postseason_json_file):
        raise Exception(f"Error: could not find json file: {postseason_json_file}")
    with open(postseason_json_file, 'r') as f:
        post = json.load(f)

    teams_json_file = os.path.join(f'season{which_season0}', 'teams.json')
    if not os.path.exists(teams_json_file):
        raise Exception(f"Error: could not find json file: {teams_json_file}")
    with open(teams_json_file, 'r') as f:
        teams = json.load(f)

    rainbow_values = [11, 7, 3, 0]

    # Start by getting sorted tuples (team, rainbows, points)
    lcs_tup = []
    last_day = post['LCS'][-1]
    for game in last_day:
        if 'Unwest' in game['league']:
            for i in range(nteams):
                name_key = f"team{i+1}Name"
                name_val = game[name_key]

                abbr_key = f"team{i+1}Abbr"
                abbr_val = game[abbr_key]

                w23l_key = f"team{i+1}SeriesW23L"
                w23l_val = game[w23l_key]
                nrainbows = 11*w23l_val[0] + 7*w23l_val[1] + 3*w23l_val[2]

                tp_key = f"team{i+1}SeriesTotalPoints"
                tp_val = game[tp_key]

                # update with outcome of last game

                rank_key = f"team{i+1}Rank"
                rank_val = game[rank_key]
                nrainbows += rainbow_values[rank_val]

                score_key = f"team{i+1}Score"
                score_val = game[score_key]
                tp_val += score_val

                lcs_tup.append((abbr_val, name_val, nrainbows, tp_val))

    lcs_tup.sort(key = lambda x: (1000000-x[2], 1000000-x[3]))

    if lcs_tup[0][0] in loser_abbrs or lcs_tup[1][0] in loser_abbrs:

        if lcs_tup[0][0] in loser_abbrs:
            print(" + Rank: 1")
            choke_abbr = lcs_tup[0][0]
            print(f"Choke artists clinched a pennant: {choke_abbr}")
        elif lcs_tup[1][0] in loser_abbrs:
            print(" + Rank: 2")
            choke_abbr = lcs_tup[1][0]
            print(f"Choke artists clinched a pennant: {choke_abbr}")

        print(f"Repairing {postseason_json_file}...")

        # Figure out who to swap the choke artist with
        swap_with_abbr = lcs_tup[3][0]
        if swap_with_abbr in loser_abbrs:
            swap_with_abbr = lcs_tup[2][0]

        # Iterate through entire postseason,
        # recreating structure,
        # filtering games as we go.
        new_post = {}

        new_lcs = []
        for day in post['LCS']:
            new_day = []
            for game in day:
                if 'Unwest' not in game['league']:
                    new_day.append(game)
                else:
                    # Filter game
                    new_game = filter_game_swap_abbrs(game, choke_abbr, swap_with_abbr)
                    new_day.append(new_game)

            new_lcs.append(new_day)

        new_post['LCS'] = new_lcs

        new_rcs = []
        for day in post['RCS']:
            new_day = []
            for game in day:
                new_game = filter_game_replace_abbrs(game, choke_abbr, swap_with_abbr, teams)
            new_rcs.append(new_day)

        new_post['RCS'] = new_rcs

        with open(postseason_json_file, 'w') as f:
            json.dump(post, f, indent=4)

        print(f"Done repairing {postseason_json_file}.")

    else:
        print("False alarm??")
        print("LCS outcomes, ranked:")
        from pprint import pprint
        pprint(lcs_tup)


def filter_game_replace_abbrs(game, choke_abbr, swap_with_abbr, teams):
    nteams = 4

    # Get a list of abbreviations in team ix order
    abbrs = []
    for i in range(nteams):
        abbr_key = f"team{i+1}Abbr"
        abbr_val = game[abbr_key]
        abbrs.append(abbr_val)

    iChoke = abbrs.index(choke_abbr)

    # Get the new name/abbr/color values
    for team in teams:
        if team['teamAbbr'] == swap_with_abbr:
            swap_name = team['teamName']
            swap_abbr = team['teamAbbr']
            swap_color = team['teamColor']

    # Replace name/abbr/color labels
    game[f"team{iChoke+1}Name"] = swap_name
    game[f"team{iChoke+1}Abbr"] = swap_abbr
    game[f"team{iChoke+1}Color"] = swap_color

    return game


def filter_game_swap_abbrs(game, choke_abbr, swap_with_abbr):
    nteams = 4

    # Get a list of abbreviations in team ix order
    abbrs = []
    for i in range(nteams):
        abbr_key = f"team{i+1}Abbr"
        abbr_val = game[abbr_key]
        abbrs.append(abbr_val)
    
    iChoke = abbrs.index(choke_abbr)
    iSwap = abbrs.index(swap_with_abbr)

    # Swap labels that are team identifiers,
    # Leave alone labels that set performance.
    swap_label_suffixes = [
        "Name",
        "Abbr",
        "Color",
    ]
    for swap_label_suffix in swap_label_suffixes:
        kchoke = f"team{iChoke+1}{swap_label_suffix}"
        kswap = f"team{iSwap+1}{swap_label_suffix}"

        temp = game[kchoke]
        game[kchoke] = game[kswap]
        game[kswap] = temp

    return game


if __name__=="__main__":
    main()
