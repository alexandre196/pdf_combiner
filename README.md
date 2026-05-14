# 📄 Combineur de PDF

Une application desktop simple et élégante pour fusionner plusieurs fichiers PDF en un seul, développée en Python.

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS-lightgrey)

---

## ✨ Fonctionnalités

- ➕ **Ajout multiple** de fichiers PDF en une seule sélection
- 🔀 **Réordonnancement** des fichiers avant la fusion (monter / descendre)
- 🗑 **Suppression** d'un fichier ou effacement complet de la liste
- ✅ **Fusion en un clic** avec choix du fichier de sortie
- 🎨 **Interface moderne** avec thème clair/sombre automatique (customtkinter)
- 🖼 **Icône personnalisée** intégrée dans l'exécutable

---

## 📦 Installation

### Prérequis

- Python 3.10+
- pip

### Installer les dépendances

```bash
pip install -r requirements.txt
```

### Lancer l'application

```bash
python pdf_combiner.py
```

---

## 🖥 Créer un exécutable (.exe)

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --icon=pdf_combiner.ico --add-data "pdf_combiner.ico;." pdf_combiner.py
```

L'exécutable sera généré dans le dossier `dist/`.

---

## 🛠 Technologies utilisées

| Librairie | Rôle |
|---|---|
| [customtkinter](https://github.com/TomSchimansky/CustomTkinter) | Interface graphique moderne |
| [pypdf](https://pypdf.readthedocs.io/) | Lecture et fusion des PDF |
| [PyInstaller](https://pyinstaller.org/) | Génération de l'exécutable |

---

## 📁 Structure du projet

```
pdf_combiner/
├── pdf_combiner.py     # Code principal
├── pdf_combiner.ico    # Icône de l'application
├── requirements.txt    # Dépendances
└── README.md
```

---

## 👤 Auteur

**Alexandre M.** — [@alexandre196](https://github.com/alexandre196)

---

## 📝 Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.
