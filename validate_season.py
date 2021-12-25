import os
import json


LAST_SEASON0 = 15

SERIES_GPD = {"LCS": 2, "RCS": 1}

ABBR_TO_NAME = {
    "LCS": "League Championship Series",
    "RCS": "Rainbow Cup",
}


for iseason in range(LAST_SEASON0 + 1):
    seasondir = "season%d" % (iseason)

    #####################
    # load team data

    teamsfile = os.path.join(seasondir, "teams.json")

    print("***************************")
    print(f"Now checking {teamsfile}")

    if not os.path.exists(teamsfile):
        raise Exception(f"Error: missing file: {teamsfile}")

    with open(teamsfile, "r") as f:
        teams = json.load(f)

    teams_team_names = sorted([j["teamName"] for j in teams])

    # -----------
    # team function defs

    def get_team_color(teamName):
        for team in teams:
            if team["teamName"] == teamName:
                return team["teamColor"]
        raise Exception(f"Error: could not find a color for team {teamName}")

    def get_team_league(teamName):
        for team in teams:
            if team["teamName"] == teamName:
                return team["league"]
        raise Exception(f"Error: could not find a league for team {teamName}")

    #####################
    # check games

    # -----------
    # game function defs

    def check_id(game):
        if "gameid" not in game:
            raise Exception(f"Error: missing game id from game {game}")

    def check_name_color_match(game):
        """For a given game ensure the team name matches the team color"""
        for i in range(4):
            name_key = f"team{i+1}Name"
            name_val = game[name_key]

            color_key = f"team{i+1}Color"
            color_val = game[color_key]

            if color_val != get_team_color(name_val):
                err = f"Error in game {game['gameid']} of season {game['season']} day {game['day']}:\n"
                err += f"Team {i+1} {name_val} had specified team color {color_val}\n"
                err += f"Does not match get_team_color({name_val}) = {get_team_color(name_val)}"
                raise Exception(err)

    def check_score(game):
        pass

    def check_generations(game):
        gens = game["generations"]
        if gens < 500:
            raise Exception(
                f"Error in game {game['gameid']} of season {game['season']} day {game['day']}: game is too short (< 500 generations)!"
            )

    def check_league(game):
        league = game["league"]
        for i in range(4):
            name_key = f"team{i+1}Name"
            name_val = game[name_key]

            lea_val = get_team_league(name_val)
            if lea_val != league:
                err = f"Error in game {game['gameid']} of season {game['season']} day {game['day']}: "
                err += "league information does not match: {name_val}: {league} should be {lea_val}"
                raise Exception(err)

    def check_id(game):
        if "gameid" not in game.keys():
            print(game)
            raise Exception(
                f"Error in game of season {game['season']} day {game['day']}: no id found"
            )

    def check_pattern(game):
        if "patternName" not in game.keys():
            raise Exception(
                f"Error in game {game['gameid']} of season {game['season']} day {game['day']}: game is missing required key patternName"
            )

    def check_map(game):
        if "map" not in game.keys():
            raise Exception(
                f"Error in game {game['gameid']} of season {game['season']} day {game['day']}: game is missing required key patternName"
            )
        mapp = game["map"]
        # required keys that must be present
        req_keys = [
            "mapName",
            "mapZone1Name",
            "mapZone2Name",
            "mapZone3Name",
            "mapZone4Name",
            "initialConditions1",
            "initialConditions2",
            "initialConditions3",
            "initialConditions4",
            "rows",
            "columns",
            "cellSize",
            "patternName",
        ]
        # unused keys that should not be present
        unreq_keys = ["url", "patternId"]

        for rk in req_keys:
            if rk not in mapp:
                raise Exception(
                    f"Error in game {game['gameid']} of season {game['season']} day {game['day']}: game map is missing key \"{rk}\"!"
                )
        # for urk in unreq_keys:
        #    if urk in mapp:
        #        raise Exception("Error in game {game['gameid']} of season {game['season']} day {game['day']}: game map should not have key \"{urk}\"!")

    def check_w23l(game):
        req_keys = []
        for i in range(4):
            key = f"team{i+1}W23L"
            req_keys.append(key)
        for rk in req_keys:
            if rk not in game:
                raise Exception(
                    f"Error in game {game['gameid']} of season {game['season']} day {game['day']}: game map is missing key \"{rk}\"!"
                )
            summ = sum(game[rk])
            if summ != game['day']:
                print(game)
                raise Exception(
                    f"Error in game {game['gameid']} of season {game['season']} day {game['day']}: win loss record for team {i+1} sums to {summ}, should sum to {game['day']}"
                )

    def check_sw23l(game, iseriesday):
        req_keys = []
        for i in range(4):
            key = f"team{i+1}SeriesW23L"
            req_keys.append(key)
        for rk in req_keys:
            if rk not in game:
                raise Exception(
                    f"Error in game {game['gameid']} of season {game['season']} day {game['day']}: game map is missing key \"{rk}\"!"
                )
            summ = sum(game[rk])
            if summ != iseriesday:
                print(game)
                raise Exception(
                    f"Error in game {game['gameid']} of season {game['season']} day {game['day']}: win loss record for team {i+1} sums to {summ}, should sum to {iseriesday}"
                )

    def check_game_season(game, correct_season):
        if iseason != game["season"]:
            raise Exception(
                f"Error in game {game['gameid']} of season {game['season']} day {game['day']}: season should be {correct_season}"
            )

    def check_season_day(day):
        if len(day) != len(teams) // 4:
            raise Exception(
                f"Error: day {day[0]['day']} has length {len(day)} but should have length {len(teams)//4}"
            )

    def check_bracket_day(day, series, iday):
        series_gpd = SERIES_GPD
        if series not in series_gpd:
            raise Exception(
                f"Error: series name {series} not in {', '.join(series_gpd.keys())}"
            )
        if iday <= 2 and len(day) != series_gpd[series]:
            raise Exception(
                f"Error: bracket for series {series} has incorrect number of games ({len(day)}, should be {series_gpd[series]})"
            )

    def check_postseason_game_descr(game, series_name):
        if series_name not in game["description"]:
            err = f"Error: series name {series_name} not found in game description {game['description']}"
            raise Exception(err)


    # -----------
    # check seed table

    def repair_seed_table_order(season, seed, seedfile):
        rainbow_values = [11, 7, 3, 0]
        f_rainbows = lambda x: 11*x[0] + 7*x[1] + 3*x[2]
        nteams = 4
        last_day = season[-1]

        new_seed = {}
        for league in seed:

            rainbows = {}
            points = {}
            # accumulate points and rainbows from last game
            for game in last_day:

                if game['league'] != league:
                    continue

                for i in range(nteams):

                    name_key = f"team{i+1}Name"
                    name_val = game[name_key]

                    w23l_key = f"team{i+1}W23L"
                    w23l_val = game[w23l_key]

                    rank_key = f"team{i+1}Rank"
                    rank_val = game[rank_key]

                    tp_key = f"team{i+1}TotalPoints"
                    tp_val = game[tp_key]

                    score_key = f"team{i+1}Score"
                    score_val = game[score_key]

                    nrainbows = f_rainbows(w23l_val)
                    nrainbows += rainbow_values[rank_val]

                    rainbows[name_val] = nrainbows

                    npoints = tp_val
                    npoints += score_val

                    points[name_val] = npoints

            tups = []
            for team in points.keys():
                tups.append((team, rainbows[team], points[team]))
            tups.sort(key = lambda x: (100000-x[1], 100000-x[2]))

            new_seed_table = []
            for i in range(4):
                new_seed_table.append(tups[i][0])
            new_seed[league] = new_seed_table
        
        # Repair the seed table
        with open(seedfile, 'w') as f:
            json.dump(new_seed, f, indent=4)

    # -----------
    # schedule

    schedfile = os.path.join(seasondir, "schedule.json")

    print("***************************")
    print(f"Now checking {schedfile}")

    if not os.path.exists(schedfile):
        raise Exception(f"Error: missing file: {schedfile}")

    with open(schedfile, "r") as f:
        sched = json.load(f)

    sched_team_names = set()
    sched_game_ids = set()
    for iday, day in enumerate(sched):
        check_season_day(day)
        games = day
        for igame, game in enumerate(games):
            check_id(game)
            check_name_color_match(game)
            check_league(game)
            check_pattern(game)
            check_game_season(game, iseason)

            for i in range(4):
                key = f"team{i+1}Name"
                val = game[key]
                sched_team_names.add(val)

            if game["gameid"] in sched_game_ids:
                raise Exception(
                    f"Error: game id {game['gameid']} is a duplicate in the schedule!"
                )
            else:
                sched_game_ids.add(game["gameid"])

    # schedule.json and teams.json must have the same number of teams
    if len(sched_team_names) != len(teams):
        raise Exception(
            f"Error: number of teams found in schedule was {len(sched_team_names)}, number of teams is {len(teams)}"
        )

    # schedule.json and teams.json must have exactly the same team names
    diff1 = set(sched_team_names) - set(teams_team_names)
    diff2 = set(teams_team_names) - set(sched_team_names)
    if len(diff1) > 0 or len(diff2) > 0:
        err = "Error: mismatch in teams.json and schedule.json team names:\n"
        err += f"schedule.json team names: {', '.join(sched_team_names)}\n"
        err += f"teams.json team names: {', '.join(teams_team_names)}\n"
        raise Exception(err)

    for team in teams:
        if team["teamName"] not in sched_team_names:
            raise Exception(
                f"Error: team name {team['teamName']} not found in schedule.json"
            )

    # -----------
    # season

    seasonfile = os.path.join(seasondir, "season.json")

    print("***************************")
    print(f"Now checking {seasonfile}")

    if not os.path.exists(seasonfile):
        raise Exception(f"Error: missing file: {seasonfile}")

    with open(seasonfile, "r") as f:
        season = json.load(f)

    season_team_names = set()
    season_game_ids = set()
    for iday, day in enumerate(season):
        check_season_day(day)
        games = day
        for igame, game in enumerate(games):
            check_id(game)
            check_name_color_match(game)
            check_score(game)
            check_generations(game)
            check_league(game)
            check_id(game)
            check_map(game)
            check_w23l(game)
            check_game_season(game, iseason)

            for i in range(4):
                key = f"team{i+1}Name"
                val = game[key]
                season_team_names.add(val)

            if game['gameid'] in season_game_ids:
                raise Exception(
                    f"Error: game id {game['gameid']} is a duplicate in the season!"
                )
            else:
                season_game_ids.add(game['gameid'])

    # season.json and teams.json must have the same number of teams
    if len(season_team_names) != len(teams):
        raise Exception(
            f"Error: number of teams found in season was {len(season_team_names)}, number of teams is {len(teams)}"
        )

    # season.json and teams.json must have exactly the same team names
    diff1 = set(season_team_names) - set(teams_team_names)
    diff2 = set(teams_team_names) - set(season_team_names)
    if len(diff1) > 0 or len(diff2) > 0:
        err = "Error: mismatch in teams.json and season.json team names:\n"
        err += f"season.json team names: {', '.join(season_team_names)}\n"
        err += f"teams.json team names: {', '.join(teams_team_names)}\n"
        raise Exception(err)

    for team in teams:
        if team["teamName"] not in season_team_names:
            raise Exception(
                f"Error: team name {team['teamName']} not found in season.json"
            )

    # season.json and schedule.json must have exactly the same game ids
    diff3 = season_game_ids - sched_game_ids
    diff4 = sched_game_ids - season_game_ids
    if len(diff3)>0 or len(diff4)>0:
        err = "Error: mismatch in game IDs between schedule and season:\n"
        if len(diff3)>0:
            for gameid in sorted(list(diff3)):
                err += f" - {gameid}\n"
        if len(diff4)>0:
            for gameid in sorted(list(diff4)):
                err += f" - {gameid}\n"
        raise Exception(err)

    # -----------
    # seed
    seedfile = os.path.join(seasondir, "seed.json")

    print("***************************")
    print(f"Now checking {seedfile}")

    if not os.path.exists(seedfile):
        raise Exception(f"Error: missing file: {seedfile}")

    with open(seedfile, "r") as f:
        seed = json.load(f)

    seed_team_names = set()
    for league in seed:
        seed_list = seed[league]
        if len(seed_list) != 4:
            raise Exception(
                f"Error: seed list for {league} is {len(seed_list)}, should be 4"
            )
        for t in seed_list:
            seed_team_names.add(t)

    # seed.json must have fewer teams than teams.json
    if len(seed_team_names) >= len(teams):
        raise Exception(
            f"Error: seed.json has too many teams: {len(seed_team_names)} should be <= {len(teams)}"
        )

    # seed.json teams must be a subset of teams.json teams
    if not set(seed_team_names).issubset(teams_team_names):
        err = "Error: mismatch in teams.json and seed.json team names:\n"
        err += f"seed.json team names: {', '.join(seed_team_names)}\n"
        err += f"teams.json team names: {', '.join(teams_team_names)}\n"
        raise Exception(err)

    # Check that seed table is in the correct order
    # (Most rainbows, then most runs as tiebreaker)
    repair_seed_table_order(season, seed, seedfile)

    # -----------
    # bracket
    bracketfile = os.path.join(seasondir, "bracket.json")

    print("***************************")
    print(f"Now checking {bracketfile}")

    if not os.path.exists(bracketfile):
        raise Exception(f"Error: missing file: {bracketfile}")

    with open(bracketfile, "r") as f:
        bracket = json.load(f)

    bracket_team_names = set()
    bracket_game_ids = set()
    for series in bracket:
        miniseason = bracket[series]
        for iday, day in enumerate(miniseason):
            check_bracket_day(day, series, iday)
            for game in day:
                bracket_team_names.add(game["team1Name"])
                bracket_team_names.add(game["team2Name"])
                if game['gameid'] in bracket_game_ids:
                    raise Exception(
                        f"Error: game id {game['gameid']} is a duplicate in the bracket!"
                    )
                else:
                    bracket_game_ids.add(game['gameid'])

    # Verify series are the correct lengths
    lcslen = len(bracket["LCS"])
    if lcslen != 9:
        raise Exception(
            f"Error: postseason LCS length is invalid: {lcslen} games, should be 9"
        )

    rcslen = len(bracket["RCS"])
    if rcslen != 9:
        raise Exception(
            f"Error: postseason RCS length is invalid: {rcslen} games, should be 9"
        )

    # bracket.json must have fewer teams than teams.json
    if len(bracket_team_names) >= len(teams):
        raise Exception(
            f"Error: bracket.json has too many teams: {len(bracket_team_names)} should be <= {len(teams)}"
        )

    ## bracket.json teams must be a subset of teams.json teams
    #ignore_list = ["Top Seed", "Bottom Seed", "Cold League", "Hot League"]
    #ignore_list = set(ignore_list)
    #bracket_team_names = bracket_team_names - ignore_list

    #if not set(bracket_team_names).issubset(set(teams_team_names)):
    #    err = "Error: mismatch in teams.json and bracket.json team names:\n"
    #    err += f"bracket.json team names: {', '.join(sorted(bracket_team_names))}\n"
    #    err += f"teams.json team names: {', '.join(sorted(teams_team_names))}\n"
    #    err += f"Missing from teams: {', '.join(sorted(set(bracket_team_names) - set(teams_team_names)))}"
    #    raise Exception(err)

    # -----------
    # postseason

    postseasonfile = os.path.join(seasondir, "postseason.json")

    print("***************************")
    print(f"Now checking {postseasonfile}")

    if not os.path.exists(postseasonfile):
        raise Exception(f"Error: missing file: {postseasonfile}")

    with open(postseasonfile, "r") as f:
        postseason = json.load(f)

    postseason_team_names = set()
    postseason_game_ids = set()
    for series in postseason:
        miniseason = postseason[series]
        for iseriesday, day in enumerate(miniseason):
            games = day
            for igame, game in enumerate(games):
                check_id(game)
                check_name_color_match(game)
                check_score(game)
                if series != "RCS":
                    check_league(game)
                check_map(game)
                check_sw23l(game, iseriesday)
                check_game_season(game, iseason)

                for i in range(4):
                    key = f"team{i+1}Name"
                    val = game[key]
                    sched_team_names.add(val)

                if game['gameid'] in postseason_game_ids:
                    raise Exception(
                        f"Error: game id {game['gameid']} is a duplicate in the postseason!"
                    )
                else:
                    postseason_game_ids.add(game['gameid'])

    for abbr, series_name in ABBR_TO_NAME.items():
        miniseason = postseason[abbr]
        for day in miniseason:
            for game in day:
                check_postseason_game_descr(game, series_name)

    team_names = set()
    for team in teams:
        team_names.add(team["teamName"])
    for postseason_team_name in postseason_team_names:
        if postseason_team_name not in team_names:
            raise Exception(
                f"Error: invalid team name {postseason_team_name} found in postseason.json"
            )

    # Verify series are the correct lengths
    lcslen = len(postseason["LCS"])
    if lcslen != 9:
        raise Exception(f"Error: postseason LCS length is invalid: {lcslen} games, should be 9")

    rcslen = len(postseason["RCS"])
    if rcslen != 9:
        raise Exception(f"Error: postseason RCS length is invalid: {rcslen} games, should be 9")

    # postseason.json must have fewer teams than teams.json
    if len(postseason_team_names) >= len(teams):
        raise Exception(
            f"Error: postseason.json has too many teams: {len(postseason_team_names)} should be <= {len(teams)}"
        )

    # Check if either choke artist was in the RCS
    one_day = postseason['RCS'][0]
    one_game = one_day[0]
    for i in range(4):
        abbr_key = f"team{i+1}Abbr"
        abbr_val = one_game[abbr_key]
        if abbr_val in ["BPT", "DET"]:
            print("")
            print("")
            print("@"*40)
            print("@"*40)
            print(f"SEASON0 = {iseason}:")
            print(f"{abbr_val} CHOKE ARTISTS REACHED THE RAINBOW CUP")
            print("@"*40)
            print("@"*40)
            print("")
            print("")





print("***************************")
print("Everything is okay")
