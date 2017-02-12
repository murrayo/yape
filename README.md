# yape
yet another pButtons extractor

For quickly processing and charting InterSystems Caché pButtons support files.

## Python version

For writing and testing I am using Python 3. Specifically:

    python --version
    Python 3.5.2 :: Anaconda 4.2.0 (x86_64)

For example if you are running default on OSX you will have Python 2.7. You can run 2.7 and 3 side by side.

## Overview
At the moment this process has _two_ steps.

**Step 1.** `extract_pButtons.py`

Extract interesting sections from pButtons and write to .csv files for opening with excel or processing with charting.

Version .01 10 Feb 2017

- mgstat extracted for all operatings systems.
- vmstat and iostat for Red Hat only.
- windows perfmon for Windows.

Plans:

- Expand to all operating systems, for example variants of vmstat and iostat.

**Step 2.** `graph_pButtons.py`

Chart files created at step 1. Currently just simple `.png`

Version .01 10 Feb 2017

- png output for:
..- mgstat.
..- vmstat Red Hat only.

Plans:

- Expand charting to all formats from step 1. 
- Create interactive html via Bokeh (as per Fabians InterSystems Community Posts).
- Create standard set of multi-file charts for trouble-shooting and performance analysis.
