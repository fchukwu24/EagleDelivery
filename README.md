# Eagle Delivery

Eagle Delivery is a Python project that simulates a campus delivery robot.
The robot navigates a grid map between building entrances. The project
compares uninformed and heuristic search for route planning, then uses
Q-learning to learn delivery policies through interaction with the
environment.

## Requirements

- Python 3.9 or newer
- No third-party Python packages are required

Run commands from the project root directory. Use `python` on Windows or
`python3` on systems where that is the Python 3 command.

## Project files

- `agents.py` contains BFS, A*, epsilon-greedy action selection, and the
  Q-learning update.
- `campus.py` loads maps and implements robot movement, rewards, and episodes.
- `run_project.py` displays maps, runs searches, and trains/evaluates agents.
- `summarize_results.py` summarizes a training run and creates a learning
  curve CSV.
- `maps/emu_campus.txt` and `maps/emu_detour.txt` are the supplied maps.
- `maps/my_campus.txt` is the custom map used for Part C.

Map symbols are `#` for blocked cells, `.` for walkways, and `S`, `L`, `H`,
`D`, `P`, and `W` for building entrances.

## Run the project

Display the default campus map:

```powershell
python run_project.py show
```

Search for a route with BFS or A*:

```powershell
python run_project.py search --algorithm bfs --start S --goal W
python run_project.py search --algorithm astar --start S --goal W
```

Choose another map with `--map`:

```powershell
python run_project.py search --map maps/emu_detour.txt --algorithm astar --start L --goal D
python run_project.py search --map maps/my_campus.txt --algorithm astar --start S --goal W
```

Run a random-action agent:

```powershell
python run_project.py random --start S --goal W --seed 0
```

## Tests

Run the full test suite:

```powershell
python -m unittest discover -v
```

Run only the search or learning tests:

```powershell
python -m unittest tests.test_student.SearchTests -v
python -m unittest tests.test_student.LearningTests -v
```

## Baseline Q-learning runs

The training command defaults to the following settings:

| Setting | Default |
|---|---:|
| Training episodes | 2,000 per seed |
| Seeds | 0, 1, 2 |
| Evaluation episodes | 100 per seed |
| Maximum actions | 200 per episode |
| Learning rate (`alpha`) | 0.3 |
| Discount factor (`gamma`) | 0.95 |
| Exploration rate (`epsilon`) | 0.2, constant during training |
| Slip probability | 0.0 |

Run the three required baseline delivery tasks. Each task writes CSV results
to its own output directory:

```powershell
python run_project.py train --start S --goal W --output results/baseline_SW
python run_project.py train --start L --goal D --output results/baseline_LD
python run_project.py train --start H --goal P --output results/baseline_HP
```

Each run saves per-seed training and evaluation CSV files plus `summary.csv`.
Generate `learning_curve.csv` and print a summary for a run with:

```powershell
python summarize_results.py results/baseline_SW
python summarize_results.py results/baseline_LD
python summarize_results.py results/baseline_HP
```

## Custom map experiment

The custom map is `maps/my_campus.txt`. The controlled experiment asks:

> How does movement slip probability affect Q-learning's training progress
> and delivery performance on the custom map for the S-to-W task?

Only slip probability changes between conditions; the other training settings
remain at their defaults. Each condition uses seeds 0, 1, and 2, trains for
2,000 episodes per seed, and evaluates for 100 episodes per seed. The same
slip probability is used during training and evaluation.

Run the three conditions and summarize each results folder:

```powershell
python run_project.py train --map maps/my_campus.txt --start S --goal W --slip 0.0 --output results/custom_slip000
python run_project.py train --map maps/my_campus.txt --start S --goal W --slip 0.1 --output results/custom_slip010
python run_project.py train --map maps/my_campus.txt --start S --goal W --slip 0.2 --output results/custom_slip020

python summarize_results.py results/custom_slip000
python summarize_results.py results/custom_slip010
python summarize_results.py results/custom_slip020
```

Compare evaluation success rate, mean successful delivery steps, and mean
return in each `summary.csv`. Compare training progress using
`learning_curve.csv`, which reports success rate and return in blocks of 100
episodes.
