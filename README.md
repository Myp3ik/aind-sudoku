# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  
A: Naked twins problem is solved with same constraint propagation techniques as ordinary sudoku grid plus one new constraint.
Idea of all constraints is to limit possible values for each box. We use 3 constraints: "elimination", "only choice" and "naked twin".
Last constraint limits box possible values even more if naked twin is found in the unit. Values for these units are possible only
in the these boxes and not any other. As a result we remove these values as possibilities in other boxes in the same unit.

# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  
A: To solve diagonal sudoku problem we use the same constraints we use with ordinary sudoku, except constraints become more strict.
1 unit group of diagonals added, thus our 3 constraint propagation techniques started to limit possible values for more boxes.
Before introducing this change each box had 20 peers, but now each box has 26 peers. So more boxes are dependant on each value
assigned to the box.

### Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project. 
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Code

* `solutions.py` - You'll fill this in as part of your solution.
* `solution_test.py` - Do not modify this. You can test your solution by running `python solution_test.py`.
* `PySudoku.py` - Do not modify this. This is code for visualizing your solution.
* `visualize.py` - Do not modify this. This is code for visualizing your solution.

### Visualizing

To visualize your solution, please only assign values to the values_dict using the ```assign_values``` function provided in solution.py

### Data

The data consists of a text file of diagonal sudokus for you to solve.