# yape 2

Yet Another pButtons Extractor 2

Second revision. Complete rewrite based on the ideas and lessons learned of the first one. And yes, this is currently heavily in the alpha stage. Use at your own risk.

The goals for the rewrite are:

- make it a one-step-process
- add more interactivity with less waiting time
- be able to handle bigger datasets

## Installation: Docker Container (recommended)

To avoid any fighting with python versions there is a Dockerfile for building a container for the interactive version

```
cd <some place you want the files>
git clone https://github.com/murrayo/yape.git
docker build -t yape2 .
```

You can run the container like this example to get parameters:
```
cd <location of your pButtons file>
docker container run --rm -v `pwd`:/data yape2 --help
```

For example to extract mgstat and vmstat:
```
docker container run --rm -v `pwd`:/data yape2 --mgstat --vmstat -q /data/<name of your pButtons file.html
```

>Note:
>This installs the command line version only, for the interactive version you will need to install locally in your OS (see below).



## Installation: Local

Requires git, pip and Python installed aready as per Python Version as below. Includes Alpha of the interactive version.

### About Python Version

Python can be a beast about versions, for the simplest experience a container is a good way to go, see the instructions for Docker below.

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


## Related Discussion

See the detailed description and discussion [in this article](https://community.intersystems.com/post/yape-yet-another-pbuttons-extractor-and-automatically-create-charts).
Have a look at [InterSystems Developer Community](community.intersystems.com) to learn about InterSystems technology, sharing solutions and staying up-to-date on the latest developments.
