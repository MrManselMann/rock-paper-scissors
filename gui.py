import tkinter as tk
from PIL import Image, ImageTk
from game import play_rock_paper_scissors
import random
#this was all chat gpt'd it was to hard to do on my own
class RockPaperScissorsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Rock-Paper-Scissors")
        
        # Load images
        self.image_paths = [
            r"C:\Users\jijoe.joseph\Desktop\New folder\pictures\rock.png",
            r"C:\Users\jijoe.joseph\Desktop\New folder\pictures\paper.png",
            r"C:\Users\jijoe.joseph\Desktop\New folder\pictures\scissor.png",  # Updated to 'scissor.png'
            r"C:\Users\jijoe.joseph\Desktop\New folder\pictures\eyesleft.png",
            r"C:\Users\jijoe.joseph\Desktop\New folder\pictures\eyesright.png",  # Added new eyes image
            r"C:\Users\jijoe.joseph\Desktop\New folder\pictures\winmouth.png",
            r"C:\Users\jijoe.joseph\Desktop\New folder\pictures\losemouth.png",
            r"C:\Users\jijoe.joseph\Desktop\New folder\pictures\normalmouth.png"
        ]
        
        # Load images and handle potential errors
        self.images = []
        for path in self.image_paths:
            try:
                image = ImageTk.PhotoImage(Image.open(path))
                self.images.append(image)
            except Exception as e:
                print(f"Error loading image at {path}: {e}")
        
        # Create and pack widgets
        self.create_widgets()
        self.update_header_image()  # Set initial header image

    def create_widgets(self):
        # Grid configuration
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_rowconfigure(2, weight=1)
        self.root.grid_rowconfigure(3, weight=1)  # Added row for "Play Again" button
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_columnconfigure(2, weight=1)

        # Header image
        if len(self.images) > 3:
            self.header_label = tk.Label(self.root, image=self.images[3])
        else:
            self.header_label = tk.Label(self.root, text="Header Image Not Loaded")
        self.header_label.grid(row=0, column=0, columnspan=3, pady=10)

        # Mouth image
        if len(self.images) > 7:
            self.mouth_label = tk.Label(self.root, image=self.images[7])
        else:
            self.mouth_label = tk.Label(self.root, text="Mouth Image Not Loaded")
        self.mouth_label.grid(row=2, column=1, pady=10)  # Changed to row=2

        # Start button
        self.start_button = tk.Button(self.root, text="Start Game", command=self.start_game)
        self.start_button.grid(row=3, column=1, pady=20)

        # Labels for displaying choices
        self.user_choice_label = tk.Label(self.root)
        self.user_choice_label.grid(row=1, column=0, padx=20)

        self.result_label = tk.Label(self.root, text="", font=("Arial", 14))
        self.result_label.grid(row=1, column=1, padx=20)

        self.computer_choice_label = tk.Label(self.root)
        self.computer_choice_label.grid(row=1, column=2, padx=20)

        # Play again button
        self.play_again_button = tk.Button(self.root, text="Play Again", command=self.reset, state=tk.DISABLED)
        self.play_again_button.grid(row=2, column=1, pady=(0, 10))  # Moved to row=2, and adjusted pady

    def start_game(self):
        # Get the result from the game
        user_choice, computer_choice, outcome = play_rock_paper_scissors()
        print(f"User Choice: {user_choice}, Computer Choice: {computer_choice}, Outcome: {outcome}")

        user_choice_index = self.map_choice_to_index(user_choice)
        computer_choice_index = self.map_choice_to_index(computer_choice)
        
        # Debug prints for indexes
        print(f"User Choice Index: {user_choice_index}, Computer Choice Index: {computer_choice_index}")

        # Update the labels with images if indices are valid
        if 0 <= user_choice_index < len(self.images):
            self.user_choice_label.config(image=self.images[user_choice_index])
        else:
            self.user_choice_label.config(text="Invalid user choice")

        if 0 <= computer_choice_index < len(self.images):
            self.computer_choice_label.config(image=self.images[computer_choice_index])
        else:
            self.computer_choice_label.config(text="Invalid computer choice")

        # Display the result and set the mouth image
        result_text = f"Computer chose {computer_choice}.\n"
        
        if outcome == "tie":
            result_text += "It's a tie!"
            mouth_index = 8  # Normal mouth image
            audio_file = None
        elif outcome == "win":
            result_text += "You win!"
            mouth_index = 5  # Win mouth image
            
        elif outcome == "lose":
            result_text += "You lose!"
            mouth_index = 6  # Lose mouth image
            

        # Ensure mouth_index is valid
        if 0 <= mouth_index < len(self.images):
            self.mouth_label.config(image=self.images[mouth_index])
        else:
            print(f"Error: Mouth image index {mouth_index} is out of range.")

        self.result_label.config(text=result_text)
        
        # Play the audio if applicable
        if audio_file:
            self.root.after(1000, audio_file)  # Delay in milliseconds (1000 ms = 1 second)
        
        # Enable the "Play Again" button
        self.play_again_button.config(state=tk.NORMAL)
        
        # Disable the "Start Game" button
        self.start_button.config(state=tk.DISABLED)

        # Update the header image randomly
        self.update_header_image()

    def update_header_image(self):
        # Randomly select an eyes image
        if len(self.images) >= 5:
            eyes_images_indices = [3, 4]  # Indices for eyesleft and eyesright images
            selected_index = random.choice(eyes_images_indices)
            self.header_label.config(image=self.images[selected_index])
        else:
            print("Error: Not enough images loaded for header.")

    def map_choice_to_index(self, choice):
        """ Map the choice string to the index of the image. """
        choices = ["rock", "paper", "scissor"]  # Ensure correct spelling
        try:
            index = choices.index(choice)
            print(f"Mapping choice '{choice}' to index {index}")  # Debug print
            return index
        except ValueError:
            print(f"Error: '{choice}' is not a valid choice.")
            return -1  # Return an invalid index to handle the error

    def reset(self):
        # Clear result label and reset buttons
        self.result_label.config(text="")
        self.user_choice_label.config(image="")
        self.computer_choice_label.config(image="")
        
        # Reset to normal mouth image
        if len(self.images) > 8:
            self.mouth_label.config(image=self.images[8])
        else:
            print("Error: Index 8 is out of range for images list.")

        self.play_again_button.config(state=tk.DISABLED)
        self.start_button.config(state=tk.NORMAL)

if __name__ == "__main__":
    root = tk.Tk()
    app = RockPaperScissorsApp(root)
    root.mainloop()
