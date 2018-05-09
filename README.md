# yape 2
yet another pButtons extractor

Second revision. Complete rewrite based on the ideas and lessons learned of the first one. And yes, this is currently heavily in the alpha stage. Use at your own risk.

The goals for the rewrite are:
   * make it a one-step-process
   * add more interactivity with less waiting time
   * be able to handle bigger datasets


To avoid any fighting with python versions, this revision is strictly distributed as
docker image.

# Basic usage
## Installation

```
git clone https://github.com/murrayo/yape.git
git checkout 2.0
pip3 install . --upgrade
```
## Basic usage:
```
yape -h
usage: yape [-h] [--filedb FILEDB] [-c] pButtons_file_name

Provide an interactive visualization to pButtons

positional arguments:
  pButtons_file_name  path to pButtons file to use

optional arguments:
-h, --help          show this help message and exit
--filedb FILEDB     use specific file as DB, useful to be able to used
                    afterwards or as standalone datasource
-c                  will output the parsed tables as csv files. useful for
                    further processing
--mgstat            plot mgstat data
-a ALL, --all ALL   graph everything
-o OUT, --out OUT   specify base output directory, default to the same
                    directory the pbuttons file is in (graphs are create in
                    a subdirectory)
```

## Experimental usage

Change to the base of your checked out yape directory and run:
```
bokeh serve --show yapesrv --args /Users/kazamatzuri/work/cases/898291/0503/squh-tc_TRAKCARE_20180503_000100_24hours_2_P1.html
```

This will give you (maybe) an interactive display of the pbuttons passed in. If you run into any errors, feel free to create an issue here: https://github.com/murrayo/yape/issues

## Related Discussion

See the detailed description and discussion [in this article](https://community.intersystems.com/post/yape-yet-another-pbuttons-extractor-and-automatically-create-charts).
Have a look at [InterSystems Developer Community](community.intersystems.com) to learn about InterSystems technology, sharing solutions and staying up-to-date on the latest developments.
