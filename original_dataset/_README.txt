The labeled-dataset.tsv file is what we shared with the WWW publication on the github repo: https://github.com/minjechoi/10dimensions/blob/master/data/labeled-dataset.tsv

Anders parsed this data into json format, with a train-test split.

There is an additional 1k examples from an earlier annotation round that I believe we used in the experiments (see preliminary_collection.tsv). The format is slightly different though, as it  includes for example the whole text given by crowdworkers, with a <mark> tag indicating the highlighted portion of the text that annotators were supposed to label.

Sadly, it seems that we don't have annotator IDs :(