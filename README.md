# yape
yet another pButtons extractor

For quickly processing and charting InterSystems Caché pButtons support files.

## Python version

Please check you have the correct Python version. For writing and testing I am using Python 3. Specifically:

    python3 --version
    Python 3.6.0

New to Python? See Fabian's article on InterSystems Community or google :)

https://community.intersystems.com/post/visualizing-data-jungle-part-i-lets-make-graph

Look right through to the comments: E.g. Be sure to install extra Python modules. `sudo pip3 install matplotlib` and `sudo pip3 install pandas`. Also since February 18th version: `sudo pip3 install bokeh` for interactive charts.

For example if you are running default on OSX you will have Python 2.7.

You can run Python 2.7 and Python 3.x side by side.

## Overview
At the moment this process has _two_ steps.

### Step 1. `extract_pButtons.py`

Extract interesting sections from pButtons and write to .csv files for opening with excel or processing with charting with `graph_pButtons.py`.

For more info:

`extract_pButtons.py --help`

Example:
`./extract_pButtons.py my_pbuttons_file_name.html`

Will create a folder `./metrics` with .csv files. Which .csv depends on the OS pButtons was run on.

Functionality notes:

- mgstat extracted for all operatings systems.
- vmstat for RH and AIX
- iostat for RH (AIX output to .txt file)
- windows perfmon for Windows.

### Step 2. `graph_pButtons.py`

Chart files created at step 1. Currently `.png` charts as lines (default) or dot or interactive `.html`

For more info:

`graph_pButtons.py  --help`

Example:
`./graph_pButtons.py ./metrics`

Will scan `./metrics` for files created by extract_pButtons and output selected chart type. Line chart to `./charts` by default.

## Examples

Example walk a directory of one or more pbuttons.html, create different chart types and add filename to title.

#### Extract to .csv

    for i in `ls *.html`; do /path_to/extract_pButtons.py $i -p ${i}_; done

#### Chart all types

    for j in line dot interactive; do for i in `ls *.html`; do /path_to/graph_pButtons.py ./${i}_metrics -p ${j}_${i}_ -s ${j} -t ${i} -I; done; done

#### Process multiple pButtons .html files in the same directory into a single graph (eg a weeks files)

Be sure to change the variable YAPE_PATH

    ./yape_week.sh -d ../path/to/pbuttons/files -I -v


## Docker image
To make usage of yape a little bit easier, we added a Dockerfile. Check out the repository and then run:

    docker build -t kazamatzuri/yape:1.0 .

Afterwards you can run yape on your pButtons file like this:

    docker run -v `pwd`/:/data  --rm --name yape-test kazamatzuri/yape:1.0 pButtons.html

## Related Discussion

See the detailed description and discussion [in this article](https://community.intersystems.com/post/yape-yet-another-pbuttons-extractor-and-automatically-create-charts).
Have a look at [InterSystems Developer Community](community.intersystems.com) to learn about InterSystems technology, sharing solutions and staying up-to-date on the latest developments.
