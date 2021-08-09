# Agent Based Disease Modelling

# Overview

The aim of this project is to build, assess and visualise agent based models (ABMs), specifically in the area of disease modelling. Thus, the bulk of this project's codebase is focused on the implementation of simulations, as well as the ability to animate these simulations, covering a wide range of variables and sources of interest, such as superspreaders, social distancing and hospital bed limits.
In order to see the advantages and disadvantages of ABMs, it is useful to first spend some time on the more common, traditional method of mathematical modelling, equation based models (EBMs), and so there is also some code relating to these.

# Getting Started

This project is coded in Python 3.7, and so this installation guide assumes you are running the same. This easiest way to get started and download the source code is by cloning the git repository.

```
git clone https://github.com/ACM40960/project-flbrack.git
```

In order to manage dependencies, it is advisable to create a Python virtual environment. First `cd` into the project folder,

```
cd project-flbrack
```

Then, to create a virtual environment, named `env`, run

```
python3 -m venv env
```

To activate the virtual environment, run

```
source env/bin/activate
```

We can then install the necessary libraries and packages using `pip`, Python's package manager. First we should make sure the the virtual environment's `pip` is up to date, by running

```
python3 -m pip install --upgrade pip
```

The project's dependencies are listed in the requirements.txt file. Fortunately, `pip` can read this file. Run the following command

```
python3 -m pip install -r requirements.txt
```

All requirements should now be installed and the project code is ready to be ran.

# Project Structure 

There are two main folders in the project, `Equation` contains code for running equation based models, and `Agent`, which contains the bulk of the project, contains code for running agent based model simulations and their animations.
Inside in each folder there is a subfolder named `Plots`, these are where the plots from the simulations are saved to. The `Agent` folder also contains a folder named `Data`. As some of the agent based simulations were ran multiple times, the data produced from these multiple runs were saved to this folder.

# Which Scripts to Run

## Equation Folder

This contains the code for the equation based models. All python scripts, (those ending with `.py`), can be ran. There are three files, each corresponding to a different equation based model. The name of the script clearly indicates which script implements which model. In order to run any of the scripts, `cd` into the `Equation` folder and then run `python3` followed by the script name. As an example, in order to run the SIR model, which is implemented in the SIRmodel.py script, run;

```
python3 SIRmodel.py
```

Each python script follows the same layout. At the top are the necessary libraries are imported. The [`scipy`](https://www.scipy.org/scipylib/index.html) library is used to numerically integrate the models differential equations and thus provide a plot of the solution.

There are a number of tunable parameters located near the top in each script that can be played around with, such as the population size, the initial number of infectious people and the recovery rate of the disease.

The equations are implemented and integrated and the results are plotted using the [`matplotlib`](https://matplotlib.org/) library. Each plot is saved to the `Equation/Plots` folder.

## Agent Folder

This contains the agent based models. There are a number of files here but not all should be ran directly.

### Animation Scripts

All files that begin with `Agent` can be ran and these are the files that will be of most interest and are most worth playing around with. Their names should be somewhat self-explanatory, but a short explanation is also written at the top of each script. Each of these scripts can be ran using `python3`. eg., in order to run the agent based equivalent of the SIR model, which is implemented by the `AgentSIRModel.py` script, run;

```
python3 AgentSIRModel.py
```

Most importantly, these are the scripts that produce animations. Animations can be turned on and off by editing the script and changing the `ANIMATION_FLAG` constant to either `True` or `False`. For the simulations themselves the [`numpy`](https://numpy.org/) library, as well as Python's standard `random` library are used. The animations are implemented using the [`pygame`](https://www.pygame.org/news) library. This is based on the [SDL library](https://www.libsdl.org/), which renders graphics using the CPU, instead of the GPU. As such, it is not always the most performant, amd to keep the animations smooth, a reasonable number of agents should be choosen.

In each of these scripts there are a number of tunable parameters, located near the top in each script, such as population size, infection rate, etc.

After the simulation and animation have finished, a plot is created and saved to the `Agent/Plots` folder graphically illustrating how the simulation unfolded.

### Repeated Scripts

Also located in this folder are the files beginning with `Repeated`. These run each of the agents based models multiple times. The data produced from these scripts is saved as a `csv` file to the `Data` folder. As these scripts run simulations with a large number of agents, and repeat them multiple times, they can take a long time to run, usually between 30 to 60 minutes for ten repeats. As a result there is no animation option for these scripts.

These also have a number of tunable parameters located near the top of the scripts. However, as these take so long to run, and are just repeated simulations of the same type as the animation scripts, I would recommend just running the animation scripts.

The `csv` data that is produced from these scripts is plotted using the `DataPlotting.py` script, again using `matplotlib`, as well as the [`pandas`](https://pandas.pydata.org/) library.

### The `agents.py` File

This is arguably the most important file in the project, and works as the back-end for all the agent based simulations. It contains the class definitions and methods for all the agents.
It also contains a number of functions that are used for the animations, as well as functions that are used for setting up the simulations.

For example, the base class of agent is the `Person` class. This contains a number of properties, such as radius, health status, and death rate. It also contains a number of methods.

+ The `__init__` method is simply the initialisaiton method that is called whenever an object of this class is created.
+ The `draw` method is used in animations for drawing the agent to the screen.
+ The `infect` method is used in simulation such that a susceptible agent can be infected by an infectious agent.
+ The `position_update` method controls how the agent moves in it's environment.
+ The `status_update` method affects the health status of the agent, for example, it controls when an agent turns from infectious to recovered.

There are a number of other classes that extend this base class, with altered and new methods, and these are described in the file itself.

There are a number of functions used to set up simulations located in this file. For example, the `create_SIR_population` function is used by the `AgentSIRModel.py` script to create an array of agents of the base class `Person`.

# Conclusion

There are many tunable options for the animations and it can be quite interesting to watch them unfold. I have set some reasonable default parameters, but it is worth playing around to see the different outcomes.
The equation based models also have tunable parameters, and it is interesting to compare the resulting plots to the plots produced by the agent based models.
I have optimised the simulations as best I could, but Python is not the quickest language, and while the animations run well usually, for some of the more complicated models, the frame rates can noticeably drop when the number of agents exceeds 200.
On my personal website I have an [interactive version](https://flbrack.com/posts/2021-07-01-agent/#interactive-animation) of the simple SIR model, which is also fun to play around with.