# Changelog


## (unreleased)

### Changes

* Update line style choices in config file. [murrayo]

### Fix

* Reinstate config file, make some more changes to smarter x and y axis. [murrayo]

* Solve for yyyy dates and yy dates or bail out. [murrayo]

### Other

* Doc: Update readme. [murrayo]

* Doc: bump version. [murrayo]


## 2.2.3 (2019-06-03)

### Changes

* Positional arg pButtons html or zip file name NOT required if passing filedb and skip-parse. [murrayo]

### Other

* Doc: Update change log ahead of version bump. [murrayo]

* Default output directory if using previously created database (--skip-parse) [murrayo]

* Doc: Update readme with parameter details. [murrayo]

* Doc: bump version. [murrayo]


## 2.2.2 (2019-05-17)

### Changes

* Some tidy up on the date format for multi-day charting. [murrayo]

* Added device name to chart title for iostat and sar chg: bit more tidy up on date/time handling for charts. [murrayo]

* Updated date handling. [murrayo]

### Other

* Doc: black latest changes. [murrayo]

* [fix] Fixed problem with sar on red hat not charting properly. [murrayo]

* Doc: Bump Version. [murrayo]


## 2.2.1 (2019-05-06)

### Changes

* Some massaging of the chart output to make more consistent and readable. Update AIX formats. Black code. [murrayo]

### Other

* Doc: Updated changelog. [murrayo]

* Quite a lot of updates. - Some layout changes to the charts to make them a bit nicer for reports etc, including adding dates to the heading and some smarter x and y axis - vmstat now produces a Total CPU chart so you don't need to stand on your head and read the id chart. - Added some logic for AIX based on reports of failures. To be honest, I wouldnt be surprised if this caused some other AIX to fail... if so, sorry, please let me know. [murrayo]

* Updated format y axis of vmstat (us, sy, wa) to 100 top, and numbers greater than 1,000. [murrayo]

* Update readme for anaconda. [murrayo]

* Update so that bokeh works with anaconda. [murrayo]

* Merge pull request #19 from murrayo/Adding-styles-to-charts. [murrayo]

  Adding styles to charts

* Merge branch 'master' of https://github.com/murrayo/yape into Adding-styles-to-charts. [murrayo]

  # Conflicts:
  #	yape/plotpbuttons.py

* Merge branch 'master' of github.com:murrayo/yape. [Fabian]

* Merge pull request #15 from kazamatzuri/master. [Fabian]

  doc: add github hint

* Doc: add github hint. [Fabian]

* Fix version indication for black. [Fabian]

* Doc: fix formatting in contributing. [Fabian]

* Doc: versioning adjustment, no auto commit. [Fabian]

* Make charts dot chart to see effects, others may follow. [murrayo]


## 2.2.0 (2019-02-27)

### Changes

* Hooked up black with pre-commit semantic versioning contributing document. [Fabian]

### Fix

* Version numbering config. [Fabian]

### Other

* Bump version: 2.1.0 → 2.2.0. [Fabian]

* Bump version: 2.0.8 → 2.1.0. [Fabian]

* Going black. [Fabian]


## 2.0.8 (2019-02-20)

### Other

* Fix sar-u plotting on hp-ux; implement sar-u plotting. [Fabian]

* Pep8 compliance. [Fabian]


## 2.0.7 (2019-02-06)

### Other

* Prevent scientific notation. [Fabian]


## 2.0.5 (2018-12-31)

### Other

* Syntax errors ... [Fabian]

* Declarative pipeline update. [Fabian]


## 2.0.4 (2018-12-31)

### Other

* Added jenkins agent label. [Fabian]


## 2.0.3 (2018-12-31)

### Other

* Pipeline, jenkins docker file. [Fabian]

* Jenkinsfile, updated readme. [Fabian]

* Remove dind. [Fabian]

* Try just building. [Fabian]

* Names.. [Fabian]

* Gitlab pipeline 1st attempt. [Fabian]


## 2.0.2 (2018-11-30)

### Other

* Improve error message when parsing bad mgstat data. [Fabian]

* Vscode configs. [Fabian]

* Add entrypoint for debugging. [Fabian]

* Updated readme, fixed reference to docker image and link. [Fabian]

* Fix old version lookup. [Fabian]

* Updated readme. [Fabian]

* Docker image build updates. [Fabian]


## 2.0.0 (2018-10-09)

### Other

* Versioning stuff. [Fabian]

* Eporting parse_args. [Fabian]

* Updated readme. [Fabian]

* Making dot graphs configurable in the config file. [Fabian]

* Fix conditional to make sure minor time ticks are rendered. [Fabian]

* Adding ds_store to local gitignore. [Fabian]

* Added rsec/s,wsec/s. [Fabian]

* Added special case for ubuntu vmstats ... [Fabian]

* Fixed readme for pwd format that works on mac. [murrayo]

* Added yaml to dependencies, was breaking container. [Fabian]

* Fix iostat plotting on some redhat linux with missing timestamps. [Fabian]

* Deal with 2016.2.3 pbuttons stuff; passed tests. [Fabian]

* Handle empty line in some 2016.1.x rh mgstat sections. [Fabian]

* Extend unittest to also plot stuff; set default config for unittests to smaller output size, to speed up testing. [Fabian]

* Moved example config to root dir. [Fabian]

* Add configuration option for output figure size and example config; added section in readme. [Fabian]

* Added support for configuration file; ignoring pbuttons in testdata/* [Fabian]

* Moved testdata dir to main repo, no need to have submodule if we're not keeping the data there. [Fabian]

* Testdata. [Fabian]

* Remove submodule. [Fabian]

* Fleshed out unit test parsing of files in yape-testdata; currently runs for 80s, will need to add some status msg. [Fabian]

* Fix error parsing mac pbuttons with empty sections. [Fabian]

* Adding support for a single html file in a zipfile. [Fabian]

* Added testdata submodule. [Fabian]

* Started implementing args parser unittests, started work on testing parsing of pbuttons. [Fabian]

* Refactor args parsing to facilitate testing. [Fabian]

* Groundwork for including tests. [Fabian]

* Fix parsing of text sections. [Fabian]

* Fixed debug logging statements; fixed osmode detection (bad indents); fixed sar-d for linux. [Fabian]

* Merge branch 'master' of github.com:murrayo/yape. [Fabian]

* Change Dockerfile to use python 3 latest (3.7) [murrayo]

* Fix variable name issue in fileout_splitcols. [Fabian]

* Remove double passing of filename to fileout* methods. [Fabian]

* Fix read me. [murrayo]

* Tidy up readme. [murrayo]

* Tidy up readme. [murrayo]

* Fix broken csv output from refactor. [murrayo]

* Fixed Dockerfile and README. [murrayo]

* Fix iostat not working after parameter passing refactor. [murrayo]

* Removing yapeserve dockerfile, it was not working anyways; adding dockerfile for regular yape, updated readme. [Fabian]

* Fix y axis to not use exponents. [murrayo]

* Limit y axis precision. [Fabian]

* Refactoring in parsing code, reductionof code duplication. [Fabian]

* Introduce quiet switch; get rid of print statements in favor of proper logging. [Fabian]

* Merge branch 'master' of github.com:murrayo/yape. [Fabian]

* Updated readme to reflect current setup. [murrayo]

* Fix Docker file for current file structure. [murrayo]

* Introducing config dictionary to cleanup method signatures. [Fabian]

* Vms. [Fabian]

* Working further on vms monitor support. [Fabian]

* Add layer in plotting to prepare for multiprocessing plots for general speedup. [Fabian]

* Handle missing mgstat output gracefully. [Fabian]

* Inlcude all devices for vms. [Fabian]

* First iteration of VMS monitor disk data parsing and plotting. [Fabian]

* Rotate minor labels when timeframe is specified. [Fabian]

* Prefix typo, added clarification in help. [Fabian]

* Fix typo in perfmon parameter. [Fabian]

* Add ability to graph sar-d. [Fabian]

* Fix sar-d parsing. [Fabian]

* Fixing vmstat for hpux. [Fabian]

* Work towards supporting hp-ux pbuttons, (iostat gets ignored for now) [Fabian]

* Fixed bug introduced in plotDisks. [murrayo]

  my bad

* Merge pull request #9 from murrayo/select_disks_for_iostat. [murrayo]

  Add select disks to plot

* Add select disks to plot. [murrayo]

  If entered --plotDisks "some disks" will only plot disks in list (string)

* Merge pull request #8 from murrayo/2.0_filenames_sorting. [murrayo]

  2.0 filenames sorting

* Add prefix option to charts. [murrayo]

  Also add prefix option to output png file

* Add prefix to csv output. [murrayo]

  Allow prefix option for csv file output, useful when dealing with multiple instance, eg iris master and shards

* Change help. [murrayo]

* Select_file_prefix. [murrayo]

  Add file prefix to output files

* Get github in synch with my local, small changes only. extract: Fix path for iostat output. graph: change  BokehChart  vmstat simply await to r_await and w_await. peakavg: set option for output path. [Murray Oldfield]

* Merging some changes from kazamatzuri/yape. [Fabian]

* Merge branch 'master' of github.com:murrayo/yape. [Fabian]

  fixing conflictsg

* Some small grammer. [Murray Oldfield]

* Grammer change. [Murray Oldfield]

* Get github in synch with my local, small changes only. extract: Fix path for iostat output. graph: change  BokehChart  vmstat simply await to r_await and w_await. peakavg: set option for output path. [Murray Oldfield]

* Merge pull request #2 from murrayo/dev. [Fabian]

  merging some changes from kazamatzuri/yape

* Merging some changes from kazamatzuri/yape. [Fabian]

* Tidy and a few bug fixes. [murrayo]

* Updated python version. [murrayo]

* Merge branch '2.0' [Fabian]

* Add documentation for week overview graphs. [Fabian]

* Make plotting week overviews possible; fix typo in perfmon parameter. [Fabian]

* Fix another if condition with timeframe. [Fabian]

* Fix iostat date parsing for Cache for UNIX (Red Hat Enterprise Linux for x86-64) 2015.1.1 (Build 505_0_15557U) Wed Aug 19 2015 16:13:34 EDT. [Fabian]

* Prevent slashes from ending up in filenames of graphs. [Fabian]

* Fix timeframe conditionals. [Fabian]

* Make widget-box scroll when their too big (i.e. perfmon) [Fabian]

* Added timeframe mode that allows passing in a timeframe to be plottet. [Fabian]

* Movie output print statement for better debugging; fix last column of perfmon parsing. [Fabian]

* Making picture a little bit bigger (labels were messed up); adding perfmon plotting) [Fabian]

* Add missing column type definitions; chunking of inserts for minor performance gain. [Fabian]

* Minor performance improvements, +12% speed parsing big pbuttons. [Fabian]

* Merge branch '2.0' of github.com:murrayo/yape into 2.0. [Fabian]

* Merge branch '2.0' of https://github.com/murrayo/yape into 2.0. [Murray Oldfield]

  * '2.0' of https://github.com/murrayo/yape:
    fixed vmstat plotting/parsing for Solaris on sparc-64

* Reformat default plot styles. Smaller plot for faster execution, add grid, zero start y axis, default format y axis. [Murray Oldfield]

* Add ability to pass existing sqlitedb and skip parsing step. [Fabian]

* Fixed vmstat plotting/parsing for Solaris on sparc-64. [Fabian]

* Updated .gitignore to exclude pycharm project files. [Murray Oldfield]

* Remove references to unused holoviews module in yapesrv. [Murray Oldfield]

* Added newline. [Fabian]

* Plotting iostat data. [Fabian]

* Update readme. [Fabian]

* Minor refactoring; improving description in help text; adding profiler option. [Fabian]

* Csv export per device. [Fabian]

* Added vmstat plotting; simple refactorings. [Fabian]

* Mgstat plotting. [Fabian]

* Added section about experimental features. [Fabian]

* Updated readme to current capabilities. [Fabian]

* Csv output perfmon. [Fabian]

* Removed references to docker to avoid confusion. [Fabian]

* Added temp/ to gitignore; added csv output option for mgstat,vmstat,iostat,sar-d,sar-u. [Fabian]

* Moved bokeh server to yapesrv, removed datashader/holoviews requirements, not being used atm. [Fabian]

* Created package definition, moved bokeh frontend out of it, added --filedb argument. [Fabian]

* Webgl backend, various little fixes, adding more sunos fixes. [Fabian]

* Fix tabbing. [Fabian]

* Handle partial pbuttons in cstat tab; fix typo in ss_tab. [Fabian]

* Handle partial pbuttons in ss tab. [Fabian]

* Partial work toward supporting solaris pbuttons (iostat, sar -u, sar -d needed adjustments) [Fabian]

* Makeing vmstat columns selectable. [Fabian]

* Made perfmon columns selectable; moved perfmon legend outside of graph. [Fabian]

* Mgstat columns selectable. [Fabian]

* Minor stuff. [Fabian]

* Added perfomn. [Fabian]

* Adding windows tasklist support. [Fabian]

* Added windowsinfo. [Fabian]

* Deal with non-existent sections. [Fabian]

* Adding cstat -D. [Fabian]

* Adding pyc to gitignore. [Fabian]

* Adding iostat scripts. [Fabian]

* Added iostat parsing/plotting; remove pycache stuff from repo. [Fabian]

* Fix typo in fdisk-l parsing. [Fabian]

* Add url. [Fabian]

* Initial checkin. [Fabian]

* Indents. [Fabian]

* Fix indents. [Fabian]

* Merging Murrays stuff. [Fabian]

* Aix test fix. [Fabian]

* Typo in extract. [Fabian]

* Removed conditional formatting to avoid errors with some reports (just until we have a better solution) [Fabian]

* Simplify calling; updated readme. [Fabian]

* Fix formatting. [Fabian]

* Replaced os.rename with shutil.move replaced building paths with os.path.join added -o,--out to both extract_pButtons and graph_pButtons to specify absolute output directory added Dockerfile added requirements for python modules in docker image. [Fabian]

* Updated examples to show week view. [Murray Oldfield]

* Updated readme. [Murray Oldfield]

* Updated readme again. [Murray Oldfield]

* Updated readme. [Murray Oldfield]

* Updated readme. [Murray Oldfield]

* Added shell script to make it easy to graph multiple days. Also graph will show day of the week if more than one day. [Murray Oldfield]

* Added date to interactive files. [Murray Oldfield]

* Added milliseconds to some graphs. [Murray Oldfield]

* Some reformat and tidy up. Revert vmstat id, added ‘Total CPU’ [Murray Oldfield]

* Additional interactive combination charts. [Murray Oldfield]

* Some tidy up. Add reference e.g. iostat disk name to chart title. [Murray Oldfield]

* Tidy as per pyCharm recommendations. [Murray Oldfield]

* Invert vmstat ‘id’ to be Total CPU Utilization (100-id) [Murray Oldfield]

* More informative output. [Murray Oldfield]

* Fix bug iostat, add -[t]itle parameter. [Murray Oldfield]

* Removed version info. [Murray Oldfield]

* Removed version info. [Murray Oldfield]

* Tidy up time display. [Murray Oldfield]

* Updated readme to show now using Python 3.6. [Murray Oldfield]

* Updated to include direction to community. [Murray Oldfield]

* Updated comments. [Murray Oldfield]

* Updated descriptions. [Murray Oldfield]

* Added community details. [Murray Oldfield]

* Added comments for Windows perfmon. [murrayo]

* Update README.md. [murrayo]

* Example output - interactive. [murrayo]

* Update README.md. [murrayo]

* Added prefix for output, bokeh html output, choose chart style. [murrayo]

* Command line option for prefix. [murrayo]

* Update README.md. [murrayo]

* Update README.md. [murrayo]

* Better win perfmon support, changed default to subset. [murrayo]

  Windows perfmon is the Wild West. This could get ugly.
  Changed default to charting to just a subset of key metrics. --kitchen_sink option if you want every column

* Update README.md. [murrayo]

* Fixed bug in charts. [murrayo]

  for AIX vmstat and when no index

* Update README.md. [murrayo]

* Update README.md. [murrayo]

* Update README.md. [murrayo]

* Update README.md. [murrayo]

* Update README.md. [murrayo]

* Update README.md. [murrayo]

* Update README.md. [murrayo]

* Update README.md. [murrayo]

* Update README.md. [murrayo]

* Update README.md. [murrayo]

* Update all areas. [murrayo]

  Major refactor and add features

* Update all areas. [murrayo]

  This is a big refactor

* Update README.md. [murrayo]

* Update README.md. [murrayo]

* Update README.md. [murrayo]

* Update README.md. [murrayo]

* Update graph_pButtons.py. [murrayo]

* Delete .gitignore. [murrayo]

* Update README.md. [murrayo]

* Update README.md. [murrayo]

* Update README.md. [murrayo]

* Update README.md. [murrayo]

* Update README.md. [murrayo]

* Update README.md. [murrayo]

* Add files. [murrayo]

* Initial commit. [murrayo]


