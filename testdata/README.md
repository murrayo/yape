# yape-testdata

To avoid fees, we are storing test-pbuttons in /scratch1/fhaupt/yape-testdata. (Otherwise we'd need to use git-lfs for these files).

you can sync them with the included sync script. (I'll keep this as submodule, maybe we want to include 1min test-pbuttons here at some point)

```
./sync
```


For now I'm using lx6 as remote host, so it helps to make an entry in your ~/.ssh/config file like this:
```
Host lx6
        User fhaupt
```


Alternatively you can also run the rsync command directly like this:
```
rsync -av --progress fhaupt@lx6:/scratch1/fhaupt/yape-testdata/* .
```
