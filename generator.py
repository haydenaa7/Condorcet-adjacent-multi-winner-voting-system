import argparse
import json
import math
import random

'''
Random Election Generator
'''

def arguments():
    '''Get command line arguments'''
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--num-voters", dest="voters", default=10)
    parser.add_argument("-c", "--num-candidates", dest="candidates", default=3)
    parser.add_argument("-r", "--max-unique-rankings", dest="unique", default=10e10)
    parser.add_argument("-maxrl", "--max-ranking-length", dest="max")
    parser.add_argument("-minrl", "--min-ranking-length", dest="min")
    parser.add_argument("-n", "--num-elections", dest="elections", default=1)
    parser.add_argument("-o", "--output-file", dest="output")
    parser.add_argument("-j", "--output-json", dest="json", default="true")
    args = parser.parse_args()
    return args

def generate_unique_rankings(num, candidates, min_len, max_len, voters):
    '''Generate all unique rankings'''
    rankings = []
    i = 0
    while i < min(num, math.factorial(candidates), voters):
        length = random.randint(min_len, max_len)
        ranking = random.sample([i for i in range(candidates)], k=length)
        if ranking not in rankings:
            rankings.append(ranking)
            i += 1
    return rankings

def generate_ballots(voters, rankings):
        '''Generate all ballots for an election'''
        # Create distribution of votes amongst rankings
        ranking_distribution = sorted([round(random.uniform(0.0,100.0), 3) for _ in range(len(rankings)-1)]) + [100.0]

        ballots = []
        prev = 0.0
        voters_remaining = voters
        for i in range(len(rankings)):
            cur_ranking = rankings[i]
            num_votes = min(round(voters * (ranking_distribution[i] - prev) * 0.01), voters_remaining)
            voters_remaining -= num_votes
            if i == len(rankings) - 1 and voters_remaining > 0:
                num_votes += voters_remaining
                voters_remaining = 0
            if num_votes == 0:
                continue
            ballots.append((cur_ranking, num_votes))
            prev = ranking_distribution[i]
        return ballots

def generate_elections(unique, candidates, min_len, max_len, num_elections, voters):
    '''Generate all elections'''
    elections = []
    for _ in range(num_elections):

        # Pull unique rankings and update status
        rankings = generate_unique_rankings(unique, candidates, min_len, max_len, voters)
        
        # Generate ballots
        ballots = generate_ballots(voters, rankings)
        elections.append(ballots)
    return elections

def output_elections_json(output, elections, voters, candidates, unique, min_len, max_len):
    json_statement = {"num_voters": voters, "num_candidates": candidates, "max_unique_rankings": unique, \
                          "max_ranking_length": max_len, "min_ranking_length": min_len, "num_elections": len(elections), \
                            "elections": [{"ballots": [{"ranking": ranking[0], "count": ranking[1]} for ranking in election]} for election in elections]}
    if output is None:
        print(json.dumps(json_statement, indent=4))
    else:
        with open(output, "w") as file:
            file.write(json.dumps(json_statement, indent=4))

def output_elections_csv(output, elections):
    result = ""
    for i, election in enumerate(elections):
        for j, ranking in enumerate(election):
            result += str(ranking[1]) + ","
            for k, candidate in enumerate(ranking[0]):
                if k != len(ranking[0]) - 1:
                    result += str(candidate) + ","
                else:
                    result += str(candidate)
            if j != len(election) - 1:
                result += "\n"
        if i != len(elections) - 1:
            result += "\n\n"
    if output is None:
        print(result)
    else:
        with open(output, "w") as file:
            file.write(result)

def main():
    # Pull and process arguments
    args = arguments()
    voters = int(args.voters)
    candidates = int(args.candidates)
    unique = int(args.unique)
    max_len = args.max
    if max_len is None:
        max_len = candidates
    else:
        max_len = int(max_len)
    min_len = args.min
    if min_len is None:
        min_len = candidates
    else:
        min_len = int(min_len)
    num_elections = int(args.elections)
    output = args.output
    json = args.json.lower()

    elections = generate_elections(unique, candidates, min_len, max_len, num_elections, voters)
    if json == 'true' or json == 't':
        output_elections_json(output, elections, voters, candidates, unique, min_len, max_len)
    else:
        output_elections_csv(output, elections)
main()
