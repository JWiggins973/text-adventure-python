import tkinter as tk
from .game import Game

FONT = "Chalkduster"


class GameGUI:
    def __init__(self, game: Game) -> None:
        """Initialize the GameGUI class with a Game instance."""
        self.game = game
        self.root = tk.Tk()
        self.root.geometry("600x800")
        self.root.configure(bg="black")
        self.root.title("SNHU Apocalypse")
        # Force all child widgets to inherit the black background by default
        self.root.tk_setPalette(background="black")
        # Ensure the process exits cleanly when the window is closed
        self.root.protocol("WM_DELETE_WINDOW", self.root.destroy)
        self.create_widgets()

    def show_game_instructions(self) -> None:
        """Display the game instructions in the GUI."""
        self.game_text.config(state="normal")
        self.game_text.delete("1.0", tk.END)
        self.game_text.insert(tk.END, self.game.game_instructions())
        self.game_text.config(state="disabled")
        # Show a Start Game button so the player can read instructions before playing
        self.start_button = tk.Button(
            self.root,
            text="Start Game",
            font=(FONT, 14),
            fg="red",
            bg="white",
            command=self.start_game,
        )
        self.start_button.pack(pady=10)

    def start_game(self) -> None:
        """Start the game by updating the GUI and removing the start button."""
        self.start_button.destroy()
        # Reveal the navigation button frame now that the game has started
        self.button_frame.pack(pady=(2, 10))
        self.update_gui()

    def create_widgets(self) -> None:
        """Create and pack all widgets for the game GUI."""
        # Title label at the top of the window
        self.title_label = tk.Label(
            self.root,
            text="SNHU Apocalypse",
            font=(FONT, 24, "bold"),
            fg="red",
            bg="black",
        )
        self.title_label.pack(pady=20)

        # Placeholder label for the room image — updated each time the player moves
        self.room_image_label = tk.Label(self.root, bg="black")
        self.room_image_label.pack(pady=10)

        # Read-only text area for game messages — disabled to prevent player editing
        self.game_text = tk.Text(
            self.root,
            height=5,
            width=50,
            font=(FONT, 12),
            fg="white",
            bg="black",
            state="disabled",
        )
        self.game_text.pack(pady=(10, 2))

        # Frame to hold room navigation buttons — not packed yet, shown after Start is clicked
        self.button_frame = tk.Frame(self.root, bg="black")

        # Pick Up Item is a Label styled as a button because macOS ignores fg color on tk.Button
        # Hidden by default and shown only when the current room contains an item
        self.pickup_button = tk.Label(
            self.root,
            text="Pick Up Item",
            font=(FONT, 12),
            fg="green",
            bg="white",
            relief="solid",
            padx=8,
            pady=4,
        )
        # Bind press and release separately to show a visual click effect
        self.pickup_button.bind("<Button-1>", self._on_pickup_press)
        self.pickup_button.bind("<ButtonRelease-1>", self._on_pickup_release)
        self.pickup_button.pack(pady=5)
        self.pickup_button.pack_forget()  # Hidden until a room with an item is entered

    def _on_pickup_press(self, _: tk.Event) -> None:
        """Change pickup button colors to indicate it is being pressed."""
        self.pickup_button.config(bg="green", fg="white")

    def _on_pickup_release(self, _: tk.Event) -> None:
        """Reset pickup button colors and trigger the item pickup on release."""
        self.pickup_button.config(bg="white", fg="green")
        self.pick_up_item()

    def update_gui(self) -> None:
        """Coordinate all GUI updates based on the current game state."""
        self._update_room_image()
        status = self.game.player_status()
        # Exit room triggers game over flow — return early to skip normal updates
        if self.game.is_game_over():
            self._show_game_over(status)
            return
        self._update_status_text(status)
        self._update_nav_buttons()
        self._update_pickup_button()

    def _update_status_text(self, status: str) -> None:
        """Update the game text widget with the given status string."""
        # Must enable before writing and disable after to keep the widget read-only
        self.game_text.config(state="normal")
        self.game_text.delete("1.0", tk.END)
        self.game_text.insert(tk.END, status)
        self.game_text.config(state="disabled")

    def _update_room_image(self) -> None:
        """Load and display the image for the current room, or show a placeholder on failure."""
        room_name = self.game.get_current_room_name().lower().replace(" ", "_")
        # Strip any characters that could form a path traversal (e.g. "../")
        safe_name = "".join(c for c in room_name if c.isalnum() or c == "_")
        try:
            image = tk.PhotoImage(file=f"images/{safe_name}.png")
            self.room_image_label.config(image=image, text="")
            # Keep a reference on the label to prevent Python garbage collecting the image
            self.room_image_label.image = image
        except Exception:
            # Show a placeholder if the image file is missing rather than silently clearing
            self.room_image_label.config(
                image="",
                text="[ no image ]",
                fg="white",
                font=(FONT, 10),
            )
            self.room_image_label.image = None

    def _update_nav_buttons(self) -> None:
        """Rebuild navigation buttons for the current room's exits."""
        # Destroy old buttons before creating new ones for the current room
        for widget in self.button_frame.winfo_children():
            widget.destroy()
        for direction, room in self.game.get_current_room_exits().items():
            # d=direction captures the loop variable so each button calls move with its own direction
            tk.Button(
                self.button_frame,
                text=room.name,
                font=(FONT, 12),
                fg="green",
                bg="white",
                command=lambda d=direction: self.move(d),
            ).pack(side=tk.LEFT, padx=5)

    def _update_pickup_button(self) -> None:
        """Show or hide the pickup button based on whether the room has an item."""
        if self.game.current_room_has_item():
            # Place the pickup button above the nav buttons and align it to the left
            self.pickup_button.pack(
                pady=5, before=self.button_frame, anchor=tk.W, padx=10
            )
            self.pickup_button.config(fg="green")
        else:
            self.pickup_button.pack_forget()

    def _show_game_over(self, status: str) -> None:
        """Display the game over state with win/lose result and a Play Again button."""
        self._update_status_text(status + self.game.check_win_lose())
        # Clear navigation buttons since the game is over
        for widget in self.button_frame.winfo_children():
            widget.destroy()
        self.pickup_button.pack_forget()
        self.restart_button = tk.Button(
            self.button_frame,
            text="Play Again",
            font=(FONT, 14),
            fg="red",
            bg="white",
            command=self.restart_game,
        )
        self.restart_button.pack(pady=10)

    def move(self, direction: str) -> None:
        """Move the player in the specified direction and update the GUI."""
        moved = self.game.move(direction)
        if not moved:
            self._update_status_text(f"No exit to the {direction}.")
            return
        self.update_gui()

    def pick_up_item(self) -> None:
        """Pick up the item in the current room and update the GUI."""
        self.game.pick_up_item()
        self.update_gui()

    def restart_game(self) -> None:
        """Restart the game by resetting the game state and updating the GUI."""
        # Reset game state through the Game interface rather than creating a new instance
        self.game.reset()
        if hasattr(self, "restart_button"):
            self.restart_button.destroy()
        self.update_gui()

    def main_loop(self) -> None:
        """Start the main loop of the game GUI."""
        self.show_game_instructions()
        self.root.mainloop()
