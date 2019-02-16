import numpy as np
import pygal
import pandas as pd

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

def get_dic_prostitute(json_data,VISITE_PERMANENCE="prostitues"):

    dic_prostitues={}
    for departements in json_data[VISITE_PERMANENCE].keys():
        dic_prostitues[departements]=sum(json_data[VISITE_PERMANENCE][departements].values())

    return(pd.DataFrame.from_dict(dic_prostitues,orient='index'))

def get_indice_colors(nb_pros_rencontree,nb_pros_permanence,code_dep):
    nb_pros_visite_df=pd.DataFrame(nb_pros_rencontree+nb_pros_permanence)
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
        ind_color[code_departement[i]]=nb_pros_visites[i] 
    return(ind_color)

def get_france_map(ind_color,FILE_NAME_FRANCE_MAP):

    fr_chart = pygal.maps.fr.Departments()
    fr_chart.title = 'Présence de Mouvement Du Nids en France'
    fr_chart.add("",ind_color) 
    return fr_chart.render()
    


def map_data(json):
    
    FILE_NAME_INDIC_DEPARTMENT="src/indicateur_departement.csv"
    
    indic_dep=pd.read_csv(FILE_NAME_INDIC_DEPARTMENT,sep="\t")
    code_dep = dict(zip(indic_dep.Department,indic_dep.code))
    
    
    nb_pros_permanence=get_dic_prostitute(json,VISITE_PERMANENCE="prostitues")
    nb_pros_rencontree=get_dic_prostitute(json,VISITE_PERMANENCE="prostitues")
    
    ind_color=get_indice_colors(nb_pros_rencontree,nb_pros_permanence,code_dep)
    render=get_france_map(ind_color,FILE_NAME_FRANCE_MAP)
    feed={"map_chart":render}
    return feed
