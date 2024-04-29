# Hayden's Method
### Condorcet-adjacent distance-based multi-winner ranked choice voting system

**voting_system.py** is the main file containing the voting algorithm implementation. If running on real-world cases, the main() function should be left uncommented and flags should be specified. An election flag (-e or --election) is required, and you may also specify the number of winners (-n or --num-winners) and the base alpha value (-a or --alpha). Several real-world cases are available in the Elections folder beginning with "parsed", and several test cases are available in the Tests folder. An example command here is "python3 voting_system.py -e Elections/parsed2020ADPR.csv -n 5".

**main.py** is an auxiliary file to run the algorithm on artificial test cases. The standard command to run this is "python3 main.py --elections elections.py --verbose", which will display outputs from all 70,000+ elections in elections.py, and display comparisons to existing popular algorithms such as IRV and Borda count.
