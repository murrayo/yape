# yape 2
yet another pButtons extractor

Second revision. Complete rewrite based on the ideas and lessons learned of the first one. And yes, this is currently heavily in the alpha stage. Use at your own risk.

The goals for the rewrite are:
   * make it a one-step-process
   * add more interactivity with less waiting time
   * be able to handle bigger datasets


To avoid any fighting with python versions, this revision is strictly distributed as
docker image.

## Docker image
Currently published as kazamatzuri/yape2:latest

You can create your own with (you're on your own;)):
```
docker image build -t <yourname>/yape2 .
```
To run, go to the directory in which you find your pbuttons and run:
```
     docker container run --rm -it -p 5006:5006 -v `pwd`:/data kazamatzuri/yape2 /data/pbuttons.html
```

Over time we will add a wrapper to make this less awkward ;)
## Related Discussion

See the detailed description and discussion [in this article](https://community.intersystems.com/post/yape-yet-another-pbuttons-extractor-and-automatically-create-charts).
Have a look at [InterSystems Developer Community](community.intersystems.com) to learn about InterSystems technology, sharing solutions and staying up-to-date on the latest developments.
