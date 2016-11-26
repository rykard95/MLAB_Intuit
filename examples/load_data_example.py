#!/usr/bin/env python

from pickle import load

if __name__ == "__main__":
    with open('intuit_data', 'rb') as f:
        data = load(f)

    # data is a dictionary with fields:
    #   `data`  => list of emails
    #   `label` => list of labels
    #   `stats` => counts of emails
    #   `label[i]` corresponds to `data[i]`
    email = data['data'][0]
    label = data['label'][0]
    stats = data['stats']

 
