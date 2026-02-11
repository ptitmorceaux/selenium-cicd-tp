## 1. Avantages observés

### Quels sont les avantages de l'automatisation des tests que vous avez constatés ?

Le principal avantage est la "non-régression". Cela permet d'intégrer sereinement de nouvelles feature (comme l'ajout des nombres négatifs ou décimaux) sans risquer de casser l'ancien code existant. On évite ainsi de devoir re-tester manuellement toute l'application à chaque modification, ce qui représente un gain de temps considérable sur le long terme.

### Comment le CI/CD améliore-t-il la qualité du code ?

Lorsqu'il est bien configuré (avec analyse statique, tests unitaires), il empeche littéralement l'intégration de code défectueux. Il impose une rigueur de développement qui permet donc d'avoir une meilleur qualité.

---

## 2. Défis rencontrés

### Quelles difficultés avez-vous rencontrées avec Selenium ?

J'ai surtout fait face à un problème lié aux dépendances :
* **Drivers Windows** : Un conflit bloquant avec `webdriver-manager` sous Windows. J'ai du effectuer des manipulations manuelles : aller dans le dossier utilisateur pour supprimer le cache `.wdm/` et forcer l'installation de la version `4.0.2` de `webdriver-manager`. J'ai mis à jour le fichier `requirements.txt` en conséquence pour figer cette version fonctionnelle.

### Comment pourriez-vous améliorer la stabilité des tests ?

* Couvrir davantage de cas limites (*edge cases*) pour renforcer la robustesse, en acceptant que cela augmente légèrement la durée d'exécution.
* Effectuer les tests sur différents environnements (vm github par ex) pour être sur que l'application fonctionne dans diverses conditions. Pbl: le CI/CD va etre bcp plus lent... Donc peut etre pas une si bonne idée ? 

---

## 3. Métriques

### Quelles métriques sont les plus importantes pour votre projet ?

* Temps d'exécution : Pour éviter de ralentir le cycle de développement
* Taux d'erreur : Pour identifier rapidement les tests instables (flaky tests)
* Couverture : Pour s'assurer que les parties critiques de la logique métier sont bien testées

### Comment mesurer l'efficacité de votre pipeline CI/CD ?

La rapidité avec laquelle le pipeline informe le développeur si son code est valide ou s'il a introduit une "régression". Plus ce temps est court, plus la boucle de développement est efficace.