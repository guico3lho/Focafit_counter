# Focafit Counter

## This repository contains the code for the Focafit Counter: an automation to count the number of points each sector scored weekly doing exercises!

## Project Overview

- `assets` folder contains the input and output of the project
- `notebooks` folder contains experiment and test purpose code only
- `src` folder contains the code the Focafit coounter uses to work
- `requirements.txt` file contains the dependecies of the project
- `.runAndDebugOnPyCharm` folder contains configuration to Run/Debug project on Pycharm

## The project was made using:

- PyCharm IDE
- Anaconda
- Python 3.10.9
- Windows 10+
- All packages used are listed in the `requirements.txt` file

## Running on your machine

- Clone the repository
- Inside `Focafit_counter` directory:
  - Install the dependencies using `pip install -r requirements.txt`
  - Add the exported file from Whatsapp in the folder `assets/input`
  - Modify `input_file_path` variable in `src/counter.py` to point to the chat file
  - run `python -m src.counter` to run the Focafit counter!
