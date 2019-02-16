import numpy as np
import pygal

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


def pie_data(json):
    pie_chart = pygal.Pie()
    pie_chart.title = 'Types d\'actions'

    for action, n_action in json['actions'].items():
        pie_chart.add(action, n_action)
    
    render = pie_chart.render(is_unicode=True)
    feed = {
        "chart": render
    }

    return feed