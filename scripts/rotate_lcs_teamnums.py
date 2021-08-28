import json
from pprint import pprint


def main():
    for season0 in range(6):
        pjs = f'season{season0}/postseason.json'
        with open(pjs, 'r') as f:
            post = json.load(f)
    
        miniseason = post['LCS']
        new_miniseason = []
        for i, day in enumerate(miniseason):
            new_day = []
            for game in day:
                new_game = rotate_team_ix(game, i)
                new_day.append(new_game)
            new_miniseason.append(new_day)

        post['LCS'] = new_miniseason

        with open(pjs, 'w') as f:
            json.dump(post, f, indent=4)

def rotate_team_ix(game, i):
    if i%4 == 0:
        return game

    tupmap = []
    for j in range(4):
        k = (j + i)%4
        tupmap.append((j,k))

    labels = ["Name", "Abbr", "Score", "Rank", "Color", "SeriesW23L", "SeriesTotalPoints"]
    
    # First pass: copy old j to new k
    for j, k in tupmap:
        for lab in labels:
            oldlab = f"team{j+1}{lab}"
            newlab = f"new_team{k+1}{lab}"
            game[newlab] = game[oldlab]
        
        oldiclab = f"initialConditions{j+1}"
        newiclab = f"new_initialConditions{k+1}"
        game['map'][newiclab] = game['map'][oldiclab]

    # Second pass: copy new k to k
    for j, k in tupmap:
        for lab in labels:
            oldlab = f"new_team{k+1}{lab}"
            newlab = f"team{k+1}{lab}"
            game[newlab] = game[oldlab]

        oldiclab = f"new_initialConditions{k+1}"
        newiclab = f"initialConditions{k+1}"
        game['map'][newiclab] = game['map'][oldiclab]

    # Third pass: remove the new_ labels
    for j, k in tupmap:
        for lab in labels:
            newlab = f"new_team{k+1}{lab}"
            del game[newlab]

        newiclab = f"new_initialConditions{k+1}"
        del game['map'][newiclab]

    return game


if __name__=="__main__":
    main()
