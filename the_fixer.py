import json
import os
import copy


WHICH_SEASON0 = 11


def main():
    nteams = 4

    loser_abbrs = ['BPT', 'DET']

    postseason_json_file = os.path.join(f'season{WHICH_SEASON0}', 'postseason.json')
    if not os.path.exists(postseason_json_file):
        raise Exception(f"Error: could not find json file: {postseason_json_file}")

    new_postseason_json_file = os.path.join(f'season{WHICH_SEASON0}', 'new_postseason.json')

    with open(postseason_json_file, 'r') as f:
        post = json.load(f)

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

                lcs_tup.append((abbr_val, name_val, nrainbows, tp_val))

    lcs_tup.sort(key = lambda x: (1000000-x[2], 1000000-x[3]))

    if lcs_tup[0][0] in loser_abbrs:

        choke_abbr = lcs_tup[0][0]

        print(f"Choke artists clinched a pennant: {choke_abbr}")
        print(f"Repairing {postseason_json_file}...")

        # Figure out who to swap the choke artist with
        swap_with_abbr = lcs_tup[3][0]
        if swap_with_abbr in loser_abbrs:
            swap_with_abbr = lcs_tup[2][0]

        # Iterate through existing LCS,
        # copy games into new LCS,
        # filtering as we go
        new_lcs = []

        
        for day in post['LCS']:
            new_day = []
            for game in day:
                if 'Unleague' not in game['league']:
                    new_day.append(game)
                else:
                    # Filter game
                    new_game = filter_game(game, choke_abbr, swap_with_abbr)
                    new_day.append(new_game)

            new_lcs.append(new_day)

        post['LCS'] = new_lcs

        with open(postseason_json_file, 'w') as f:
            json.dump(post, f)

        print(f"Done repairing {postseason_json_file}.")



def filter_game(game, choke_abbr, swap_with_abbr):
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
    # Leave aloen labels that set performance.
    swap_labels_suffixes = [
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
