# detailed_analysis.py  
from match_stats import player_wins, player_losses, WINNER_NAME, LOSER_NAME  
from typing import List, Dict, Any  
  
DATE_INDEX = 5  # Index for tourney_date  
SCORE_INDEX = 23  # Index for score  
  
def get_common_opponents(player_A: str, player_B: str) -> List[str]:  
    wins_A = set(match_result[LOSER_NAME] for match_result in player_wins(player_A))  
    losses_A = set(match_result[WINNER_NAME] for match_result in player_losses(player_A))  
    opponents_A = wins_A.union(losses_A)  
  
    wins_B = set(match_result[LOSER_NAME] for match_result in player_wins(player_B))  
    losses_B = set(match_result[WINNER_NAME] for match_result in player_losses(player_B))  
    opponents_B = wins_B.union(losses_B)  
  
    common_opponents = list(opponents_A.intersection(opponents_B))  
    return common_opponents  
  
def get_match_details(player_A: str, player_B: str, common_opponents: List[str]) -> List[Dict[str, Any]]:  
    details = []  
    for opponent in common_opponents:  
        # Retrieve matches for player A and B against each common opponent  
        matches_A = list(player_wins(player_A, opponent)) + list(player_losses(player_A, opponent))  
        matches_B = list(player_wins(player_B, opponent)) + list(player_losses(player_B, opponent))  
  
        # Details for Player A  
        for match_A in matches_A:  
            player_A_won = match_A[WINNER_NAME] == player_A  
            result_A = "won" if player_A_won else "lost"  
            detail_A = {  
                'player': player_A,  
                'opponent': opponent,  
                'date': match_A[DATE_INDEX],  
                'result': result_A,  
                'score': match_A[SCORE_INDEX],  
            }  
            details.append(detail_A)  
  
        # Details for Player B  
        for match_B in matches_B:  
            player_B_won = match_B[WINNER_NAME] == player_B  
            result_B = "won" if player_B_won else "lost"  
            detail_B = {  
                'player': player_B,  
                'opponent': opponent,  
                'date': match_B[DATE_INDEX],  
                'result': result_B,  
                'score': match_B[SCORE_INDEX],  
            }  
            details.append(detail_B)  
    return details  


def get_summary_statistics(player_A: str, player_B: str, common_opponents: List[str]) -> Dict[str, Any]:  
    summary = {  
        'total_games': 0,  
        'common_opponents': len(common_opponents),  
        'player_A_wins': 0,  
        'player_A_losses': 0,  
        'player_B_wins': 0,  
        'player_B_losses': 0,  
    }  
  
    for opponent in common_opponents:  
        matches_A = list(player_wins(player_A, opponent)) + list(player_losses(player_A, opponent))  
        matches_B = list(player_wins(player_B, opponent)) + list(player_losses(player_B, opponent))  
          
        summary['total_games'] += len(matches_A) + len(matches_B)  
        summary['player_A_wins'] += sum(1 for match in matches_A if match[WINNER_NAME] == player_A)  
        summary['player_A_losses'] += sum(1 for match in matches_A if match[LOSER_NAME] == player_A)  
        summary['player_B_wins'] += sum(1 for match in matches_B if match[WINNER_NAME] == player_B)  
        summary['player_B_losses'] += sum(1 for match in matches_B if match[LOSER_NAME] == player_B)  
  
    return summary  

  
def format_match_details(match_details: List[Dict[str, Any]]) -> str:  
    formatted_details = ""  
    for detail in match_details:  
        formatted_details += (  
            f"{detail['player']} {detail['result']} against {detail['opponent']} on {detail['date']}, score: {detail['score']}\n"  
        )  
    return formatted_details  
