# Mouvement U'nid
Notre solution consiste en un reporting automatique des informations renseignées par les bénévoles dans les gsheets. 
Notre pipeline s'articule comme suit: 
* Prétraitement des données:
  - conversion automatique des données du gsheet en données .csv et paramétrée par un scheduler (fréquence hbdomadaire)
  - filtering et conversion des données .csv en .json pour les analyses ultérieures
* Analyses statistiques des interventions et affichage sur notre interface web:
  - à l'échelle nationale
  - à l'échelle départementale
  - évolution chronologique
  - regroupement par type d'actions
  - comparatif bénévoles / personnes sensibilisées / prostituées rencontrées
  - systèmes de filtres pour isoler les statistiques souhaitées
* Envoi de mail automatique individualisée pour motiver les bénévoles et leur permettre d'avoir un suivi personnalisé de leurs actions
