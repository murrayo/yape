# yape
yet another pButtons extractor

For quickly processing and charting InterSystems Caché pButtons support files.

## Python version

Please check you have the correct Python version. For writing and testing I am using Python 3. Specifically:

    python --version
    Python 3.5.2 :: Anaconda 4.2.0 (x86_64)
    
I have also tested on 3.6. New to Python? See Fabians article on InterSystems Community or google :) 

https://community.intersystems.com/post/visualizing-data-jungle-part-i-lets-make-graph

Look right through to the comments: E.g. Be sure to install extra Python modules. `sudo pip3 install matplotlib` and `sudo pip3 install pandas`. Also since February 18th version: `sudo pip install bokeh` for interactive charts.

For example if you are running default on OSX you will have Python 2.7. You can run Python 2.7 and Python 3.x side by side.

## Overview
At the moment this process has _two_ steps.

### Step 1. `extract_pButtons.py`

Extract interesting sections from pButtons and write to .csv files for opening with excel or processing with charting with `graph_pButtons.py`.

For more info:

`extract_pButtons.py --help`

Example:
`./extract_pButtons.py my_pbuttons_file_name.html`

Will create a folder `./metrics` with .csv files. Which .csv depends on the OS pButtons was run on.

Version .02 15 Feb 2017

- mgstat extracted for all operatings systems.
- vmstat for RH and AIX
- iostat for RH (AIX output to .txt file)
- windows perfmon for Windows.

### Step 2. `graph_pButtons.py`

Chart files created at step 1. Currently just simple `.png`

Version .03 16 Feb 2017

- png output.  

Version .04 18 Feb 2018

- Added support for output using Bokeh (interactive html files)
- Changed command line options, so look at --help.

For more info:

`graph_pButtons.py  --help`

Example:
`./graph_pButtons.py ./metrics`

Will scan `./metrics` for files created by extract_pButtons and output png files to `./charts` by default.

Plans:

- Create standard set of multi-file charts for trouble-shooting and performance analysis.

