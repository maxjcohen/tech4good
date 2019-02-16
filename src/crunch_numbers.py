import numpy as np
import pygal
from pygal.style import RedBlueStyle
import pandas as pd

custom_style = RedBlueStyle(background='transparent')


def text_data(json):

    n_prostitues = int(np.sum([[e for e in region.values()] for region in json['actions']['visites'].values()]))

    # n_benevoles = np.sum([region for region in json["visites"].values()])

    # n_sensibilises = np.sum([region for region in json["visites"].values()])

    # Return template filled with data
    feed = {
        "n_prostitues": n_prostitues,
        # "n_benevoles": n_benevoles,
        # "n_sensibilises": n_sensibilises
    }

    return feed


def pie_data(json):
    pie_chart = pygal.Pie(style=custom_style)
    pie_chart.title = 'Types d\'actions'

    for action, regions in json['actions'].items():
        sum_region = np.sum([region['total'] for region in regions.values()])
        pie_chart.add(action, sum_region)
    
    feed = {
        "chart": pie_chart.render(is_unicode=True)
    }

    return feed

def get_dic_prostitute(json_data,VISITE_PERMANENCE="prostitues"):

    dic_prostitues={}
    for departements in json_data['actions'][VISITE_PERMANENCE].keys():
        dic_prostitues[departements]=sum(json_data['actions'][VISITE_PERMANENCE][departements].values())

    return(pd.DataFrame.from_dict(dic_prostitues,orient='index'))

def get_indice_colors(nbr,code_dep):
    nb_pros_visite_df=pd.DataFrame(nbr)
    department_of_interest=list(nb_pros_visite_df.index) 

    nb_pros_visites=np.array(nb_pros_visite_df)

    for i in range(len(department_of_interest)):
        if (department_of_interest[i]=='Alpes-Maritime'):
            department_of_interest[i]='Alpes-Maritimes' 
        elif (department_of_interest[i]=='Essone'):
            department_of_interest[i]='Essonne' 
        elif (department_of_interest[i]=='Eure-et-Loire'):
            department_of_interest[i]='Eure-et-Loir' 
        elif (department_of_interest[i]=='Hauts-de-France'):
            department_of_interest[i]='Nord' 

    code_departement=[code_dep[name_dep] for name_dep in department_of_interest]
    ind_color={}
    for i in range(len(nb_pros_visites)):
        ind_color[code_departement[i]]=nb_pros_visites[i][0] 
    return(ind_color)
  


def map_data(json):
    FILE_NAME_INDIC_DEPARTMENT="src/indicateur_departement.csv"
    
    indic_dep=pd.read_csv(FILE_NAME_INDIC_DEPARTMENT,sep="\t")
    code_dep = dict(zip(indic_dep.Department,indic_dep.code))
    
    
    nb_pros_permanence=get_dic_prostitute(json,VISITE_PERMANENCE="permanences")
    nb_pros_rencontree=get_dic_prostitute(json,VISITE_PERMANENCE="visites")
    
    ind_color=get_indice_colors(nb_pros_permanence+nb_pros_rencontree,code_dep)
    
    fr_chart = pygal.maps.fr.Departments(style=custom_style, show_legend=False)
    fr_chart.title = 'Mouvement du Nid en France'
    fr_chart.add("",ind_color)

    feed={
        "map_chart": fr_chart.render(is_unicode=True)
    }

    return feed
