import argparse

from malleys import M3, M5
from match_stats import (
    prepare_match_results,
    list_players,
    Delta_i_AB,
    NoAdversaryMatches,
)


def P_ABC(player_A, player_B, common_adversary, matches):
    if matches == 3:
        return (
            M3(0.6 + Delta_i_AB(player_A, player_B, common_adversary), (1 - 0.6))
            + M3(0.6, (1 - (0.6 - Delta_i_AB(player_A, player_B, common_adversary))))
        ) / 2
    elif matches == 5:
        return (
            M5(0.6 + Delta_i_AB(player_A, player_B, common_adversary), (1 - 0.6))
            + M5(0.6, (1 - (0.6 - Delta_i_AB(player_A, player_B, common_adversary))))
        ) / 2


def P(player_A: str, player_B: str, gender: str, verbosity=0):
    players = list_players()
    players.remove(player_A)
    players.remove(player_B)

    if gender == "men":
        num_matches = 5
    elif gender == "women":
        num_matches = 3
    else:
        raise IndexError

    sum = 0
    i = 0
    common_players = 0
    for common_adversary in players:
        i += 1
        if verbosity >= 1 and (i % 10 == 0):
            print(f"processed {i} of {len(players)} potential common adversaries")
        try:
            pABC = P_ABC(player_A, player_B, common_adversary, num_matches)
            sum += pABC
            if verbosity >= 2:
                print(
                    f"Probability of {player_A} beating {player_B} via {common_adversary}: {pABC};"
                )
            common_players += 1
        except NoAdversaryMatches:
            pass

    result = sum / common_players
    print(f"The probability of {player_A} beating {player_B} is {result}")

    odd_a = 1 / result
    odd_b = 1 / (1 - result)
    print(f"Real odds for {player_A} winning: " + str(odd_a))
    print(f"Real odds for {player_B} winning: " + str(odd_b))
    return result


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "gender",
        choices=("men", "women"),
        help="Specify gender of players so as to select from atp or wta statistics",
    )
    parser.add_argument(
        "player_A",
        help="Name of player whose probability of winning is to be calculated [e.g. Roger Federer]",
    )
    parser.add_argument(
        "player_B", help="Name of player which is to be beaten [e.g. Novak Djokovic]"
    )
    parser.add_argument(
        "--years",
        type=int,
        default=[2021, 2022],
        nargs=2,
        help="Range of years for which to consider statistics",
    )
    parser.add_argument(
        "-v", "--verbosity", action="count", default=0, help="increase output verbosity"
    )
    args = parser.parse_args()

    prepare_match_results(args.years, args.gender, args.verbosity)
    P(args.player_A, args.player_B, args.gender, args.verbosity)


if __name__ == "__main__":
    main()
