# match_stats.py
import csv
from dataclasses import dataclass

import os
from collections import Counter
from datetime import datetime
from typing import List, Optional, Tuple

import requests as requests

WINNER_NAME = 10
LOSER_NAME = 18

WINNER_STATS_START = 27
WINNER_STATS_END = 32
LOSER_STATS_START = 36
LOSER_STATS_END = 41

# This is a global variable that will store the match results
match_results = []


@dataclass
class Stats:
    aces: int
    double_faults: int
    service_points: int
    first_in: int
    first_won: int
    second_won: int
    adv_aces: int
    adv_double_faults: int
    adv_service_points: int
    adv_first_in: int
    adv_first_won: int
    adv_second_won: int


class NoAdversaryMatches(Exception):
    pass


def results_filepath(url: str):
    tournament, _, year = url.split("/")[-1].split("_")
    return f"{tournament}/{year}"


def download_match_results(url: str, verbosity: int = 0):
    if verbosity >= 1:
        print(f"Downloading {url}")
    request = requests.get(url)
    output_file = results_filepath(url)
    output_directory = "".join(output_file.split("/")[:-1])
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    open(output_file, "wb").write(request.content)
    reader = csv.reader(request.content.decode("utf-8").splitlines(), delimiter=",")
    next(reader)
    return reader


def load_match_results(results_file_path: str):
    if os.path.exists(results_file_path):
        results_file = open(results_file_path)
        next(results_file)
        match_results = [row for row in csv.reader(results_file)]
    else:
        raise FileNotFoundError
    return match_results


def filter_match_results(match_results):
    # exclude incomplete/unplayed matches (e.g. "W/O" or "RET" in score]
    match_results = [k for k in match_results if "W" not in k[23] and "R" not in k[23]]
    # exclude matches without stats
    match_results = [k for k in match_results if "" not in [k[27], k[36]]]
    return match_results


def list_players(match_min: int = 0) -> List[str]:
    ## make list of all players with a result
    players = [k[10] for k in match_results] + [k[18] for k in match_results]
    ## limit list of players to those with at least match_min match_results
    players = [k for k, v in Counter(players).items() if v >= match_min]
    return players


def player_wins(player_name: str, adversary_name: Optional[str] = None):
    if adversary_name:
        wins = filter(
            lambda match_result: adversary_name == match_result[LOSER_NAME],
            match_results,
        )
    else:
        wins = match_results
    return filter(lambda match_result: player_name == match_result[WINNER_NAME], wins)


def player_losses(player_name: str, adversary_name: Optional[str] = None):
    if adversary_name:
        losses = filter(
            lambda match_result: adversary_name == match_result[WINNER_NAME],
            match_results,
        )
    else:
        losses = match_results
    return filter(lambda match_result: player_name == match_result[LOSER_NAME], losses)


def player_aggregate_stats(player_name: str, adversary_name: Optional[str]):
    player_stats = [
        player_match[WINNER_STATS_START : WINNER_STATS_END + 1]
        + player_match[LOSER_STATS_START : LOSER_STATS_END + 1]
        for player_match in player_wins(player_name, adversary_name)
    ]
    player_stats.extend(
        [
            player_match[LOSER_STATS_START : LOSER_STATS_END + 1]
            + player_match[WINNER_STATS_START : WINNER_STATS_END + 1]
            for player_match in player_losses(player_name, adversary_name)
        ]
    )

    if len(player_stats) == 0:
        raise NoAdversaryMatches

    aggregate_player_stats = []
    for stat_column in zip(*player_stats):
        aggregate_player_stats.append(sum([int(s) for s in stat_column if s.isdigit()]))

    return Stats(*aggregate_player_stats)


def spw(player: str, adversary: str):
    stats = player_aggregate_stats(player, adversary)
    return (stats.first_won + stats.second_won) / float(stats.service_points)


def rpw(player: str, adversary: str):
    stats = player_aggregate_stats(player, adversary)
    return (
        stats.adv_service_points - stats.adv_first_won - stats.adv_second_won
    ) / float(stats.adv_service_points)


def Delta_i_AB(player_A: str, player_B: str, common_adversary: str):
    return (spw(player_A, common_adversary) - (1 - rpw(player_A, common_adversary))) - (
        spw(player_B, common_adversary) - (1 - rpw(player_B, common_adversary))
    )


def prepare_match_results(year_range: Tuple[int, int], gender: str, verbosity: int = 0):  
    results = []  
  
    if gender == "men":  
        base_url = "https://raw.githubusercontent.com/1NoobDev/tennis_atp/master/atp_matches_"  
    elif gender == "women":  
        base_url = "https://raw.githubusercontent.com/1NoobDev/tennis_wta/master/wta_matches_"  
    else:  
        raise ValueError("Gender must be one of either 'men' or 'women'")  
  
    for year in range(year_range[0], year_range[1] + 1):  
        year_url = f"{base_url}{year}.csv"  
        year_filename = results_filepath(year_url)  
        current_year = datetime.now().year  # Get the current year  
  
        # If the year is the current year or the file does not exist, download the results  
        if year == current_year or not os.path.exists(year_filename):  
            try:  
                results.extend(download_match_results(year_url, verbosity))  
            except Exception as e:  
                if verbosity >= 1:  
                    print(f"Could not download the file for year {year}: {e}")  
        else:  
            try:  
                results.extend(load_match_results(year_filename))  
            except FileNotFoundError as e:  
                if verbosity >= 1:  
                    print(f"File not found: {year_filename} - {str(e)}")  
  
    global match_results  
    match_results = filter_match_results(results)  
