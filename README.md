# yape
yet another pButtons extractor

For quickly processing and charting InterSystems Caché pButtons support files.

## Python version

Please check you have the correct Python version. For writing and testing I am using Python 3. Specifically:

    python --version
    Python 3.5.2 :: Anaconda 4.2.0 (x86_64)

For example if you are running default on OSX you will have Python 2.7. You can run 2.7 and 3 side by side.

## Overview
At the moment this process has _two_ steps.

### Step 1.** `extract_pButtons.py`

Extract interesting sections from pButtons and write to .csv files for opening with excel or processing with charting.

For more info:

`extract_pButtons.py --help`

Example:
`./extract_pButtons.py my_pbuttons_file_name.html`

Version .02 15 Feb 2017

- mgstat extracted for all operatings systems.
- vmstat for RH and AIX
- iostat for RH (AIX output to .txt file)
- windows perfmon for Windows.

### Step 2.** `graph_pButtons.py`

Chart files created at step 1. Currently just simple `.png`

Version .02 15 Feb 2017

- png output.  

For more info:

`graph_pButtons.py  --help`

Example:
`./graph_pButtons.py -s ./metrics`


Plans:

- Create standard set of multi-file charts for trouble-shooting and performance analysis.
- Create interactive html via Bokeh (as per Fabians InterSystems Community Posts).
