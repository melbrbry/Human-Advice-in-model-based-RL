# Human-Advice-in-model-based-RL
In this project, we use Human Advice expressed in LTL-f to guide the exploration of the learning agent in a variant of R-max. We demonstrate the effective of the approach 
in a simple grid game called ESCAPE!. The agent should get the key first and then reach the door while avoiding the nails.
We use different advices and test them against the plain algorithm.

## Getting Started

You need to clone the reporistory to your local machine. Run this command in your terminal where you like to clone the project

```
git clone https://github.com/melbrbry/Human-Advice-in-model-based-RL
```

### Prerequisites

Required packages (use pip install on linux):  
numpy  
automata  
pygame  

## Repository Description
The repository has only one branch: the master branch.

## Documentation
In this section, I write a brief description of some of the repository files/folders

**Main.py**: the main code, it runs the GUI of the game.

**HRI.py**: impelements the variant of R-Max with advice incorporated.

**RMax.py**: impelements the plain variant of R-Max.

**HRI_report_v3.pdf**: full project report.

**automata**: this folder contains automata library.

## Acknowledgement
- This project is done as part of the Electives in AI course taught by prof. De Giacomo and prof. Ellen Foster - Sapienza Università di Roma.
- This project is a team-based project done with my teammates: Jim Catacora, Jose Jaramillo.


