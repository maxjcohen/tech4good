import numpy as np

def text_data(json):

    n_prostitues = np.sum([[prostitue for prostitue in json["prostitues"][region].values()] \
        for region in json["prostitues"]])

    n_benevoles = np.sum([region for region in json["benevoles"].values()])

    n_sensibilises = np.sum([region for region in json["sensibilises"].values()])

    # Return template filled with data
    feed = {
        "n_prostitues": n_prostitues,
        "n_benevoles": n_benevoles,
        "n_sensibilises": n_sensibilises
    }

    return feed