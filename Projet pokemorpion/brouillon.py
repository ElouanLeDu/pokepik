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
fenetre.geometry("400x300")  # Dimensionner la fenêtre

# Ajouter des widgets pour le joueur 1
label_joueur1 = tk.Label(fenetre, text="Nom du Joueur 1 :")
label_joueur1.place(x=50, y=50)  # Position du label
entree_joueur1 = tk.Entry(fenetre, width=30)
entree_joueur1.place(x=200, y=50)  # Position de l'entrée

# Ajouter des widgets pour le joueur 2
label_joueur2 = tk.Label(fenetre, text="Nom du Joueur 2 :")
label_joueur2.place(x=50, y=100)  # Position du label
entree_joueur2 = tk.Entry(fenetre, width=30)
entree_joueur2.place(x=200, y=100)  # Position de l'entrée

# Bouton de recherche
bouton_rechercher = tk.Button(fenetre, text="Rechercher", command=rechercher)
bouton_rechercher.place(x=150, y=200)  # Position du bouton

# Lancer la boucle principale
fenetre.mainloop()
"""""
    def valider_joueurs(self):

        # Récupérer les noms des Pokémon saisis
        self.poke1 = self.entree_joueur1.get()
        self.poke2 = self.entree_joueur2.get()

        # Vérifier si les champs sont remplis
        if not self.poke1 or not self.poke2:
            messagebox.showerror("Erreur", "Veuillez entrer les noms des deux Pokémon.")
            return

        # Vérifier si les Pokémon sont valides
        if not self.fight.combat(self.poke1, self.poke2):
            messagebox.showerror("Erreur",f"Les Pokémon '{self.poke1}' ou '{self.poke2}' ne sont pas valides. Réessayez.")
            return

        # Si tout est valide, arrêter la musique et passer au combat
        pygame.mixer.music.stop()
        self.g.supprimerTout()

        self.g.afficherImage(-50, 0, "poke_stadium.png")

        self.g.quit()  # Fermer la boucle Tkinter pour continuer le programme
"""


def affichage_mot(self, mot):
    """
    Affiche le mot sur plusieurs lignes s'il contient des espaces.
    Sinon, affiche le mot en entier sur une seule ligne.
    """
    if ' ' in mot:
        # Découper le mot par espaces et afficher chaque partie sur une nouvelle ligne
        for partie in mot.split(' '):
            print(partie)
    else:
        # Afficher le mot entier
        print(mot)