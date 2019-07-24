# yape

Yet Another pButtons Extractor

Use at your own risk and if you find any issues, please feel free to file it [here](https://github.com/murrayo/yape/issues).

## Installation: Docker Container (recommended)

### Use image from docker hub

Of course, you need docker installed first :)

[https://hub.docker.com/r/yape/yape/]

The same usage information applies, for example:

```
docker pull yape/yape
docker container run --rm -v "$(pwd)":/data yape/yape --help
```

For example to extract mgstat and vmstat quietly and also output csv files:
```
cd <directory with your pButtons file.html>
docker container run --rm -v "$(pwd)":/data yape/yape --mgstat --vmstat -qc /data/<name of your pButtons file.html>
```


### Create image yourself

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

Python can be a beast about versions, for the simplest experience a container is a good way to go. You have been warned.

See: https://www.anaconda.com/distribution

The following was used to test and build yape for the container version:

```
$ python --version
Python 3.7.3
```

To use pip to install packages to Anaconda Environment
```
$ sudo conda install pip
```

```
$ pip --version
pip 19.1.1 from /Users/mo/anaconda3/lib/python3.7/site-packages/pip (python 3.7)
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

### Example: Dotgraphs plotting
To switch to dot graphs instead of line graphs set the style to "". For example, define the following in your config:
```
plotting:
  dim: 16,6
  style: ""
  markersize: 2
```

dim is dimensions in inches.

Choices for style are:
'-' solid line
'--' dashed line
'-.' dash-dotted line
':' dotted line

The defaults for configuration are:
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
yape --filedb data.db --timeframe "2018-06-11 00:00:00,2018-06-17 22:00:00" -a --skip-parse -o testdata/ 
```
Note: the last positional argument (pButtons file name) is not entered when --skip-parse and --filedb are used.

## Experimental interactive version

Change to the base of your checked out yape directory and run:
```
bokeh serve --show yapesrv --args /path/to/your.html
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
