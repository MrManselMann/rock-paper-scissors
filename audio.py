import pygame

def play_mp3(file_path):
    # Initialize pygame mixer
    pygame.mixer.init()
    
    # Load the MP3 file
    pygame.mixer.music.load(file_path)
    
    # Play the MP3 file
    pygame.mixer.music.play()
    
    # Wait until the music is finished playing
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

# Example usage
play_mp3("test.mp3")
