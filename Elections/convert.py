import argparse

def convert():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input-file", dest="file", required=True)
    parser.add_argument("-o", "--output-file", dest="output", required=True)
    parser.add_argument("-p", "--first-pos", dest="first", default=6)
    args = parser.parse_args()

    input_file = args.file
    output_file = args.output
    first = int(args.first)

    ballots = {}
    with open(input_file, "r") as i:
        i.readline()
        for line in i:
            cleaned = filter(lambda x : x != "", [phrase.replace("skipped,", "").replace("skipped", "").replace("Undeclared", "")\
                                                        .replace("Undeclared,", "").replace("overvote,", "").replace("overvote", "")\
                                                        .replace("Write-in,", "").replace("Write-in", "").replace("\"", "")
                                                            .strip() for phrase in line.split(",")[first:]])
            remove_dups = tuple(list(dict.fromkeys(list(cleaned))))
            if remove_dups != tuple():
                if remove_dups not in ballots:
                    ballots[remove_dups] = 1
                else:
                    ballots[remove_dups] += 1
    
    ballots = dict(sorted(ballots.items(), key=lambda item: item[1], reverse=True))

    with open(output_file, "w") as o:
        for ballot in ballots:
            o.write(str(ballots[ballot]) + "," + ",".join(ballot) + "\n")

    print("Successfully converted input file " + input_file + " to output file " + output_file)
convert()
