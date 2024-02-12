import argparse

def process_round(ballots : dict, candidates : list, alpha : float, last_round : bool = False) -> dict:
    '''
    Main function to generate winner from given ballots and alpha (hyperparameter) value.
    Uses Condorcet winner criterion to calculate a matrix for each pair of candidates, but where the number of votes (points)
    is manipulated by the alpha value to enforce determinism.
    Ballot votes (individual voting power) is recalculated with recalculate_ballots() once a winner is determined, similar to STV.
    '''
    score = {candidate : 0 for candidate in candidates}
    print("ROUND START")
    # Continues to loop while a winner is not found
    while (len(candidates) - 1) not in score.values():
        print("Alpha: " + str(alpha))
        score = {candidate : 0 for candidate in candidates}
        pairs = [(candidate, candidate) for candidate in candidates]
        stop = False
        # Do Concorcet matrix calculations with distance
        for candidate in candidates:
            for opponent in candidates:
                # Check to verify that pair has not already done a head-to-head match
                if not stop and (candidate, opponent) not in pairs:
                    print(candidate + " vs " + opponent)
                    candidate_points, opponent_points = 0, 0
                    for ranking, votes in ballots.items():
                        if candidate not in ranking and opponent not in ranking:
                            # On absense of both candidate and opponent, ignore pair
                            continue
                        elif candidate in ranking and opponent not in ranking:
                            # On appearance of candidate but absense of opponent, give equivalent of distance 1-modified votes to candidate
                            candidate_points += votes * (1 + alpha)
                        elif candidate not in ranking and opponent in ranking:
                            # On apperance of opponent but absense of candidate, give equivalent of distance 1-modified votes to opponent
                            opponent_points += votes * (1 + alpha)
                        else:
                            # On appearance of both candidate and opponent, calculate distance in ranking between candidate and opponent
                            # General formula for distance-modified votes is votes * (1 + distance * alpha)
                            # For v = 10000, d = 5, a = 0.01, dmv = 10000 * (1 + 5 * 0.01) = 10500 votes after modification
                            distance = ranking.index(candidate) - ranking.index(opponent)
                            #print(votes * (1 + distance*alpha))
                            if distance < 0:
                                candidate_points += votes * (1 + distance * alpha)
                            else:
                                opponent_points += votes * (1 + distance * alpha)
                    if candidate_points > opponent_points:
                        score[candidate] += 1
                        if score[candidate] == len(candidates) - 1:
                            stop = True
                        print(candidate + " beat " + opponent + " " + str(candidate_points) + " to " + str(opponent_points))
                    else:
                        score[opponent] += 1
                        if score[opponent] == len(candidates) - 1:
                            stop = True
                        print(opponent + " beat " + candidate + " " + str(opponent_points) + " to " + str(candidate_points))
                    pairs.append((opponent, candidate))
                    pairs.append((candidate, opponent))
        # Increase alpha proportionally every iteration until winner or loser found
        alpha *= 2

    print("Round results: " + str(score))
    winner = list(score.keys())[list(score.values()).index(len(candidates) - 1)]
    print(winner + " is the round winner\n")
    if last_round:
        return winner
    else:
        return winner, recalculate_ballots(ballots, winner, alpha)

def recalculate_ballots(ballots : dict, winner : str, alpha : float) -> dict:
    '''
    Loop through ballots, recalculating votes (changing voting power) according to the distance the winner was from first choice
    Uses alpha, which may have increased from the original quantity based on the number of loops necessary to choose winner
    Logic: if it was more difficult to choose a winner, then the race was close, and those that lost out should have a larger advantage next round
    '''
    new_ballots = {}
    for ballot in ballots:
        if len(ballot) != 1:
            distance_from_first = ballot.index(winner)
            ballot_without_winner = tuple(filter(lambda x : x != winner, ballot))
            if ballot_without_winner not in new_ballots:
                new_ballots[ballot_without_winner] = ballots[ballot] / (1 + distance_from_first * alpha)
            else:
                new_ballots[ballot_without_winner] += ballots[ballot] / (1 + distance_from_first * alpha)
    return new_ballots

def process_election(ballots : dict, num_winners : int, alpha : float) -> list:
    winners = []
    new_ballots = ballots
    for i in range(num_winners):
        candidates = []
        for ballot in new_ballots:
            for candidate in ballot:
                if candidate not in candidates:
                    candidates.append(candidate)
        assert num_winners - (i + 1) < len(candidates)
        #print(candidates)
        if i != num_winners - 1:
            winner, new_ballots = process_round(new_ballots, candidates, alpha)
        else:
            winner = process_round(new_ballots, candidates, alpha, last_round=True)
        winners.append(winner)
    return winners

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-e", "--election-file", dest="ballots", required=True)
    parser.add_argument("-n", "--num-winners", dest="num_winners", default=3)
    parser.add_argument("-a", "--alpha", dest="alpha", default=0.01)
    args = parser.parse_args()

    num_winners = int(args.num_winners)
    alpha = float(args.alpha)

    ballots = {}
    with open(args.ballots, "r") as election:
        for line in election:
            split = line.strip().split(",")
            if split[1] == '':
                continue
            votes = int(split[0])
            ranking = tuple(split[1:])
            ballots[ranking] = votes

    winners = process_election(ballots, num_winners, alpha)
    print("ELECTION RESULTS")
    for i, winner in enumerate(winners):
        print(str(i+1) + ". " + winner)
main()

