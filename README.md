# Agent Based Disease Modelling

## Overview

The aim of this project is to build, assess and visualise agent based models (ABMs), specifically in the area of disease modelling. Thus the bulk of this project's codebase is focussed on the implementation of simulations, covering a wide range of variables and sources of interest, such as superspreaders, social distancing and hospital bed limits.
In order to see the advantages and disadvantages of ABMs, it is useful to first spend some time on the more common, traditional method of mathematical modelling, equation based models (EBMs), and so there is also some code relating to these.

## Install

This project is coded in Python 3.7, and so this installation guide assumes you are running the same. This easiest way to install is to download the source code by cloning the git repository.

```
git clone https://github.com/ACM40960/project-flbrack.git
```

In order to manage dependencies, it is advisable to create a Python virtual environment. First `cd` into the project folder,

```
cd project-flbrack
```

Then to create a virtual environment, named `env`, run

```
python3 -m venv env
```

Then to activate the virtual environment, run

```
source env/bin/activate
```

We can then install the necessary libraries and packages using `pip`, Python's package manager. First we should make sure the `pip` in the virtual environment is up to date, by running

```
python3 -m pip install --upgrade pip
```

The dependencies are listed in the requirements.txt file. Fortunately, `pip` can read this file. Run the following command

```
python3 -m pip install -r requirements.txt
```

All requirements should now be installed and the project code is ready to be ran.