import datetime

import smtplib,glob,os
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

def get_plot(person,data,file1,file2):
    ## plot of work
    name=person
    data_sorted=data[data["test"]==name].iloc[:,2:6]
    data_sorted.columns=["type de mission","date","duree","fin"]
    temps_date=pd.to_numeric(data_sorted["fin"])-pd.to_numeric(data_sorted["duree"])
    data_sorted.duree=temps_date
    data_sorted=data_sorted.iloc[:,:-1]
    data_sorted["date"]=pd.to_datetime(data_sorted["date"])
    data_sorted=data_sorted.sort_values(by="date")
    perm = data_sorted.date.dt.to_period("M")  # new way to get the same
    gy = data_sorted.groupby(perm).sum()
    gy.plot(x=gy.index,y="duree")
    plt.title("Duree de travail du bénévole")
    plt.savefig("file1".format(person))

    total_heure_travaille=data_sorted.groupby(perm).sum().sum()
    moyenne_heure=total_heure_travaille/len(gy)
    
    
    ## Area of work

    x=pd.get_dummies(data_sorted["type de mission"])
    mult=data_sorted.duree
    z=pd.merge(x,pd.DataFrame(data_sorted,columns=["date"]),left_index=True, right_index=True)

    for domaine in ["Accompagnement","Formation","Prévention","Sensibilisation et plaidoyer","Rencontre"]:
        z[domaine]*=data_sorted.duree
    
        
    gy = z.groupby(perm).sum()
    
    fig, ax = plt.subplots()
    
    ax=gy.plot(ax=ax,x=gy.index,y="Accompagnement")
    ax=gy.plot(ax=ax,x=gy.index,y="Formation")
    
    ax=gy.plot(ax=ax,x=gy.index,y="Prévention")
    ax=gy.plot(ax=ax,x=gy.index,y="Sensibilisation et plaidoyer")
    ax=gy.plot(ax=ax,x=gy.index,y="Rencontre")
    plt.title("Analyse des domaine d'action du bénévole")
    plt.savefig("file2".format(person))
    return(total_heure_travaille,moyenne_heure)

def get_stat(data,domaine="Rencontre",region=False):
    data_domaine=data[data["Vous enregistrez une action de :"]==domaine].iloc[:,:12]
    if (region is not False):
        data_domaine=data_domaine[data_domaine["Votre délégation départementale"].isin(region)]
    #print(data_domaine.head())
    data_domaine["Quelle est la date de l'action que vous enregistrez ?"]=pd.to_datetime(data_domaine["Quelle est la date de l'action que vous enregistrez ?"])
    #print(data_domaine.head())
    data_domaine=data_domaine.sort_values(by="Quelle est la date de l'action que vous enregistrez ?")
    #print(data_domaine.columns)                                                            
    perm = data_domaine["Quelle est la date de l'action que vous enregistrez ?"].dt.to_period("M")
    #print(perm)
    gy = data_domaine.groupby(perm).sum()
    #print(gy.head())
    now = datetime.datetime.now()
    time_now = (now.year, now.month, now.day, now.hour, now.minute, now.second)[:2]
    actual_month="%d-%d"%(time_now[0],time_now[1])
    #print(gy.columns)
    #gy['2019-02']['Combien de personnes prostituées avez-vous rencontrées ?']
    nb_pro,nb_fem,nb_hom,nb_tra,nb_new=0,0,0,0,0
    
    if(actual_month in gy.index):
        nb_pro=gy[actual_month]["Combien de personnes prostituées avez-vous rencontrées ?"]
        nb_fem=gy[actual_month]['Parmi ces personnes, combien étaient des femmes ?']
        nb_hom=gy[actual_month]['Combien étaient des hommes (dont travestis) ?']
        nb_tra=gy[actual_month]['Et combien étaient des personnes trans ?']
        nb_new=gy[actual_month]['Parmi ces personnes rencontrées, combien en connaissiez-vous déjà?']
    return(nb_pro,nb_fem,nb_hom,nb_tra,nb_new)

def get_info_visite(person,data,domaine="Rencontre"):
   
    tnb_pro,tnb_fem,tnb_hom,tnb_tra,tnb_new=get_stat(data,domaine,region=False)
    var_exp=str("Ce mois ci, dans toute la France %d prostituees on ete rencontrees, dont %d femmes, %d hommes et %d personnes transexuelles. La communaute Mouvement Du Nid a aussi rencontre %d nouvelles prostituees"%(tnb_pro,tnb_fem,tnb_hom,tnb_tra,tnb_new))    
    region_pers=data_domaine[data_domaine["test"]==person]["Votre délégation départementale"].unique()
    if(len(region_pers)==0): 
        return var_exp
    elif(len(region_pers==1)):
        var_exp+=' Vous avez travaillé dans le département suivant : %s. Voici des informations plus précises concernant les performances de votre département.'%region_pers[0]
    elif(len(region_pers>1)):
        var_exp+=' Vous avez travaillé dans les départements '
        for reg in region_pers:
            var_exp+=("%s "%region_pers)
        var_exp+=" Voici des informations plus précises concernant les performances de ces départements.\n \n"
    nb_pro,nb_fem,nb_hom,nb_tra,nb_new=get_stat(data,domaine,region=region_pers)
    var_exp+="%d prostituees on ete rencontrees, dont %d femmes, %d hommes et %d personnes transexuelles. La communaute Mouvement Du Nid a aussi rencontre %d nouvelles prostituees."%(nb_pro,nb_fem,nb_hom,nb_tra,nb_new)    
    var_exp+="Ces département représentent %.3F %% de MVT et nous en sommes très fier"%(np.float(nb_pro)/np.float(tnb_pro))   
    return(var_exp)


def get_stat_acc(person,data,domaine="Accompagnement",region=False):
    data_domaine = data.drop(data.columns[[6,7,8,9,10,11,12]], axis=1)
    if (region is not False):
        data_domaine=data_domaine[data_domaine["Votre délégation départementale"].isin(region)]
    #print(data_domaine.head())
    data_domaine["Quelle est la date de l'action que vous enregistrez ?"]=pd.to_datetime(data_domaine["Quelle est la date de l'action que vous enregistrez ?"])
    #print(data_domaine.head())
    data_domaine=data_domaine.sort_values(by="Quelle est la date de l'action que vous enregistrez ?")
    #print(data_domaine.columns)                                                            
    perm = data_domaine["Quelle est la date de l'action que vous enregistrez ?"].dt.to_period("M")
    #print(perm)
    gy = data_domaine.groupby(perm).sum()
    #print(gy.head())
    now = datetime.datetime.now()
    time_now = (now.year, now.month, now.day, now.hour, now.minute, now.second)[:2]
    actual_month="%d-%d"%(time_now[0],time_now[1])
    #print(gy.columns)
    #gy['2019-02']['Combien de personnes prostituées avez-vous rencontrées ?']
    nb_pro,nb_fem,nb_hom,nb_tra,nb_new=0,0,0,0,0
    if(actual_month in gy.index):
        nb_pro=gy[actual_month]['Combien de personnes ont été accueillies au cours de la permanence ?']
        nb_fem=gy[actual_month]['Parmi ces personnes, combien étaient des femmes ?.1']
        nb_hom=gy[actual_month]['Combien étaient des hommes (dont travestis) ?.1']
        nb_tra=gy[actual_month]['Et combien étaient des personnes trans ?.1']
    return(nb_pro,nb_fem,nb_hom,nb_tra)

def get_info_visite_acc(person,data,domaine="Accompagnement"):
   
    tnb_pro,tnb_fem,tnb_hom,tnb_tra=get_stat_acc(person,data,domaine,region=False)
    var_exp=str("Ce mois ci, dans toute la France %d prostituees ont sohaité être accompagnées, dont %d femmes, %d hommes et %d personnes transexuelles."%(tnb_pro,tnb_fem,tnb_hom,tnb_tra))    
    region_pers=data_domaine[data_domaine["test"]==person]["Votre délégation départementale"].unique()
    if(len(region_pers)==0): 
        return var_exp
    elif(len(region_pers==1)):
        var_exp+=' Vous avez travaillé dans le département suivant : %s. Voici des informations plus précises concernant les performances de votre département.'%region_pers[0]
    elif(len(region_pers>1)):
        var_exp+=' Vous avez travaillé dans les départements '
        for reg in region_pers:
            var_exp+=("%s "%region_pers)
        var_exp+=" Voici des informations plus précises concernant les performances de ces départements.\n \n"
    nb_pro,nb_fem,nb_hom,nb_tra=get_stat_acc(person,data,domaine,region=region_pers)
    var_exp+="%d prostituees sont venus dans nos locaux dont %d femmes, %d hommes et %d personnes transexuelles."%(nb_pro,nb_fem,nb_hom,nb_tra)    
    var_exp+="Ces département représentent %.3F %% de MVT et nous en sommes très fier"%(np.float(nb_pro)/np.float(tnb_pro))   
    return(var_exp)


def send_mail_benevole(filename,filename2,visites,accomp,person_name,mail):
    msg = MIMEMultipart()
    msg['Subject'] = "Votre report d'activité mensuel"
    me = 'bastinflorian1@gmail.com'
    family = 'bastinflorian1@gmail.com'
    msg['From'] = me
    msg['To'] = family
    #msg.preamble = "Cher %s, \n Tout d'abord nous tenons a vous remercier pour votre investissement au sein de l'association Mouvement Du Nid.\nVous trouverez en piece jointe le report d'activite de ce mois ci." %person_name
    txt="Cher %s, \n\nTout d'abord nous tenons a vous remercier pour votre investissement au sein de l'association Mouvement Du Nid.\nVous trouverez en piece jointe le report d'activite de ce mois ci.\n\n" %person_name
    txt+="Concernant le domaine des visites: \n\n"
    
    txt+=visites+".\n"
    
    txt+="Concernant le domaine des accompagnements: \n\n"
    txt+=accomp
    
    
    filename='/Users/newuser/Documents/Hackathon_margo/res_benevole/DureedetravaildubénévolePrénom26.png'
    filename2='/Users/newuser/Documents/Hackathon_margo/res_benevole/AnalysedesdomainedactiondePrénom26.png'

    msg.attach(MIMEText(txt))
               
    fp = open(filename, 'rb')
    img = MIMEImage(fp.read())
    img.add_header('Content-Disposition', "attachment; filename= %s" % "Votre investissement chez nous.png")
    fp.close()
    msg.attach(img)

    fp = open(filename2, 'rb')
    img = MIMEImage(fp.read())
    img.add_header('Content-Disposition', "attachment; filename= %s" % "Vos domaines d'investissement.png")
    fp.close()
    msg.attach(img)

    # Send the email via our own SMTP server.
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.ehlo()
    s.starttls()

    s.login(me,'Yomoma1111')

    s.sendmail(me, family, msg.as_string())
    s.quit()
    
def send_mail(person="Prénom26"):   
    filename1="im1.png"
    filename2="im2.png"

    NAME_DATA_FILE="/Users/newuser/Documents/Hackathon_margo/data.csv"
    data=pd.read_csv(NAME_DATA_FILE,sep="\t")
    data=data.fillna(0)
    data=data.iloc[:,1:]
    var_exp=get_info_visite(person,data,domaine="Rencontre")
    var_exp_acc=get_info_visite_acc(person,data,domaine="Accompagnement")
    heure_travail,moyenne_heure=get_plot(person,data,filename1,filename2)   
    send_mail_benevole(filename,filename2,var_exp,var_exp_acc,person_name="Florian Bastin",mail="bastinflorian1@gmail.com")
