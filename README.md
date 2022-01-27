# Social Finance Digital Labs - Children's Services data synthesizer

This project aims to provide a one-stop shop for generating different kind of data from Children's Social Care. This can be configured
and used downstream to test tools that aim to work with real data.

For now, we only have support for generating the SSDA903 census - but this can be expanded in future.

The generation process is two-step:

1. Given a set of probabilities and a start date, end date, generate a list of children with various interactions throughout their life. This list is complete until their 18th birthday.
2. Take census snapshots given a specific set of dates for the census (so excluding any future events)


The data generated is unlikely to match all validation rules as much of it is randomly selected - but this may improve with time.

Eventually we will be able to simulate poor/missing data by adjusting step 2 to include random errors.

## What do I need?

Patience. And a few tools. Most importantly you need [Python][python]. Follow the links
to download a recent version and install this.

Next, we use [Poetry][poetry] for dependency management. Once you have
working python version installed, installing Poetry should be as easy as following
the steps on [this page][poetry-install].

However, it's not always that easy. If those steps don't work, download the installer
from [this link][poetry-script]. Find your downloaded file, and the launch it
by running `python install-poetry.py` where `install-poetry.py` is the name of the
downloaded file.

Now you are ready to check out this project. If you're not familiar with GIT, try
one of the many tutorials available online. For windows, I can recommend
[this one][git-tutorial].

Once you have checked out this repository, install the required libraries:

```shell
poetry install
```

You can now chose to either activate a poetry "shell" or prefix every command
with "poetry run". To activate a poetry shell, type:

```shell
poetry shell
```

For a basic generation workflow, you then run

```shell
python examples/<your command here>.py
```

# Contribution guidelines

There are plenty of open issues to improve the generation procedure - feel free to make a PR to solve any of these.

[python]: https://www.python.org/downloads/
[poetry]: https://python-poetry.org/
[poetry-install]: https://python-poetry.org/docs/master/#installation
[poetry-script]: https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py

[git-tutorial]: https://www.computerhope.com/issues/ch001927.htm
[github-fork]: https://docs.github.com/en/get-started/quickstart/fork-a-repo
