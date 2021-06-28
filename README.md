# Social Finance Digital Labs - Children's Services data synthesizer

This project aims to provide a one-stop shop for generating different kind of data from Children's Social Care. This can be configured
and used downstream to test tools that aim to work with real data.

For now, we only have support for generating the SSDA903 census - but this can be expanded in future.

The generation process is two-step:

1. Given a set of probabilities and a start date, end date, generate a list of children with various interactions throughout their life. This list is complete until their 18th birthday.
2. Take census snapshots given a specific set of dates for the census (so excluding any future events)


The data generated is unlikely to match all validation rules as much of it is randomly selected - but this may improve with time.

Eventually we will be able to simulate poor/missing data by adjusting step 2 to include random errors.

# Installation and example usage

Checkout the repo, and run

```
pip install .
```

For a basic generation workflow, you then run

```
<code to follow>
```

# Contribution guidelines

There are plenty of open issues to improve the generation procedure - feel free to make a PR to solve any of these.