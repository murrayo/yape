# yape 2
yet another pButtons extractor 2

Second revision. Complete rewrite based on the ideas and lessons learned of the first one. And yes, this is currently heavily in the alpha stage. Use at your own risk.

The goals for the rewrite are:
   * make it a one-step-process
   * add more interactivity with less waiting time
   * be able to handle bigger datasets

# Basic usage

## Installation local copy

```
git clone https://github.com/murrayo/yape.git
git checkout
pip3 install . --upgrade
```
## parameters
```
$ yape -h
usage: yape [-h] [--filedb FILEDB] [--skip-parse] [-c] [--mgstat] [--vmstat]
            [--iostat] [--permon] [--timeframe TIMEFRAME] [--prefix PREFIX]
            [--plotDisks PLOTDISKS] [-a] [-o OUT]
            pButtons_file_name

Yape 2.0

positional arguments:
  pButtons_file_name    path to pButtons file to use

optional arguments:
  -h, --help            show this help message and exit
  --filedb FILEDB       use specific file as DB, useful to be able to used
                        afterwards or as standalone datasource.
  --skip-parse          disable parsing; requires filedb to be specified to
                        supply data
  -c                    will output the parsed tables as csv files. useful for
                        further processing. will currently create: mgstat,
                        vmstat, sar-u. sar-d and iostat will be output per
                        device
  --mgstat              plot mgstat data
  --vmstat              plot vmstat data
  --iostat              plot iostat data
  --permon              plot perfmon data
  --timeframe TIMEFRAME
                        specify a timeframe for the plots, i.e. --timeframe
                        "2018-05-16 00:01:16,2018-05-16 17:04:15"
  --prefix PREFIX       specify output file prfeix
  --plotDisks PLOTDISKS
                        restrict list of disks to plot
  -a, --all             graph everything
  -o OUT, --out OUT     specify base output directory, defaulting to
                        <pbuttons_name>/
```
## Weekly overview graphs

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

## Docker

To avoid any fighting with python versions there is also a Dockerfile for building a container for the interactive version

For example:
```
docker build -t yape2 .
```

## Related Discussion

See the detailed description and discussion [in this article](https://community.intersystems.com/post/yape-yet-another-pbuttons-extractor-and-automatically-create-charts).
Have a look at [InterSystems Developer Community](community.intersystems.com) to learn about InterSystems technology, sharing solutions and staying up-to-date on the latest developments.