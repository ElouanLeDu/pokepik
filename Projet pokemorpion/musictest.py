import pygame

# Initialisation de Pygame Mixer
pygame.mixer.init()

# Charger la musique
pygame.mixer.music.load("combat music.mp3")  # Remplace par le chemin de ton fichier

# Lancer la musique en boucle
pygame.mixer.music.play(-1)  # -1 pour jouer en boucle

# Exemple d'un combat Pokémon simple
print("Un combat Pokémon commence !")
input("Appuyez sur Entrée pour continuer...")
pygame.mixer.music.stop()  # Arrêter la musique à la fin
