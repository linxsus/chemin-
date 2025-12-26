# Guide d'Intégration : Système de Gestion d'États et Chemins

## Vue d'ensemble

Ce système permet de naviguer automatiquement entre les écrans de votre jeu en utilisant un graphe d'états et un algorithme de pathfinding.

---

## 📋 CHECKLIST D'INTÉGRATION

### Phase 1 : Installation et Configuration

- [ ] **1.1** Copier les dossiers dans votre projet :
  ```
  automatisation/
  ├── config/
  │   └── etat-chemin.toml
  ├── core/
  ├── etats/
  ├── chemins/
  └── utils/
  ```

- [ ] **1.2** Installer les dépendances :
  ```bash
  pip install tomli  # Pour Python < 3.11
  ```

- [ ] **1.3** Vérifier que l'import fonctionne :
  ```python
  from core import GestionnaireEtats
  ```

---

### Phase 2 : Implémenter les États (Détection d'Écran)

Pour chaque écran de votre jeu, vous devez implémenter la méthode `verif()`.

- [ ] **2.1** Modifier `etats/ville.py` :
  ```python
  from core.etat import Etat

  class EtatVille(Etat):
      nom = "ville"
      groupes = ["ecran_principal"]

      def verif(self) -> bool:
          # VOTRE LOGIQUE DE DÉTECTION ICI
          # Exemples :

          # Option A : Détection par image (avec votre système existant)
          return detecter_image("images/ville_titre.png")

          # Option B : Détection par OCR
          return "VILLE" in lire_texte_ecran()

          # Option C : Détection par pixel
          return pixel_couleur(100, 200) == (255, 128, 0)
  ```

- [ ] **2.2** Répéter pour chaque état :
  - [ ] `etats/carte.py`
  - [ ] `etats/formation_troupe.py`
  - [ ] `etats/construction_batiment.py`
  - [ ] `etats/popup_erreur.py`
  - [ ] `etats/popup_confirmation.py`
  - [ ] `etats/popup_info.py`
  - [ ] `etats/demarrage.py`

- [ ] **2.3** Ajouter vos propres états si nécessaire :
  ```python
  # etats/mon_nouvel_etat.py
  from core.etat import Etat

  class EtatMonNouvelEtat(Etat):
      nom = "mon_nouvel_etat"
      groupes = ["ecran_principal"]

      def verif(self) -> bool:
          # Votre logique
          return False
  ```

---

### Phase 3 : Implémenter les Actions

- [ ] **3.1** Modifier `chemins/actions.py` avec votre système de clic/attente :
  ```python
  class CliquerBouton(Action):
      def __init__(self, nom_bouton: str):
          self.nom_bouton = nom_bouton

      def executer(self) -> None:
          # VOTRE LOGIQUE DE CLIC ICI
          # Exemples :

          # Option A : Coordonnées fixes
          positions = {
              "bouton_carte": (500, 300),
              "bouton_ville": (100, 50),
              "bouton_fermer": (800, 100),
          }
          x, y = positions[self.nom_bouton]
          pyautogui.click(x, y)

          # Option B : Détection d'image
          pos = trouver_image(f"boutons/{self.nom_bouton}.png")
          if pos:
              pyautogui.click(pos)

  class Attendre(Action):
      def __init__(self, duree: float):
          self.duree = duree

      def executer(self) -> None:
          import time
          time.sleep(self.duree)
  ```

---

### Phase 4 : Configurer les Priorités

- [ ] **4.1** Modifier `config/etat-chemin.toml` :
  ```toml
  [priorites]
  # Ordre de test des états (les popups en premier !)
  ordre = [
      "popup_erreur",
      "popup_confirmation",
      "popup_info",
      "demarrage",
      "ville",
      "carte",
      "formation_troupe",
      "construction_batiment"
  ]
  ```

---

### Phase 5 : Intégrer dans votre Code Principal

- [ ] **5.1** Initialiser le gestionnaire :
  ```python
  from core import GestionnaireEtats, AucunEtatTrouve

  # Au démarrage de votre programme
  gestionnaire = GestionnaireEtats("config/etat-chemin.toml")
  ```

- [ ] **5.2** Fonction pour naviguer vers un état :
  ```python
  def naviguer_vers(destination: str) -> bool:
      """
      Navigue vers l'état destination.
      Retourne True si réussi, False sinon.
      """
      MAX_TENTATIVES = 5

      for tentative in range(MAX_TENTATIVES):
          # 1. Déterminer où on est
          try:
              etat_actuel = gestionnaire.determiner_etat_actuel()
          except AucunEtatTrouve:
              print("Impossible de déterminer l'état actuel")
              return False

          # 2. Vérifier si on est déjà arrivé
          if etat_actuel.nom == destination:
              print(f"Arrivé à {destination}")
              return True

          # 3. Trouver le chemin
          chemins, complet = gestionnaire.trouver_chemin(etat_actuel, destination)

          if not chemins:
              print(f"Aucun chemin de {etat_actuel.nom} vers {destination}")
              return False

          # 4. Exécuter le premier chemin
          chemin = chemins[0]
          print(f"Exécution: {chemin}")

          actions = chemin.generer_actions()
          for action in actions:
              action.executer()

          # 5. Si chemin incertain, on reboucle pour redéterminer l'état
          if not complet:
              print("Chemin incertain, redétermination...")
              continue

      return False
  ```

- [ ] **5.3** Utiliser dans votre programme :
  ```python
  # Exemple d'utilisation
  def collecter_ressources():
      # Aller à la carte
      if naviguer_vers("carte"):
          # Faire les actions sur la carte
          collecter_sur_carte()

          # Retourner à la ville
          naviguer_vers("ville")

  def former_troupes():
      if naviguer_vers("formation_troupe"):
          # Lancer la formation
          lancer_formation()
          naviguer_vers("ville")
  ```

---

## 📁 STRUCTURE FINALE

```
automatisation/
├── config/
│   └── etat-chemin.toml      # ✏️ Configurer les priorités
│
├── core/                      # ⚙️ Ne pas modifier
│   ├── __init__.py
│   ├── etat.py
│   ├── etat_inconnu.py
│   ├── chemin.py
│   ├── exceptions.py
│   └── gestionnaire_etats.py
│
├── etats/                     # ✏️ Implémenter verif() pour chaque état
│   ├── ville.py
│   ├── carte.py
│   └── ...
│
├── chemins/                   # ✏️ Implémenter les actions
│   ├── actions.py             # ⬅️ IMPORTANT : vos fonctions de clic
│   ├── ville_carte.py
│   └── ...
│
├── utils/
│   └── logger.py              # ⚙️ Ne pas modifier
│
└── votre_programme.py         # ✏️ Intégrer le gestionnaire
```

---

## 🔧 EXEMPLE COMPLET D'INTÉGRATION

```python
# votre_programme.py

import time
from core import GestionnaireEtats, AucunEtatTrouve, EtatInconnuException

class Automatisation:
    def __init__(self):
        self.gestionnaire = GestionnaireEtats("config/etat-chemin.toml")

    def naviguer_vers(self, destination: str, max_tentatives: int = 5) -> bool:
        """Navigue vers un état."""
        for _ in range(max_tentatives):
            try:
                etat_actuel = self.gestionnaire.determiner_etat_actuel()
            except AucunEtatTrouve:
                print("[ERREUR] État actuel inconnu")
                return False

            if etat_actuel.nom == destination:
                return True

            chemins, complet = self.gestionnaire.trouver_chemin(
                etat_actuel, destination
            )

            if not chemins:
                print(f"[ERREUR] Pas de chemin vers {destination}")
                return False

            # Exécuter le premier chemin
            for action in chemins[0].generer_actions():
                action.executer()

            if complet:
                # Vérifier qu'on est bien arrivé
                time.sleep(0.5)
                etat_final = self.gestionnaire.determiner_etat_actuel()
                return etat_final.nom == destination

        return False

    def ou_suis_je(self) -> str:
        """Retourne le nom de l'état actuel."""
        try:
            return self.gestionnaire.determiner_etat_actuel().nom
        except AucunEtatTrouve:
            return "inconnu"

    def run(self):
        """Boucle principale."""
        print(f"État actuel: {self.ou_suis_je()}")

        # Exemple de tâches
        if self.naviguer_vers("carte"):
            print("Sur la carte !")
            # ... faire des actions ...

        if self.naviguer_vers("ville"):
            print("Retour en ville !")


if __name__ == "__main__":
    bot = Automatisation()
    bot.run()
```

---

## ⚠️ POINTS IMPORTANTS

1. **Les méthodes `verif()` doivent être rapides** - évitez les opérations lentes
2. **L'ordre des priorités est crucial** - testez les popups en premier
3. **Gérez les cas d'erreur** - réseau, écran de chargement, etc.
4. **Testez chaque état individuellement** avant de tester les chemins

---

## 🐛 DÉBOGAGE

Activez les logs détaillés dans `config/etat-chemin.toml` :

```toml
[logging]
niveau = "DEBUG"
```

Cela affichera les détails du pathfinding et de la détection d'état.
