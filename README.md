# Drum Machine
Author: Emily Quinn Finney
Version: 1.0

In this package I implemented built an electronic drum machine that prints 
drum rhythms across the CLI. The package is written in Python, tested in pytest,
and uses various data types including generators and bitmaps. 

## Features

The drum machine (drum.py) in its current form can: 
* Create a Song object with a certain title and number of beats per minute
* Play all rhythms available in a given pattern dictionary (pattern_dict). This dictionary is currently hard-coded.
* "Play" a Song (aka, print rhythms across the CLI) for a user-defined number of seconds. 

I intend to add more features to this drum machine, including the ability to 
play sound, as time permits.

## Running Tests

To test the code, you will need pytest installed. Then type the following into the terminal: 

```
pytest -v -s test_drum.py
```

Last edited 04/05/2018