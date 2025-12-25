# Spécification Technique : Système de Gestion d'États et Chemins

**Version**: 1.0  
**Date**: 2024-12-25  
**Contexte**: Framework d'automatisation de jeu - Navigation entre écrans

---

## 1. Vue d'ensemble

### 1.1 Objectif
Système permettant de modéliser et naviguer dans un graphe d'états (écrans de jeu) via des chemins (transitions), avec recherche automatique de chemin (pathfinding) et gestion de l'incertitude.

### 1.2 Périmètre
Ce système couvre **uniquement** :
- Modélisation des états et chemins
- Recherche de chemin (pathfinding)
- Détermination de l'état actuel
- Génération de liste d'actions pour navigation

**Hors périmètre** (géré par d'autres composants) :
- Exécution des actions
- Vérification de l'état actuel avant exécution
- Gestion de la mémoire d'exécution

### 1.3 Composants principaux

```
┌─────────────────────────────────────────────────────────────┐
│                   GestionnaireEtats                         │
│  - Scan et enregistrement des états/chemins                │
│  - Pathfinding (algorithme plus court chemin)              │
│  - Détermination état actuel                               │
│  - Configuration (priorités)                               │
└─────────────────────────────────────────────────────────────┘
           │                            │
           ↓                            ↓
┌──────────────────────┐      ┌──────────────────────┐
│       Etat           │      │      Chemin          │
│  - Singleton         │      │  - État initial      │
│  - verif()           │◄─────│  - État sortie       │
│  - nom               │      │  - generer_actions() │
│  - groupes[]         │      └──────────────────────┘
└──────────────────────┘
           △
           │
┌──────────────────────┐
│    EtatInconnu       │
│  - etats_possibles[] │
└──────────────────────┘
```

---

## 2. Structures de données

### 2.1 Classe : Etat

**Description** : Représente un état/écran du système (ex: ville, carte, popup).

**Pattern** : Singleton (une seule instance par classe)

**Attributs** :
| Nom | Type | Description | Obligatoire | Défaut |
|-----|------|-------------|-------------|---------|
| `nom` | String | Identifiant unique de l'état | Oui | Nom de la classe |
| `groupes` | List[String] | Groupes d'appartenance (ex: "popup", "ecran_principal") | Non | [] |

**Méthodes** :

```
verif() -> Boolean
  Description: Vérifie si le système est actuellement dans cet état
  Paramètres: Aucun
  Retour: 
    - true si l'état actuel correspond
    - false sinon
  Exceptions: Aucune
  Notes: Implémentation spécifique dans chaque classe dérivée
```

**Contraintes** :
- Chaque classe dérivée ne peut avoir qu'UNE seule instance (Singleton)
- Le `nom` doit être unique dans tout le système
- Les `groupes` sont des strings (validation via enum généré par script)

**Exemples de classes dérivées** :
- `EtatVille` : nom="ville", groupes=["ecran_principal"]
- `EtatCarte` : nom="carte", groupes=["ecran_principal"]
- `EtatPopupErreur` : nom="popup_erreur", groupes=["popup"]

---

### 2.2 Classe : EtatInconnu (hérite de Etat)

**Description** : État spécial représentant un état incertain. Utilisé comme état de sortie de chemins dont le résultat est imprévisible.

**Attributs additionnels** :
| Nom | Type | Description | Obligatoire |
|-----|------|-------------|-------------|
| `etats_possibles` | List[Etat] | Liste des états à tester pour déterminer l'état réel | Oui |

**Comportement spécifique** :

```
verif() -> Boolean
  Retour: Toujours false
  Raison: Un état inconnu ne peut jamais être l'état actuel réel
```

**Exemples** :
- `EtatInconnuPopup` : etats_possibles=[EtatPopupErreur, EtatPopupConfirmation, EtatPopupInfo]
- `EtatInconnuGlobal` : etats_possibles=[] (vide = tous les états enregistrés)

---

### 2.3 Classe : Chemin

**Description** : Représente une transition possible entre deux états, avec les actions nécessaires pour effectuer la transition.

**Pattern** : Pas de Singleton (peut y avoir plusieurs chemins pour la même transition)

**Attributs** :
| Nom | Type | Description | Obligatoire | Valeurs possibles |
|-----|------|-------------|-------------|-------------------|
| `etat_initial` | Etat | État de départ | Oui | Instance d'Etat |
| `etat_sortie` | Etat, List[Etat], ou null | État(s) d'arrivée | Non | - null : inconnu complet<br>- Etat : sortie certaine<br>- List[Etat] : liste d'états possibles |
| `fonction_actions` | Function | Fonction générant les actions | Oui | Signature: `() -> List[Action]` |

**Méthodes** :

```
generer_actions() -> List[Action]
  Description: Appelle fonction_actions pour obtenir la liste d'actions
  Paramètres: Aucun
  Retour: Liste d'objets Action du framework
  Exceptions: Peut lever exceptions de fonction_actions
```

**Types d'état de sortie** :

1. **Sortie certaine** : `etat_sortie = EtatCarte`
   - Le chemin mène toujours vers cet état
   
2. **Sortie multiple** : `etat_sortie = [EtatVille, EtatCarte]`
   - Le chemin peut mener vers l'un de ces états
   - Il faut tester après exécution
   
3. **Sortie inconnue complète** : `etat_sortie = null`
   - Aucune idée de l'état d'arrivée
   - Il faut tester tous les états enregistrés
   
4. **Sortie via EtatInconnu** : `etat_sortie = EtatInconnuPopup`
   - Utilise la liste `etats_possibles` de l'EtatInconnu

**Exemples** :
```
CheminVilleCarte:
  etat_initial: EtatVille
  etat_sortie: EtatCarte
  fonction_actions: () -> [CliquerBouton("carte"), Attendre(1)]

CheminFermerPopup:
  etat_initial: EtatPopupErreur
  etat_sortie: EtatInconnuPopup  # Retour incertain
  fonction_actions: () -> [CliquerBouton("fermer")]

CheminDemarrage:
  etat_initial: EtatDemarrage
  etat_sortie: null  # Complètement inconnu
  fonction_actions: () -> [LancerApplication()]
```

---

### 2.4 Classe : GestionnaireEtats

**Description** : Composant central gérant le graphe d'états, le pathfinding et la détermination d'état.

**Attributs privés** :
| Nom | Type | Description |
|-----|------|-------------|
| `_etats` | Map[String, Etat] | Dictionnaire nom → instance Etat |
| `_chemins` | List[Chemin] | Liste de tous les chemins enregistrés |
| `_priorites` | List[String] | Ordre de priorité des noms d'états pour les tests |
| `_logger` | Logger | Logger du module |

**Méthodes publiques** :

#### 2.4.1 Initialisation

```
constructeur(chemin_config: String)
  Description: Initialise le gestionnaire, scan les états/chemins, charge config
  Paramètres:
    - chemin_config: Chemin vers fichier TOML de configuration
  Comportement:
    1. Initialiser le logger (get_module_logger('GestionnaireEtats'))
    2. Scanner le répertoire 'etats/' et instancier toutes les classes Etat
    3. Scanner le répertoire 'chemins/' et instancier toutes les classes Chemin
    4. Charger la configuration TOML
    5. Résoudre toutes les références (string/classe → instance)
    6. Valider la cohérence (noms uniques, références valides)
  Exceptions:
    - ErreurConfiguration: Si le fichier TOML est invalide
    - ErreurValidation: Si noms dupliqués ou références invalides
  Post-conditions:
    - Tous les états sont enregistrés dans _etats
    - Tous les chemins sont enregistrés dans _chemins
    - Toutes les références sont résolues
```

#### 2.4.2 Recherche de chemin

```
trouver_chemin(etat_depart: Etat|String, etat_arrivee: Etat|String) 
  -> (List[Chemin], Boolean)
  
  Description: Trouve le plus court chemin entre deux états
  
  Paramètres:
    - etat_depart: État de départ (instance ou nom)
    - etat_arrivee: État d'arrivée (instance ou nom)
    
  Retour: Tuple (liste_chemins, chemin_complet)
    - liste_chemins: Séquence ordonnée de Chemin à exécuter
    - chemin_complet: 
      * true = chemin complet jusqu'à destination
      * false = chemin partiel (contient incertitude, s'arrête avant)
      
  Algorithme:
    1. Résoudre etat_depart et etat_arrivee en instances si strings
    2. TENTATIVE 1 - Chemins certains uniquement:
       a. Construire graphe avec uniquement chemins à sortie certaine
       b. Appliquer algorithme plus court chemin (BFS/Dijkstra)
       c. Si chemin trouvé → retourner (chemin, true)
    3. TENTATIVE 2 - Avec chemins incertains:
       a. Construire graphe complet (tous les chemins)
       b. Appliquer algorithme plus court chemin
       c. Si chemin trouvé:
          - Parcourir le chemin trouvé
          - S'arrêter au premier chemin incertain
          - Retourner (chemin_partiel, false)
    4. Si aucun chemin → retourner ([], false)
    
  Exceptions:
    - EtatInconnu: Si etat_depart ou etat_arrivee n'existe pas
    
  Exemples:
    # Cas 1: Chemin direct certain
    trouver_chemin("ville", "carte") 
    → ([CheminVilleCarte], true)
    
    # Cas 2: Chemin multiple certain
    trouver_chemin("ville", "formation_troupe")
    → ([CheminVilleCarte, CheminCarteFormation], true)
    
    # Cas 3: Chemin avec incertitude
    trouver_chemin("popup_erreur", "ville")
    → ([CheminFermerPopup], false)  # S'arrête à l'incertitude
    
    # Cas 4: Pas de chemin
    trouver_chemin("ville", "etat_inexistant")
    → ([], false)
```

**Notes sur l'algorithme** :
- Un chemin est "certain" si `etat_sortie` est une instance unique d'Etat
- Un chemin est "incertain" si `etat_sortie` est null, une liste, ou un EtatInconnu
- Pour le graphe, les chemins incertains créent des arcs vers tous leurs états possibles

#### 2.4.3 Détermination d'état actuel

```
determiner_etat_actuel(liste_etats: List[Etat|String] = null) -> Etat
  
  Description: Teste les états pour déterminer l'état actuel du système
  
  Paramètres:
    - liste_etats: Liste d'états à tester (null = tous les états)
    
  Retour: Instance Etat correspondant à l'état actuel
  
  Algorithme:
    1. Si liste_etats est null:
       - Utiliser tous les états de _etats
    2. Sinon:
       - Résoudre les strings en instances
    3. Trier les états selon l'ordre de _priorites:
       a. États dans _priorites viennent en premier (dans l'ordre défini)
       b. États hors _priorites viennent après (ordre quelconque)
    4. Pour chaque état dans l'ordre:
       a. Appeler etat.verif()
       b. Si retourne true → retourner cet état
    5. Si aucun état ne correspond:
       - Chercher un EtatInconnuGlobal (celui avec etats_possibles vide)
       - Si trouvé → retourner cet état
       - Sinon → lever exception AucunEtatTrouve
       
  Exceptions:
    - AucunEtatTrouve: Si aucun état ne correspond et pas d'EtatInconnuGlobal
    - EtatInvalide: Si un nom d'état dans liste_etats n'existe pas
    
  Exemples:
    # Cas 1: État trouvé directement
    determiner_etat_actuel() 
    → EtatVille (car verif() retourne true)
    
    # Cas 2: Avec liste restreinte
    determiner_etat_actuel([EtatVille, EtatCarte])
    → teste uniquement ces 2 états
    
    # Cas 3: Aucun état trouvé
    determiner_etat_actuel()
    → EtatInconnuGlobal (fallback)
```

**Notes** :
- Les états EtatInconnu ne sont jamais testés directement (leur verif() retourne toujours false)
- L'ordre de priorité est crucial pour optimiser les tests

#### 2.4.4 Méthodes utilitaires

```
obtenir_etat(nom: String) -> Etat
  Description: Récupère une instance d'état par son nom
  Retour: Instance Etat
  Exception: EtatInconnu si nom invalide

obtenir_chemins_depuis(etat: Etat|String) -> List[Chemin]
  Description: Liste tous les chemins partant d'un état
  Retour: Liste de Chemin ayant etat comme etat_initial

obtenir_chemins_vers(etat: Etat|String) -> List[Chemin]
  Description: Liste tous les chemins arrivant à un état
  Retour: Liste de Chemin ayant etat comme etat_sortie possible
  Note: Inclut chemins incertains si etat fait partie des possibilités
```

---

## 3. Format de configuration (TOML)

**Fichier** : `config/etat-chemin.toml`

```toml
# Configuration du système de gestion d'états et chemins

# ===== PRIORITÉS DE TEST DES ÉTATS =====
[priorites]
# Ordre de test pour determiner_etat_actuel()
# Les états listés ici sont testés en premier dans l'ordre
# Les états non listés sont testés après (ordre non garanti)
ordre = [
    "demarage",
    "ville",
    "carte",
    "formation_troupe",
    "construction_batiment",
    "popup_erreur",
    "popup_confirmation",
    "popup_info"
]

# ===== CONFIGURATION PATHFINDING (optionnel) =====
[pathfinding]
# Profondeur maximale de recherche (évite boucles infinies)
max_profondeur = 20

# Timeout en secondes pour la recherche
timeout_secondes = 5

# ===== LOGGING (optionnel) =====
[logging]
# Niveau de détail des logs spécifique au gestionnaire
# Valeurs: DEBUG, INFO, WARNING, ERROR
niveau = "INFO"

# Logguer les chemins trouvés
log_chemins_trouves = true
```

**Validation** :
- `priorites.ordre` doit contenir des noms d'états valides
- Les états non listés dans `ordre` sont testés après
- La configuration est chargée au démarrage, erreur si fichier manquant

---

## 4. Organisation des fichiers

```
projet/
├── config/
│   └── etat-chemin.toml          # Configuration
│
├── etats/                         # Module des états
│   ├── __init__.py
│   ├── ville.py                   # class EtatVille(Etat)
│   ├── carte.py                   # class EtatCarte(Etat)
│   ├── popup_erreur.py            # class EtatPopupErreur(Etat)
│   ├── inconnu_popup.py           # class EtatInconnuPopup(EtatInconnu)
│   ├── inconnu_global.py          # class EtatInconnuGlobal(EtatInconnu)
│   └── ...
│
├── chemins/                       # Module des chemins
│   ├── __init__.py
│   ├── ville_carte.py             # class CheminVilleCarte(Chemin)
│   ├── carte_formation.py         # class CheminCarteFormation(Chemin)
│   ├── fermer_popup.py            # class CheminFermerPopup(Chemin)
│   └── ...
│
├── core/
│   ├── etat.py                    # Classe de base Etat + Singleton
│   ├── etat_inconnu.py            # Classe EtatInconnu
│   ├── chemin.py                  # Classe Chemin
│   └── gestionnaire_etats.py     # Classe GestionnaireEtats
│
└── utils/
    └── logger.py                  # Système de logging existant
```

**Conventions de nommage** :
- Fichiers : `snake_case.py`
- Classes : `PascalCase`
- Exemples :
  - `etats/ville.py` → `class EtatVille`
  - `chemins/ville_carte.py` → `class CheminVilleCarte`

---

## 5. Algorithmes détaillés

### 5.1 Scan des modules

```
FONCTION scanner_modules(repertoire: String, classe_base: Class) -> List[Instance]
  ENTRÉES:
    - repertoire: Chemin du répertoire à scanner ("etats/" ou "chemins/")
    - classe_base: Classe dont doivent hériter les classes trouvées (Etat ou Chemin)
  
  SORTIE:
    - Liste d'instances des classes trouvées
  
  ALGORITHME:
    instances ← liste vide
    
    POUR chaque fichier .py dans repertoire:
      SI fichier commence par "__":
        CONTINUER  # Ignorer __init__.py, __pycache__, etc.
      
      module_name ← extraire nom sans extension
      module ← importer dynamiquement le module
      
      POUR chaque attribut dans module:
        SI attribut est une classe ET hérite de classe_base:
          instance ← instancier la classe (Singleton pour Etat)
          AJOUTER instance à instances
    
    RETOURNER instances
  
  EXCEPTIONS:
    - Erreur d'import → Logger warning et continuer
    - Erreur d'instanciation → Logger warning et continuer
```

### 5.2 Résolution des références

```
FONCTION resoudre_references(chemins: List[Chemin], etats: Map[String, Etat])
  ENTRÉES:
    - chemins: Liste des chemins à traiter
    - etats: Map des états enregistrés
  
  ALGORITHME:
    POUR chaque chemin dans chemins:
      # Résoudre etat_initial
      SI chemin.etat_initial est String:
        SI chemin.etat_initial existe dans etats:
          chemin.etat_initial ← etats[chemin.etat_initial]
        SINON:
          LEVER ErreurValidation("État initial inexistant: " + chemin.etat_initial)
      
      SI chemin.etat_initial est Class:
        instance ← chercher instance de cette classe dans etats.values()
        SI trouvée:
          chemin.etat_initial ← instance
        SINON:
          LEVER ErreurValidation("Classe d'état initial non enregistrée")
      
      # Résoudre etat_sortie
      SI chemin.etat_sortie est null:
        # OK, sortie inconnue complète
        CONTINUER
      
      SI chemin.etat_sortie est String:
        # Idem que etat_initial
        résoudre en instance
      
      SI chemin.etat_sortie est Class:
        # Idem que etat_initial
        résoudre en instance
      
      SI chemin.etat_sortie est List:
        POUR chaque element dans chemin.etat_sortie:
          résoudre element (String ou Class → Instance)
  
  POST-CONDITIONS:
    - Tous les etat_initial sont des instances
    - Tous les etat_sortie sont null, instance, ou List[instance]
```

### 5.3 Pathfinding (BFS modifié)

```
FONCTION bfs_plus_court_chemin(
  graphe: Map[Etat, List[Chemin]], 
  depart: Etat, 
  arrivee: Etat
) -> List[Chemin] ou null

  ENTRÉES:
    - graphe: Pour chaque état, liste des chemins sortants
    - depart: État de départ
    - arrivee: État d'arrivée
  
  SORTIE:
    - Liste ordonnée de Chemin formant le plus court chemin
    - null si aucun chemin
  
  ALGORITHME:
    file ← file vide
    file.ajouter((depart, []))  # (état_actuel, chemin_parcouru)
    visites ← ensemble vide
    
    TANT QUE file non vide:
      (etat_actuel, chemin_parcouru) ← file.defiler()
      
      SI etat_actuel dans visites:
        CONTINUER
      
      visites.ajouter(etat_actuel)
      
      SI etat_actuel == arrivee:
        RETOURNER chemin_parcouru
      
      chemins_sortants ← graphe[etat_actuel]
      
      POUR chaque chemin dans chemins_sortants:
        etats_suivants ← obtenir_etats_sortie(chemin)
        
        POUR chaque etat_suivant dans etats_suivants:
          SI etat_suivant non dans visites:
            nouveau_chemin ← chemin_parcouru + [chemin]
            file.ajouter((etat_suivant, nouveau_chemin))
    
    RETOURNER null  # Aucun chemin trouvé
```

**Fonction auxiliaire** :
```
FONCTION obtenir_etats_sortie(chemin: Chemin) -> List[Etat]
  SI chemin.etat_sortie est null:
    RETOURNER tous les états enregistrés
  
  SI chemin.etat_sortie est Etat:
    RETOURNER [chemin.etat_sortie]
  
  SI chemin.etat_sortie est List[Etat]:
    RETOURNER chemin.etat_sortie
  
  SI chemin.etat_sortie est EtatInconnu:
    SI etat_sortie.etats_possibles est vide:
      RETOURNER tous les états enregistrés
    SINON:
      RETOURNER etat_sortie.etats_possibles
```

### 5.4 Construction graphe pour pathfinding

```
FONCTION construire_graphe(chemins: List[Chemin], seulement_certains: Boolean) 
  -> Map[Etat, List[Chemin]]

  ENTRÉES:
    - chemins: Tous les chemins disponibles
    - seulement_certains: true = ignorer chemins incertains
  
  SORTIE:
    - Map associant chaque état aux chemins partant de cet état
  
  ALGORITHME:
    graphe ← map vide
    
    POUR chaque chemin dans chemins:
      SI seulement_certains ET chemin est incertain:
        CONTINUER  # Ignorer ce chemin
      
      etat_depart ← chemin.etat_initial
      
      SI etat_depart non dans graphe:
        graphe[etat_depart] ← liste vide
      
      graphe[etat_depart].ajouter(chemin)
    
    RETOURNER graphe

FONCTION chemin_est_incertain(chemin: Chemin) -> Boolean
  RETOURNER (
    chemin.etat_sortie est null OU
    chemin.etat_sortie est List OU
    chemin.etat_sortie est instance de EtatInconnu
  )
```

---

## 6. Gestion des erreurs

### 6.1 Exceptions

| Exception | Quand | Action |
|-----------|-------|--------|
| `ErreurConfiguration` | Fichier TOML invalide ou manquant | Arrêt du programme |
| `ErreurValidation` | Références invalides, noms dupliqués | Arrêt au démarrage |
| `EtatInconnu` | Nom d'état inexistant dans une requête | Lever exception |
| `AucunEtatTrouve` | `determiner_etat_actuel()` ne trouve rien | Lever exception |
| `AucunCheminTrouve` | Pathfinding échoue (retour normal) | Retourner ([], false) |

### 6.2 Logging

**Niveaux de log** :

| Niveau | Usage |
|--------|-------|
| DEBUG | Détails algorithme pathfinding, états testés |
| INFO | Scan modules, chemins trouvés, état actuel déterminé |
| WARNING | Imports échoués, références non résolues (continuable) |
| ERROR | Erreurs critiques (validation, configuration) |

**Exemples** :
```
[INFO] GestionnaireEtats - Scan du répertoire 'etats/': 15 états trouvés
[INFO] GestionnaireEtats - Scan du répertoire 'chemins/': 42 chemins trouvés
[DEBUG] GestionnaireEtats - Pathfinding: ville → formation_troupe
[DEBUG] GestionnaireEtats - Chemin trouvé: ville → carte → formation_troupe (2 étapes)
[INFO] GestionnaireEtats - État actuel déterminé: EtatVille
[WARNING] GestionnaireEtats - Import échoué: etats/test_debug.py (ignoré)
[ERROR] GestionnaireEtats - Validation: État 'carte_invalide' référencé mais inexistant
```

---

## 7. Cas d'usage détaillés

### 7.1 Cas 1 : Navigation simple avec chemin certain

**Objectif** : Aller de "ville" à "carte"

**Déroulement** :
```
1. Manoire appelle:
   chemins, complet = gestionnaire.trouver_chemin("ville", "carte")

2. Gestionnaire:
   - Résout "ville" → EtatVille
   - Résout "carte" → EtatCarte
   - Tentative 1 (chemins certains):
     * Trouve CheminVilleCarte (etat_sortie = EtatCarte)
     * Chemin = [CheminVilleCarte]
   - Retourne ([CheminVilleCarte], true)

3. Manoire:
   - Voit que complet = true
   - Génère la SequenceAction:
     actions = CheminVilleCarte.generer_actions()
   - Exécute la séquence
   - Arrive à l'état "carte"
```

**Résultat** : Navigation directe, aucune incertitude

---

### 7.2 Cas 2 : Navigation multi-étapes

**Objectif** : Aller de "ville" à "formation_troupe"

**Graphe** :
```
ville → carte → formation_troupe
```

**Déroulement** :
```
1. gestionnaire.trouver_chemin("ville", "formation_troupe")

2. Pathfinding:
   - Tentative 1 (chemins certains):
     * Trouve: ville → carte (via CheminVilleCarte)
     * Puis: carte → formation_troupe (via CheminCarteFormation)
   - Retourne ([CheminVilleCarte, CheminCarteFormation], true)

3. Manoire:
   - Génère actions:
     actions = []
     actions += CheminVilleCarte.generer_actions()
     actions += CheminCarteFormation.generer_actions()
   - Exécute toute la séquence
```

**Résultat** : Navigation en 2 étapes, certaine

---

### 7.3 Cas 3 : Navigation avec incertitude

**Objectif** : Fermer un popup et retourner à l'écran principal

**Graphe** :
```
popup_erreur → ??? (peut être ville, carte, ou formation_troupe)
```

**Définition du chemin** :
```python
class CheminFermerPopup(Chemin):
    etat_initial = EtatPopupErreur
    etat_sortie = EtatInconnuEcranPrincipal  # États possibles: ville, carte, formation
    fonction_actions = lambda: [CliquerBouton("fermer")]
```

**Déroulement** :
```
1. gestionnaire.trouver_chemin("popup_erreur", "ville")

2. Pathfinding:
   - Tentative 1 (chemins certains):
     * CheminFermerPopup est incertain → ignoré
     * Aucun chemin certain trouvé
   
   - Tentative 2 (avec incertains):
     * Trouve CheminFermerPopup
     * Ce chemin est incertain → arrêt là
   
   - Retourne ([CheminFermerPopup], false)

3. Manoire:
   - Voit que complet = false
   - Génère et exécute les actions de CheminFermerPopup
   
4. Après exécution:
   - Manoire appelle:
     etat_actuel = gestionnaire.determiner_etat_actuel(
       [EtatVille, EtatCarte, EtatFormationTroupe]
     )
   
5. Selon résultat:
   a. Si etat_actuel = EtatVille:
      → Objectif atteint, fin
   
   b. Si etat_actuel = EtatCarte:
      → Relancer: gestionnaire.trouver_chemin("carte", "ville")
   
   c. Si etat_actuel = EtatFormationTroupe:
      → Relancer: gestionnaire.trouver_chemin("formation_troupe", "ville")
```

**Résultat** : Navigation en 2 phases (exécution + redétermination)

---

### 7.4 Cas 4 : Démarrage de l'application

**Situation** : Application vient de démarrer, état complètement inconnu

**Déroulement** :
```
1. Manoire appelle:
   etat_actuel = gestionnaire.determiner_etat_actuel()

2. Gestionnaire:
   - Liste des états = tous les états enregistrés
   - Ordre de test selon priorités:
     1. EtatDemarage → verif() retourne false
     2. EtatVille → verif() retourne true ✓
   
   - Retourne EtatVille

3. Manoire:
   - Sait qu'on est dans "ville"
   - Peut maintenant naviguer normalement
```

**Cas alternatif** : Aucun état ne correspond
```
2. Gestionnaire:
   - Tous les verif() retournent false
   - Cherche EtatInconnuGlobal
   - Le trouve et le retourne

3. Manoire:
   - État actuel = "inconnu global"
   - Décide d'appeler CheminDemarrage pour réinitialiser
```

---

## 8. Patterns d'implémentation

### 8.1 Singleton Metaclass

**Objectif** : Garantir une seule instance par classe Etat

**Pseudo-code** :
```
CLASS SingletonMeta (hérite de Metaclass):
  _instances = dictionnaire vide
  
  MÉTHODE __call__(class, *args, **kwargs):
    SI class non dans _instances:
      instance = SUPER().__call__(*args, **kwargs)
      _instances[class] = instance
    RETOURNER _instances[class]

CLASS Etat (metaclass=SingletonMeta):
  # La métaclasse garantit le singleton
  ...
```

### 8.2 Résolution flexible des références

**Support de 3 formats** :
```
# Format 1: String
chemin.etat_initial = "ville"

# Format 2: Class
chemin.etat_initial = EtatVille

# Format 3: Instance
chemin.etat_initial = etat_ville_instance

# Le gestionnaire normalise tout en instances
```

**Fonction de résolution** :
```
FONCTION resoudre_reference(ref, map_etats) -> Etat:
  SI ref est String:
    RETOURNER map_etats[ref]
  
  SI ref est Class:
    POUR chaque etat dans map_etats.values():
      SI isinstance(etat, ref):
        RETOURNER etat
    LEVER EtatInconnu
  
  SI ref est instance de Etat:
    RETOURNER ref
  
  LEVER TypeError("Type de référence invalide")
```

---

## 9. Tests et validation

### 9.1 Tests unitaires requis

| Test | Description |
|------|-------------|
| `test_singleton` | Vérifier qu'une classe Etat ne peut avoir qu'une instance |
| `test_scan_etats` | Vérifier que tous les fichiers .py dans etats/ sont scannés |
| `test_resolution_references` | Tester résolution string/class/instance |
| `test_pathfinding_simple` | Chemin direct A→B |
| `test_pathfinding_multiple` | Chemin A→B→C |
| `test_pathfinding_aucun` | Aucun chemin entre A et B |
| `test_pathfinding_incertain` | Chemin avec incertitude |
| `test_determiner_etat` | Test de détermination d'état |
| `test_priorites` | Vérifier ordre de test des états |
| `test_etat_inconnu_fallback` | Test du fallback EtatInconnuGlobal |
| `test_validation_noms_uniques` | Lever exception si noms dupliqués |
| `test_validation_references` | Lever exception si référence invalide |

### 9.2 Tests d'intégration requis

| Test | Description |
|------|-------------|
| `test_navigation_complete` | Scénario complet: scan → pathfinding → exécution simulée |
| `test_navigation_incertaine` | Scénario avec incertitude et redétermination |
| `test_config_toml` | Chargement et application de configuration |
| `test_cas_complexe` | Graphe complexe avec 10+ états et 20+ chemins |

---

## 10. Métriques de performance

### 10.1 Objectifs de performance

| Métrique | Objectif |
|----------|----------|
| Temps de scan | < 1 seconde pour 50 états + 100 chemins |
| Temps pathfinding simple | < 50ms pour chemin direct |
| Temps pathfinding complexe | < 500ms pour graphe de 50 états |
| Temps determination état | < 200ms pour 20 états à tester |
| Mémoire | < 50 MB pour système complet |

### 10.2 Cas limites

| Cas | Comportement attendu |
|-----|---------------------|
| Graphe cyclique | BFS gère naturellement (ensemble visités) |
| 100+ états | Performance dégradée acceptable (< 2s) |
| Chemin très long (10+ étapes) | Limiter avec max_profondeur config |
| Tous les verif() sont lents | Optimiser ordre de priorité |

---

## 11. Évolutions futures possibles

### 11.1 Optimisations envisageables

1. **Cache de pathfinding**
   - Mémoriser chemins déjà calculés
   - Invalidation si graphe change

2. **Poids sur les chemins**
   - Certains chemins plus "coûteux" (lents, risqués)
   - Algorithme Dijkstra au lieu de BFS

3. **Apprentissage**
   - Statistiques sur succès/échec des chemins
   - Ajustement automatique des priorités

4. **Parallélisation**
   - Tester plusieurs états en parallèle
   - Pathfinding sur plusieurs CPU

### 11.2 Fonctionnalités additionnelles

1. **Pré-conditions sur chemins**
   - Chemin disponible seulement si condition vraie
   - Ex: "ville → carte" seulement si niveau > 5

2. **Post-actions**
   - Actions après changement d'état réussi
   - Ex: sauvegarder état après navigation

3. **Groupes de chemins**
   - Activer/désactiver groupe de chemins
   - Ex: désactiver chemins "premium" si pas abonné

---

## 12. Glossaire

| Terme | Définition |
|-------|------------|
| **État** | Écran ou situation identifiable du jeu (ville, carte, popup) |
| **Chemin** | Transition entre deux états avec actions nécessaires |
| **Pathfinding** | Recherche automatique de chemin entre deux états |
| **État certain** | État de sortie connu à 100% |
| **État incertain** | État de sortie inconnu ou multiple |
| **Chemin complet** | Chemin sans incertitude jusqu'à destination |
| **Chemin partiel** | Chemin s'arrêtant à une incertitude |
| **Singleton** | Pattern garantissant une seule instance d'une classe |
| **BFS** | Breadth-First Search, algorithme de parcours de graphe |
| **Résolution de référence** | Conversion string/classe → instance |

---

## Annexe A : Exemples de code (Python illustratif)

**Note** : Ces exemples sont donnés à titre illustratif en Python, mais la spec est agnostique du langage.

### Exemple d'État

```python
# etats/ville.py
from core.etat import Etat

class EtatVille(Etat):
    nom = "ville"
    groupes = ["ecran_principal"]
    
    def verif(self):
        # Logique de détection (OCR, image matching, etc.)
        return detecter_bouton_carte() and detecter_titre_ville()
```

### Exemple d'EtatInconnu

```python
# etats/inconnu_popup.py
from core.etat_inconnu import EtatInconnu
from etats.popup_erreur import EtatPopupErreur
from etats.popup_confirmation import EtatPopupConfirmation

class EtatInconnuPopup(EtatInconnu):
    nom = "inconnu_popup"
    groupes = ["popup"]
    etats_possibles = [
        EtatPopupErreur,  # Sera résolu en instance
        EtatPopupConfirmation
    ]
```

### Exemple de Chemin

```python
# chemins/ville_carte.py
from core.chemin import Chemin
from etats.ville import EtatVille
from etats.carte import EtatCarte
from actions import CliquerBouton, Attendre

class CheminVilleCarte(Chemin):
    etat_initial = EtatVille
    etat_sortie = EtatCarte
    
    def fonction_actions():
        return [
            CliquerBouton("bouton_carte"),
            Attendre(1.0)
        ]
```

### Exemple d'utilisation du Gestionnaire

```python
from core.gestionnaire_etats import GestionnaireEtats

# Initialisation
gestionnaire = GestionnaireEtats("config/etat-chemin.toml")

# Déterminer état actuel
etat_actuel = gestionnaire.determiner_etat_actuel()
print(f"État actuel: {etat_actuel.nom}")

# Trouver chemin
chemins, complet = gestionnaire.trouver_chemin(etat_actuel, "formation_troupe")

if complet:
    print(f"Chemin complet trouvé: {len(chemins)} étapes")
    for chemin in chemins:
        actions = chemin.generer_actions()
        # Exécuter actions...
else:
    print("Chemin partiel (incertitude)")
    # Exécuter puis redéterminer état...
```

---

**FIN DE LA SPÉCIFICATION**

Version 1.0 - Document complet et utilisable pour implémentation dans n'importe quel langage.
