from IPython import embed

def get_labels(path="labels.txt"):
    labels = []
    with open(path, 'r') as f:
        line = f.readline()
        line = line.split(',')
    for el in line:
        labels.append(el.strip())
    return labels

print(get_labels())
