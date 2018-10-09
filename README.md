# yape 2

Yet Another pButtons Extractor 2

Second revision of the original yape. Complete rewrite based on the ideas and lessons learned of the first one. Still in development, but mostly in a usable form now. Use at your own risk and if you find any issues, please feel free to file it [here](https://github.com/murrayo/yape/issues).

The goals for the rewrite are:

- make it a one-step-process
- add more interactivity with less waiting time
- be able to handle bigger datasets


## Installation: Docker Container (recommended)


To avoid any fighting with python versions there is a Dockerfile for building a container

```
cd <some place you want the files>
git clone https://github.com/murrayo/yape.git
cd yape
docker build -t yape2 .
```

You can run the container like this example to get parameters:
```
docker container run --rm -v "$(pwd)":/data yape2 --help
```

For example to extract mgstat and vmstat quietly and also output csv files:
```
cd <directory with your pButtons file.html>
docker container run --rm -v "$(pwd)":/data yape2 --mgstat --vmstat -qc /data/<name of your pButtons file.html>
```

>Note:
>This installs the command line version only, for the interactive version you will need to install locally in your OS (see below).



## Installation: Local

Requires git, pip and Python installed aready as per Python Version as below. Includes Alpha of the interactive version.

### About Python Version

Python can be a beast about versions, for the simplest experience a container is a good way to go.

yape has been tested on the following Python version;
```
$ python --version
Python 3.6.4 :: Anaconda custom (64-bit)

$ pip --version
pip 18.0 from /Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/site-packages/pip (python 3.6)
```

### Install for running locally

```
cd <some place you want the files>
git clone https://github.com/murrayo/yape.git
sudo pip install . --upgrade

yape --help
```

## Other things you can try

### Personal default options

You can specify a configuration file with the
```
yape --config config.example.yml ...
```
parameter. This allows to set things like the default output graph size. See `config.example.yml` for possible options and their default value.
Yape will always check if there is a `~/.yape.yml` file and load that.

### Dotgraphs plotting
To switch to dotgraphs instead of linegraphs, define the following in your config:
```
plotting:
  dim: 16,6
  style: .
  markersize: 0.5
```
The defaults are:
```
plotting:
  dim: 16,6
  style: "-"
  markersize: 1
```

### Weekly overview graphs

To create a week overview graph you can currently parse a number of pbuttons into a file and then plot that:
```
yape --filedb data.db pbuttons1.html
yape --filedb data.db pbuttons2.html
yape --filedb data.db pbuttons3.html
yape --filedb data.db pbuttons4.html
yape --filedb data.db pbuttons5.html
yape --filedb data.db pbuttons6.html
yape --filedb data.db pbuttons7.html
....
yape --filedb data.db --timeframe "2018-06-11 00:00:00,2018-06-17 22:00:00" -a --skip-parse -o testdata/ pbuttons7.html
```
Note: the last positional argument is still required, but is going to get ignored completely. (todo: fix the argument parsing for that)

## Experimental interactive version

Change to the base of your checked out yape directory and run:
```
bokeh serve --show yapesrv --args /Users/kazamatzuri/work/cases/898291/0503/squh-tc_TRAKCARE_20180503_000100_24hours_2_P1.html
```

This will give you (maybe) an interactive display of the pbuttons passed in. If you run into any errors, feel free to create an issue here: https://github.com/murrayo/yape/issues

## Testing

To run the unittests, use
```
python setup.py nosetests
```
(you might need to use python3 as command if you have multiple versions of python installed)

It will run tests with all pbutton files found in the test-data directory.

## Related Discussion

See the detailed description and discussion [in this article](https://community.intersystems.com/post/yape-yet-another-pbuttons-extractor-and-automatically-create-charts).
Have a look at [InterSystems Developer Community](community.intersystems.com) to learn about InterSystems technology, sharing solutions and staying up-to-date on the latest developments.
