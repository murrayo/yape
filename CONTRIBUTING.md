
# Contributing

We're excited about new contributors and want to make it easy for you to help improve this project. If you run into problems, please open a GitHub issue.

If you want to contribute a fix, or a minor change that doesn't change the API, go ahead and open a pull requests, see details on pull requests below.

If you're interested in making a larger change, we recommend you to open an issue for discussion first. That way we can ensure that the change is within the scope of this project before you put a lot of effort into it.


#Issues

We use GitHub issues to track bugs. Please ensure your description is clear and has sufficient instructions to be able to reproduce the issue.


# Developing

We use `black` to format code and keep it all consistent within the repo. With that in mind, you'll also want to install the precommit hooks because your build will fail if your code isn't black:
```
   pre-commit install
```

To run the test suite with the current version of Python/virtual environment, use nosetest:

```   
python setup.py nosetests
```


Pull Requests
-------------

1. Fork the repo and create your branch from ``master``.
2. If you've added code that should be tested, add tests.
3. If you've changed APIs, update the documentation.
4. Make sure you commit message matches something like `(chg|fix|new): COMMIT_MSG` so `gitchangelog` can correctly generate the entry for your commit.


Releasing to Docker Hub
-----------------

Jenkins handles releasing docker images to https://hub.docker.com/r/yape/yape/tags

Yape uses `semantic versions <https://semver.org/>`_. Once you know the appropriate version part to bump, use the ``bumpversion`` tool to bump the package version, add a commit, and tag the commit appropriately:


```
   git checkout master
   gitchangelog > CHANGELOG.md
   bumpversion patch
```
(it doesn't automatically commit the version bump changes to make it easier to verify)

Then push the new commit and tags to master:

```
   git push origin master --tags
```
Voila. 