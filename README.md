# Focafit Counter

## This repository contains the code for the Focafit Counter: an automation to count the number of points each sector scored weekly doing exercises!

## Project Overview

- `assets` folder contains the input and output of the project
- `src` folder contains the code the Focafit coounter uses to work
- `requirements.txt` file contains the dependecies of the project
- `.runAndDebugOnPyCharm` folder contains configuration to Run/Debug project on Pycharm

## The project was made using:

- PyCharm IDE
- Anaconda
- Python 3.10.9
- Windows 10+
- All packages used are listed in the `requirements.txt` file

## Setting environment

- Clone the repository
- Inside `Focafit_counter` directory:
  - Install the dependencies using `pip install -r requirements.txt`;
  - Add the exported txt file from Whatsapp into `assets/input` folder.


## Running the code
- This project uses `argparse` library
- Currently, there are 3 arguments:
  - `"-i"` to specify the input file (format: path, type: str)
  - `"-o"` to specify the output file (format: path, type: str)
  - `"-d"` to specify the date the counting will be made (format: "dd/mm/yyyy", type: str)
  - Run `python -m src.counter -i "./assets/input/chat_example.txt" -o "./assets/output" -d "15/05/2023"` to run an example of the Focafit_counter!
  - The result can be checked inside `./assets/output` folder
  - The expected result is:
```
🦾 FOCA FIT SEMANAL - 08/05 A 14/05 🦾 
Gerado por: Focafit_counter 😎 

💜💙🖤 RANKING POR NÚCLEO 💚🧡💛 

1ª BOPE: 40
2ª NOE: 6
3ª NUT: 4
4ª NDP: 2


🏆 RANKING POR PESSOA 🏆

1º Chico: 4
2º Zeca: 2

```
