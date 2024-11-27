import tkinter as tk
from tkinter import messagebox

def rechercher():
    # Récupérer les entrées des deux barres de recherche
    joueur1 = entree_joueur1.get()
    joueur2 = entree_joueur2.get()

    # Afficher les résultats ou effectuer une action
    if joueur1 and joueur2:
        messagebox.showinfo("Recherche", f"Joueur 1 : {joueur1}\nJoueur 2 : {joueur2}")
    else:
        messagebox.showwarning("Attention", "Veuillez entrer les noms des deux joueurs.")

# Créer la fenêtre principale
fenetre = tk.Tk()
fenetre.title("Recherche pour 2 joueurs")

# Ajouter des widgets pour le joueur 1
label_joueur1 = tk.Label(fenetre, text="Nom du Joueur 1 :")
label_joueur1.pack(pady=5)
entree_joueur1 = tk.Entry(fenetre, width=30)
entree_joueur1.pack(pady=5)

# Ajouter des widgets pour le joueur 2
label_joueur2 = tk.Label(fenetre, text="Nom du Joueur 2 :")
label_joueur2.pack(pady=5)
entree_joueur2 = tk.Entry(fenetre, width=30)
entree_joueur2.pack(pady=5)

# Bouton de recherche
bouton_rechercher = tk.Button(fenetre, text="Rechercher", command=rechercher)
bouton_rechercher.pack(pady=10)

# Lancer la boucle principale
fenetre.mainloop()
