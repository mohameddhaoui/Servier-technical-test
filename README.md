
# Servier-technical-test

Le rendu du test technique pour Servier - Mohamed DHAOUI


## 1- Workflow global du projet

Le repo est organisé comme ci-dessous :

    |── bin
    |───── run_drugs_relations_pipeline.py
    |── configurations
    |── data
    |── lib
    |─────helpers
    |─────utils
    |─────modules
    |───────── data_prep
    |───────── data_transfer
    |───────── data_transformation
    |───────── data_exposition
    |── sql
    |── tests

-----------

Le point d'entrée du repo est le fichier `run_drugs_relations_pipeline.py`,  permet de déclencher le data pipeline de génération du json contenant les relations des  drugs avec les journaux et les pubmed. Le pipeline exécute les traitements suivants :
- **La data préparation** : retrouver les fichiers sources à traiter, les transférer dans une zone quarantaine, vérifier leurs qualités et les pré-processer. Le résultat de cette étape sera sauvegardé dans le dossier `data/preprocessed` et on obtient comme output les paths de ces fichiers.
Exemple de format d'output
> {'drugs': './data/preprocessed/drugs.csv', 'clinical_trials':
> './data/preprocessed/clinical_trials.csv', 'pubmed':
> './data/preprocessed/pubmed.csv'}

- **La data transformation** :  on charge les données pré-processées et générées par l'étape précédente et on applique une série des traitement pour produire un json contenant les relations des drugs avec `pubmed`et un autre pour les relations avec `clinical_trials`
Exemple de format d'output:

> {'clinical_trials': './data/exposition/drugs_clinical_trials.json',
> 'pubmed': './data/exposition/drugs_pubmed.json'}
 1. La data exposition : on charge les fichiers json générés par l'étape précédentes et on les traite et fusionne pour généré le fichier json final contenant permettant de determiner les relations des drugs avec les journaux , les pubmed et les clinical_trials.
une observation dans le fichier json produit a le format ci-dessous:

    {"id_relation": "id_mention", "date", "journal","type", "drug_name', "drug_attcode"}
    id_relation : une clé composée de l'id de mention avec l'id du drug  id_mention : l'id de titre contenant la mention du drug date : date  de mention journal : journal qui a mentionné le drug type : type de  mention, soit "pubmed" , soit "clinical_trials"

**Le format de json proposée permet de :**
- Connaitre les relations des médicaments avec les pubmed , en filtrant sur le champ `type`
- Connaitre  les  relations des médicaments avec les clinical_trials , en filtrant sur le champ `type`
- Connaitre les relations des medicaments avec les journaux, en utilisant  les champs `journal`, `date` et `drug_name`

NB : L'inconvenient de ce format de json  est le traitement de la relation entre les journaux et les médicaments: un journal peut  mentionner un drug plusieurs fois le meme jour, cela engendrera plusieurs observations dans notre json et il faudra traiter ce scénario dans l'import du json.

{"NCT01967433-A04AD": {"id": "NCT01967433", "date": "2020-01-01", "journal": "Journal of emergency nursing", "type": "clinical_trials", "drug_name": "DIPHENHYDRAMINE", "drug_atccode": "A04AD"}


## 2- Data pipeline
Le pipeline de données se repose sur le fichier de configuration se trouvant dans `configurations/..._datasrc_config.yaml` :
Le fichier contient les paramètres de toutes les étapes de notre data pipeline.

- **Data Preparation** :  Le code principal de ce traitement se trouve dans `lib/modules/data_prep/data_preparation_pipeline.py` : On commence par chercher les fichiers qui correspondent au regex du fichier de config, ensuite on exécute un pipeline de data_quality "assez basique" et enfin  on nettoie les données ( traitement des Nans, des types, des caractères spéciaux) .
Ce traitement peut etre exécuté en parallèle/en chunk par type de fichiers ( drugs, clinical_trials, pubmed)
- **Data transformation** : Le code principal de ce traitement se trouve dans `lib/modules/data_transformation/data_transformation_pipeline.py`. On se contente de traiter les les fichiers générés par la dataprep pour générer un json par type de relation ( "clinical_trials", "pubmed")
- **Data Exposition** : Le code principal de ce traitement se trouve dans `/lib/modules/data_exposition/data_exposition_pipeline.py` : On récupère les données transformées, on le traite , fusionne et exporte sous un format json. On calcule ensuite les indicateurs de la section `4. Traitement ad-hoc`, dans notre cas c'est le journal contenant le plus de mentions d'articles différents

## 3- Comment executer le script
Pour pouvoir executer le script :
 - Il faut set un virtualenv et l'activer
 - Nettoyer les fichiers d'outputs existants :  `make init_pipeline`
- Exécuter le pipeline : `make run_pipeline`

Le résultat aura cette forme :

> ({'json_drugs_relations_path':
> './data/exposition//drugs_all_mentions.json'},
> {'journal_max_mentions': 'Psychopharmacology'})

Le fichier json se trouvera dans `./data/exposition//drugs_all_mentions.json` et le journal ayant le plus de mentions est `Psychopharmacology`

## 4- Réponses aux questions  de la section "Python et Data Engineering"


> Quels sont les éléments à considérer pour faire évoluer votre
> code afin qu’il puisse gérer de grosses volumétries de données
> (fichiers de plusieurs To ou millions de fichiers par exemple) ?

 Pour pouvoir traiter des grosses volumétries des données, on peut envisager les améliorations suivantes :
 - Ajout de la feature de lecture et traitement en chunk des données
 - Utiliser un mécanisme de mapreduce manuel : on découpe les fichiers sources ( pubmed et clinical_trials ) en plusieurs fichiers de taille gérable , on lance le traitement par fichiers  et on prévoit une brique de reduce et de fusion avant la couche d'exposition
 - On utilise des bibliothèques/framework de traitement parallèle des dataframes et des données : (Dask, Rapids, Numba), Pyspark
 - On utilise des outils cloud managés pour l'éxecution de étapes de workflow ( kubernetes, Dataflow )

Pour le traitement de millions de fichiers, il faut rendre les briques du pipeline le plus `stateless` possible et découpler au maximum les étapes ( architecture `micro-services` ) . Cela permettra d'utiliser des briques de traitement serverless par un/groupe de fichiers  ( lambda function, cloud function, cloud ru ...)


## 5- Réponses aux questions  de la section SQL:

Les fichiers sql se trouvent dans le dossier `sql` du repo.

**Pour la première partie du test :**
On génère une table contenant les dates du 01/01/2019 au 31/12/2019, **jour par jour**. Ensuite on fait la jointure avec la table transaction sur la date et on aggrège sur le produits ( product_price *product_quantity)


    WITH  RECURSIVE dates(date) AS (
	    VALUES('2019-01-01')
	    UNION ALL
	    SELECT  date(date, '+1 day')
	    FROM dates
	    WHERE  date  <  '2019-12-31'
     )

    SELECT  DT.date  as  date, IFNULL(sum( TR.prod_price* TR.prod_qty),0) as ventes FROM dates DT

    left join TRANSACTIONS TR
    ON  DT.date=TR.date

    group by  DT.date


**Pour la seconde partie :**

On fait la jointure entre la table TRANSACTIONS et la table PRODUCT_NOMECLATURE, en utilisant des commandes `CASE`pour pouvoir pivoter les résultats d'agrégations


    SELECT  TR.client_id,

    sum(CASE  WHEN  PRD_NOM.product_type="MEUBLE"  then (TR.prod_price* TR.prod_qty) END) as ventes_meuble,

    sum(CASE  WHEN  PRD_NOM.product_type="DECO"  then (TR.prod_price* TR.prod_qty) END)as ventes_deco

    FROM TRANSACTIONS TR

    LEFT JOIN PRODUCT_NOMENCLATURE PRD_NOM ON  TR.prop_id=PRD_NOM.product_id

    where  TR.date  BETWEEN  "2019-01-01"  and  "2019-12-31"

    group by client_id
