# flash_cards [![GitHub license](https://img.shields.io/badge/license-MIT-teal.svg)](https://github.com/tomasvana10/seriescalculator_sdd/main/LICENSE.md) ![version](https://img.shields.io/github/v/release/tomasvana10/flash_cards) 
A very simple flash cards GUI built with CustomTkinter

Download .zip: [click here](https://github.com/tomasvana10/flash_cards/archive/refs/heads/main.zip)

## Dependencies
Installed with pip
- `customtkinter==5.2.0`
- `ankisync2==0.3.4`
- `numpy==1.25.2`
- `Pillow==10.0.0`

Pip is likely already installed on your computer. If it isn't, [click here](https://pip.pypa.io/en/stable/installation)

## Installation
Once pip is installed on your computer, follow these steps:
 - Run this command in your terminal to clone the repository: `git clone https://github.com/tomasvana10/flash_cards.git`
 - Copy the path of the repository on your computer, run `cd flash_cards` 
 - Install the dependencies by executing `pip install -r requirements.txt`. Ensure you type -r.
 - Run the program: `python3 flash_cards.py`

## Features
- __Just click through cards or actually type the answer__
  - Simply click enter to cycle through questions.
  - Uses Jaccard's Index to compare your answer to the true answer and return a score.
    
- __Logs all your scores__
  - Data including deck name, question, answer, your answer, timestamp and score.
  - Scores are written to `flash_cards/scores.json`
 
- __Singular and bulk conversion of Anki Deck files (.apkg) using ankisync2__
  - Simply export your deck as a `.apkg` and only leave `Include scheduling information` unchecked.
  - Go to `flash_card`'s built-in settings, open the `imports` folder and drag the `.apkg` and begin conversion.
  - Note that you will have to reopen the settings window to view `.apkg` files you added while you had settings open.

## Acknowledgements
This project utilises the following custom modules and libraries:
- [CustomTkinter](https://pypi.org/project/customtkinter/)
- [Pillow](https://pypi.org/project/pillow/)
- [NumPy](https://pypi.org/project/numpy/)
- [ankisync2](https://pypi.org/project/ankisync2/)
