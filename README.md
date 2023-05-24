# MAC-Tracker

## Prerequisites
In order to use this project you have to have python3 installed.

## Prepare the local environment
Clone the project locally: `git clone git@github.com:allexu/MAC-Tracker.git`
Open a terminal and navigate to the project directory
Create the environment: `python -m venv env`
Activate the environment: `env\Scripts\activate`
Install dependencies `pip install -r requirements.txt`

## Using the tool
Every time you have to activate the environment before using the tool
By simply running python main.py it will show you the help menu which looks like this:
```
Usage: MAC Tracker [OPTIONS]

Options:
  -p, --print            Print the MAC address tables for all switches
  -i, --ip-address TEXT  Specify IP addresses of switches
  -s, --search TEXT      Search for MAC addresses in the specified switch(es)
  --help                 Show this message and exit.
  ```
  
Here are few examples:
```
python main.py --help
python main.py -p
python main.py -i 10.0.1.1 -p
python main.py -s aa:bb:cc:dd:ee:ff -s 11:22:33:44:55:66
python main.py -s aa:bb:cc:dd:ee:ff -s 11:22:33:44:55:66 -i 10.0.1.1
python main.py -s aa:bb:cc:dd:ee:ff -s 11:22:33:44:55:66 -i 10.0.1.1 -i 10.0.1.2
```
