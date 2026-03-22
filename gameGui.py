import tkinter as tk  # Import tkinter for GUI elements
from game import Game


class GameGUI:
    def __init__(self, game):
        """Initialize the GameGUI class with a Game instance."""
        self.game = game
        self.root = tk.Tk()
        self.root.geometry("600x800")
        self.root.configure(bg="black")
        self.root.title("SNHU Apocalypse")
        self.root.tk_setPalette(background="black")
        self.create_widgets()

    # Display game instructions and current status in the GUI
    def show_game_instructions(self):
        """Display the game instructions in the GUI."""
        self.game_text.config(state="normal")
        self.game_text.delete("1.0", tk.END)  # Clear old text
        self.game_text.insert(
            tk.END, self.game.game_instructions()
        )  # Insert instructions
        self.game_text.config(state="disabled")
        # Start game button
        self.start_button = tk.Button(
            self.root,
            text="Start Game",
            font=("Chalkduster", 14),
            fg="red",
            bg="white",
            command=self.start_game,
        )
        self.start_button.pack(pady=10)

    # Start the game by updating the GUI and removing the start button
    def start_game(self):
        """Start the game by updating the GUI and removing the start button."""
        self.start_button.destroy()  # Remove the start button
        self.button_frame.pack(pady=10)  # Show the button frame for navigation buttons
        self.update_gui()  # Update the GUI with the initial game state

    # Create and pack the widgets for the game GUI
    def create_widgets(self):
        """Create and pack the widgets for the game GUI."""
        # Game title label
        self.title_label = tk.Label(
            self.root,
            text="SNHU Apocalypse",
            font=("Chalkduster", 24, "bold"),
            fg="red",
            bg="black",
        )
        self.title_label.pack(pady=20)

        # Room image label
        self.room_image_label = tk.Label(self.root, bg="black")
        self.room_image_label.pack(pady=10)

        # Text widget to display game messages and status
        self.game_text = tk.Text(
            self.root,
            height=10,
            width=50,
            font=("Chalkduster", 12),
            fg="white",
            bg="black",
            state="disabled",
        )
        self.game_text.pack(pady=10)

        # Button frame for navigation buttons
        self.button_frame = tk.Frame(self.root, bg="black")

        # Pick up item button - hidden until needed
        self.pickup_button = tk.Button(
            self.root,
            text="Pick Up Item",
            font=("Chalkduster", 12),
            fg="green",
            bg="white",
            command=self.pick_up_item,
            state="disabled",
        )
        self.pickup_button.pack(pady=5)
        self.pickup_button.pack_forget()  # Hide the pick up item button until it's needed

    def update_gui(self):
        """Update the GUI elements based on the current game state."""

        # Display the current status of the player and room in the game_text widget
        status = self.game.player_status()

        # Load and display the room image
        room_name = self.game.player.current_room.name.lower().replace(
            " ", "_"
        )  # Convert room name to lowercase and replace spaces with underscores for file naming
        image_path = f"images/{room_name}.png"
        image = tk.PhotoImage(file=image_path)
        self.room_image_label.config(image=image)
        self.room_image_label.image = (
            image  # Keep reference to prevent garbage collection
        )

        # Check win/lose condition if player is in the Exit room and update the status accordingly
        if self.game.player.current_room.name == "Exit":
            status += self.game.check_win_lose()
            self.game_text.config(state="normal")
            self.game_text.delete("1.0", tk.END)
            self.game_text.insert(tk.END, status)
            self.game_text.config(state="disabled")
            for widget in self.button_frame.winfo_children():
                widget.destroy()
            self.pickup_button.pack_forget()  # Hide pickup button at game over

            # Restart button to allow player to play again after game over
            # Restart game button
            self.restart_button = tk.Button(
                self.button_frame,
                text="Play Again",
                font=("Chalkduster", 14),
                fg="red",
                bg="white",
                command=self.restart_game,
            )
            self.restart_button.pack(pady=10)
            return  # Exit the update_gui function early since the game is over

        # Update the game_text widget with the current status
        self.game_text.config(state="normal")
        self.game_text.delete("1.0", tk.END)  # clear old text
        self.game_text.insert(tk.END, status)  # insert new text
        self.game_text.config(state="disabled")

        # Destroy old navigation buttons if they exist
        for widget in self.button_frame.winfo_children():
            widget.destroy()

        # Gets valid moves for the current room and creates buttons for each valid move
        valid_moves = self.game.player.current_room.get_exits()

        # Update button states based on valid moves
        for direction in valid_moves:
            button = tk.Button(
                self.button_frame,
                text=valid_moves[direction].name,
                font=("Chalkduster", 12),
                fg="green",
                bg="white",
                command=lambda d=direction: self.move(d),
            )
            button.pack(side=tk.LEFT, padx=5)

        # Show or hide the pick up button based on whether the room has an item
        if self.game.player.current_room.has_item():
            self.pickup_button.pack(pady=5)
            self.pickup_button.config(state="normal", fg="green")
        else:
            self.pickup_button.pack_forget()

    def move(self, direction):
        """Move the player in the specified direction and update the GUI."""
        self.game.player.move(direction)
        self.update_gui()

    def pick_up_item(self):
        """Pick up the item in the current room and update the GUI."""
        current_room = self.game.player.current_room
        if current_room.has_item():
            item = current_room.get_item()
            self.game.player.add_to_inventory(item)
            current_room.remove_item()
            self.update_gui()  # Update the GUI to reflect the change in inventory and room status

    def restart_game(self):
        """Restart the game by resetting the game state and updating the GUI."""
        self.game = Game()
        self.restart_button.destroy()
        self.update_gui()

    def main_loop(self):
        """Start the main loop of the game GUI."""
        self.show_game_instructions()  # Show instructions in the GUI at the start of the game
        self.root.mainloop()  # Start the Tkinter event loop
