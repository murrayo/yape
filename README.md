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

Extract intereasting sections from pButtons to .csv file for opening with excel or processing with charting.

Version .01 10 Feb 2017

- mgstat extracted for all pButtons.
- vmstat and iostat for Red Hat only.
- windows perfmon.

**Step 2.** `graph_pButtons.py`

Chart files created at step 1. Currently just simple `.png`

Version .01 10 Feb 2017

- mgstat and vmstat only charted.

## Other Notes.

Will be expanded to cover AIX, Itanium, etc.
Ultimately the two separate processes could become one utility. 


