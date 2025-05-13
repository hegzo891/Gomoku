import tkinter as tk
from tkinter import messagebox, ttk
from board import GomokuBoard
from players.human import HumanPlayer
from players.minimax_ai import MinimaxAI
from players.alphabeta_ai import AlphaBetaAI
from utils.constants import HUMAN, AI, EMPTY

class GomokuGame:
    def __init__(self, root, size=5, game_mode="Human vs AI", ai1_type="AlphaBeta", ai1_depth=2, ai2_type="AlphaBeta", ai2_depth=2):
        self.root = root
        self.root.title("✨ Gomoku Game")
        self.root.configure(bg="#f8f9fa")
        
        # Set minimum window size
        self.root.minsize(500, 500)
        
        # Make the window resizable
        self.root.resizable(True, True)
        
        # Configure grid to be responsive
        for i in range(size + 2):  # +2 for title and status bar
            self.root.grid_rowconfigure(i, weight=1)
        for i in range(size):
            self.root.grid_columnconfigure(i, weight=1)
        
        self.board = GomokuBoard(size)
        self.human_player = HumanPlayer()
        
        # Initialize AI players based on selected types
        self.ai_player_1 = self.create_ai(ai1_type, ai1_depth)
        self.ai_player_2 = self.create_ai(ai2_type, ai2_depth) if game_mode == "AI vs AI" else None
        
        if game_mode == "AI vs AI":
            self.current_player = AI
        else:
            self.current_player = HUMAN
        self.size = size
        self.buttons = {}
        self.game_active = True
        self.game_mode = game_mode
        
        # Beautiful color palette
        self.colors = {
            'background': '#f0f2f5',
            'title_bg': '#6c5ce7',
            'title_fg': 'white',
            'button_bg': '#dfe6e9',
            'button_active': '#b2bec3',
            'button_hover': '#a5b1c2',
            'human_color': 'black',
            'ai_color': 'white',
            'status_bg': '#6c5ce7',
            'status_fg': 'white',
            'button_border': '#636e72',
            'win_highlight': '#fdcb6e',
            'button_disabled': '#b2bec3',
            'stone_bg': '#dfe6e9',
            'board_bg': '#dfe6e9',
            'stone_shadow': '#636e72'
        }
        
        # Title Frame with gradient effect
        title_frame = tk.Frame(self.root, bg=self.colors['title_bg'])
        title_frame.grid(row=0, column=0, columnspan=size, sticky="nsew", padx=5, pady=(5, 10))
        
        title = tk.Label(
            title_frame,
            text="Gomoku Game",
            font=("Segoe UI Emoji", 24, "bold"),
            bg=self.colors['title_bg'],
            fg=self.colors['title_fg'],
            padx=10,
            pady=10
        )
        title.pack(expand=True, fill='both')
        
        # Create the GUI buttons for the game board
        self.canvas = tk.Canvas(bg=self.colors['board_bg'])
        for i in range(self.size):
            for j in range(self.size):
                button = tk.Button(
                    self.root,
                    text=' ',
                    font=("Segoe UI Emoji", 24),
                    width=2,
                    height=1,
                    bg=self.colors['button_bg'],
                    fg="#2d3436",
                    activebackground=self.colors['button_active'],
                    relief="flat",
                    # image=self.create_stone_image(),
                    borderwidth=1,
                    highlightthickness=1,
                    highlightbackground=self.colors['button_border'],
                    highlightcolor=self.colors['button_border'],
                    command=lambda row=i, col=j: self.make_move(row, col)
                )
                button.grid(row=i + 1, column=j, padx=3, pady=3, sticky="nsew")
                self.buttons[(i, j)] = button
        
        # Status bar
        self.status_var = tk.StringVar()
        self.update_status_text()
        
        status_bar = tk.Label(
            self.root,
            textvariable=self.status_var,
            font=("Segoe UI Emoji", 12, "bold"),
            bg=self.colors['status_bg'],
            fg=self.colors['status_fg'],
            padx=10,
            pady=5,
            anchor='center'
        )
        status_bar.grid(row=self.size + 1, column=0, columnspan=self.size, sticky="nsew", padx=5, pady=(10, 5))
        
        # Hover effects on buttons
        self.create_hover_effect()
        
        # Add menu
        self.create_menu()
        
        # Center the window
        self.center_window()
        
        # If it's AI's turn first, make the move
        if self.current_player == AI and self.game_mode != "Human vs Human":
            self.root.after(500, self.ai_move)

    def create_ai(self, ai_type, depth):
        """Create an AI player based on the selected type and depth"""
        if ai_type == "Minimax":
            return MinimaxAI(depth)
        else:
            return AlphaBetaAI(depth)

    def update_status_text(self):
        """Update the status text based on game mode and current player"""
        if self.game_mode == "Human vs AI":
            status_text = "Your turn (Black ⚫)" if self.current_player == HUMAN else "AI's turn (White ⚪)"
        elif self.game_mode == "AI vs AI":
            status_text = f"AI 1's turn (Black ⚫)" if self.current_player == HUMAN else "AI 2's turn (White ⚪)"
        else:  # Human vs Human
            status_text = "Player 1's turn (Black ⚫)" if self.current_player == HUMAN else "Player 2's turn (White ⚪)"
        
        self.status_var.set(status_text)

    def center_window(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def create_menu(self):
        menubar = tk.Menu(self.root)
        
        # Game menu
        game_menu = tk.Menu(menubar, tearoff=0)
        game_menu.add_command(label="New Game", command=self.prompt_new_game)
        game_menu.add_separator()
        game_menu.add_command(label="Exit", command=self.root.quit)
        menubar.add_cascade(label="Game", menu=game_menu)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="About", command=self.show_about)
        menubar.add_cascade(label="Help", menu=help_menu)
        
        self.root.config(menu=menubar)

    def show_about(self):
        messagebox.showinfo(
            "About Gomoku",
            "Gomoku Game\n\nA beautiful Python implementation of the classic game\n"
            "with AI opponents using Minimax and Alpha-Beta algorithms.\n\n"
            "First to get 5 in a row wins!\n"
            "Black (⚫) vs White (⚪)"
        )

    def prompt_new_game(self):
        if messagebox.askyesno("New Game", "Are you sure you want to start a new game?"):
            self.root.destroy()
            main()

    def create_hover_effect(self):
        for button in self.buttons.values():
            button.bind("<Enter>", lambda e, b=button: b.config(bg=self.colors['button_hover']))
            button.bind("<Leave>", lambda e, b=button: b.config(bg=self.colors['button_bg']))

    def make_move(self, row, col):
        if not self.game_active:
            return
            
        if self.board.is_valid_move(row, col):
            self.board.make_move(row, col, self.current_player)
            self.update_board()
            
            # Check for winner
            if self.board.check_winner(self.current_player):
                self.handle_win()
                return
            
            # Check for draw
            if self.board.is_full():
                self.end_game("It's a draw!")
                return

            self.switch_player()

            # AI makes a move if it's AI's turn
            if self.current_player == AI and self.game_mode != "Human vs Human":
                self.status_var.set("AI is thinking..." if self.game_mode == "Human vs AI" else 
                                 f"{'AI 1' if self.current_player == HUMAN else 'AI 2'} is thinking...")
                self.root.update()
                self.root.after(500, self.ai_move)  # Delay for realism

    def handle_win(self):
        """Handle the win condition with appropriate message"""
        if self.game_mode == "Human vs AI":
            winner = "You win! (Black ⚫)" if self.current_player == HUMAN else "AI wins! (White ⚪)"
        elif self.game_mode == "AI vs AI":
            winner = "AI 1 wins! (Black ⚫)" if self.current_player == HUMAN else "AI 2 wins! (White ⚪)"
        else:  # Human vs Human
            winner = "Player 1 wins! (Black ⚫)" if self.current_player == HUMAN else "Player 2 wins! (White ⚪)"
        
        self.end_game(winner)
        
    def ai_move(self):
        if not self.game_active:
            return
        
        if self.game_mode == "AI vs AI":
            ai_player = self.ai_player_1 if self.current_player == HUMAN else self.ai_player_2
        else:
            ai_player = self.ai_player_1
        
        move = ai_player.get_move(self.board)
        if move:
            row, col = move
            self.board.make_move(row, col, self.current_player)
            self.update_board()

            if self.board.check_winner(self.current_player):
                self.handle_win()
                return
                
            if self.board.is_full():
                self.end_game("It's a draw!")
                return

            self.switch_player()

            
            # If game is still active and it's AI's turn, make next move
            if self.game_active and ((self.game_mode == "AI vs AI") or 
                                (self.game_mode == "Human vs AI" and self.current_player == AI)):
                self.root.after(500, self.ai_move)
                
    def update_board(self):
        for i in range(self.size):
            for j in range(self.size):
                text = self.board.board[i][j]
                button = self.buttons[(i, j)]
                
                if text == HUMAN:
                    # Black stone (⚫)
                    button.config(
                        text='⚫',
                        font=("Segoe UI Emoji", 24),
                        fg='black',
                        bg=self.colors['stone_bg'],
                        disabledforeground='black'
                    )
                elif text == AI:
                    # White stone (⚪)
                    button.config(
                        text='⚪',
                        font=("Segoe UI Emoji", 24),
                        fg='white',
                        bg=self.colors['stone_bg'],
                        disabledforeground='white'
                    )
                else:
                    button.config(
                        text=' ',
                        font=("Segoe UI Emoji", 24),
                        fg="#2d3436",
                        bg=self.colors['button_bg']
                    )
                button.config(state='disabled' if text != EMPTY else 'normal')

    def switch_player(self):
        self.current_player = HUMAN if self.current_player == AI else AI
        self.update_status_text()

    def end_game(self, message):
        self.game_active = False
        
        # Highlight winning cells if any (and if it's not a draw)
        if "draw" not in message.lower():
            winner = HUMAN if "Black" in message or "Player 1" in message or "AI 1" in message else AI
            winning_cells = self.board.get_winning_cells() if hasattr(self.board, 'get_winning_cells') else []
            
            for (i, j) in winning_cells:
                self.buttons[(i, j)].config(bg=self.colors['win_highlight'])
        
        # Show game over message
        if messagebox.askyesno("Game Over", f"{message}\n\nWould you like to play again?"):
            self.root.destroy()
            main()

def main():
    def validate_size():
        try:
            size = int(size_entry.get())
            if size < 5:
                raise ValueError("Board size must be at least 5.")
            if size > 15:
                if not messagebox.askokcancel("Large Board", "Boards larger than 15 may not display well. Continue?"):
                    return False
            return True
        except ValueError as e:
            messagebox.showerror("Invalid input", str(e))
            return False

    def get_ai_settings(frame, player_num):
        """Create AI selection widgets for one player"""
        tk.Label(frame, text=f"AI {player_num} Type:", bg="#f8f9fa").grid(row=0, column=0, padx=5, sticky="w")
        
        ai_type = tk.StringVar(value="AlphaBeta")
        tk.Radiobutton(frame, text="Alpha-Beta", variable=ai_type, value="AlphaBeta", bg="#f8f9fa").grid(row=0, column=1, padx=5, sticky="w")
        tk.Radiobutton(frame, text="Minimax", variable=ai_type, value="Minimax", bg="#f8f9fa").grid(row=0, column=2, padx=5, sticky="w")
        
        tk.Label(frame, text="Depth:", bg="#f8f9fa").grid(row=0, column=3, padx=5, sticky="w")
        depth = tk.Spinbox(frame, from_=1, to=5, width=2)
        depth.grid(row=0, column=4, padx=5, sticky="w")
        depth.delete(0, "end")
        depth.insert(0, "2")
        
        return ai_type, depth

    def update_ai_settings():
        """Show/hide AI settings based on game mode"""
        if mode_var.get() == "Human vs AI":
            ai1_frame.pack(fill="x", pady=5)
            ai2_frame.pack_forget()
        elif mode_var.get() == "AI vs AI":
            ai1_frame.pack(fill="x", pady=5)
            ai2_frame.pack(fill="x", pady=5)
        else:  # Human vs Human
            ai1_frame.pack_forget()
            ai2_frame.pack_forget()

    def start_game():
        if not validate_size():
            return

        # Store the settings before destroying the window
        size = int(size_entry.get())
        game_mode = mode_var.get()
        
        if game_mode == "Human vs AI":
            ai1_type = ai1_type_var.get()
            ai1_depth = int(ai1_depth_spin.get()) if hasattr(ai1_depth_spin, 'get') else 2
            ai_settings = (ai1_type, ai1_depth)
        elif game_mode == "AI vs AI":
            ai1_type = ai1_type_var.get()
            ai1_depth = int(ai1_depth_spin.get()) if hasattr(ai1_depth_spin, 'get') else 2
            ai2_type = ai2_type_var.get()
            ai2_depth = int(ai2_depth_spin.get()) if hasattr(ai2_depth_spin, 'get') else 2
            ai_settings = (ai1_type, ai1_depth, ai2_type, ai2_depth)
        else:
            ai_settings = None

        input_window.destroy()
        
        root = tk.Tk()
        try:
            root.iconbitmap('gomoku.ico')
        except:
            pass
        style = ttk.Style()
        style.theme_use('clam')
        
        # Create game with stored settings
        if game_mode == "Human vs AI":
            game = GomokuGame(root, size, game_mode, *ai_settings)
        elif game_mode == "AI vs AI":
            game = GomokuGame(root, size, game_mode, ai1_type, ai1_depth, ai2_type, ai2_depth)
        else:  # Human vs Human
            game = GomokuGame(root, size, game_mode)
            
        root.mainloop()

    input_window = tk.Tk()
    input_window.title("Gomoku - Game Setup")
    input_window.configure(bg="#f8f9fa")
    input_window.resizable(False, False)

    window_width = 600
    window_height = 600
    screen_width = input_window.winfo_screenwidth()
    screen_height = input_window.winfo_screenheight()
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)
    input_window.geometry(f'{window_width}x{window_height}+{x}+{y}')

    main_frame = tk.Frame(input_window, bg="#f8f9fa", padx=30, pady=30)
    main_frame.pack(expand=True, fill='both')

    title = tk.Label(
        main_frame,
        text="Gomoku Setup",
        font=("Segoe UI Emoji", 24, "bold"),
        bg="#f8f9fa",
        fg="#6c5ce7"
    )
    title.pack(pady=(10, 20))

    # Game mode selection
    mode_frame = tk.Frame(main_frame, bg="#f8f9fa")
    mode_frame.pack(pady=10, fill="x")
    
    tk.Label(mode_frame, text="Game Mode:", font=("Segoe UI Emoji", 12), bg="#f8f9fa").pack(anchor="w")
    
    mode_var = tk.StringVar(value="Human vs AI")
    modes = [("Human vs AI", "Human vs AI"), 
             ("AI vs AI", "AI vs AI"), 
             ("Human vs Human", "Human vs Human")]
    
    for text, mode in modes:
        tk.Radiobutton(mode_frame, text=text, variable=mode_var, value=mode, 
                      bg="#f8f9fa").pack(anchor="w")

    # Board size selection
    input_frame = tk.Frame(main_frame, bg="#f8f9fa")
    input_frame.pack(pady=10, fill="x")
    
    tk.Label(input_frame, text="Board Size (5-15):", font=("Segoe UI Emoji", 12), bg="#f8f9fa").grid(row=0, column=0, sticky="w")
    
    size_entry = ttk.Entry(input_frame, font=("Segoe UI Emoji", 12), width=5, justify='center')
    size_entry.grid(row=0, column=1, padx=10, sticky="w")
    size_entry.insert(0, "5")

    # AI settings
    ai_settings_frame = tk.Frame(main_frame, bg="#f8f9fa")
    ai_settings_frame.pack(pady=10, fill="x")
    
    # AI 1 settings (for Human vs AI or AI vs AI)
    ai1_frame = tk.Frame(ai_settings_frame, bg="#f8f9fa")
    ai1_type_var, ai1_depth_spin = get_ai_settings(ai1_frame, 1)
    
    # AI 2 settings (only for AI vs AI)
    ai2_frame = tk.Frame(ai_settings_frame, bg="#f8f9fa")
    ai2_type_var, ai2_depth_spin = get_ai_settings(ai2_frame, 2)
    
    # Set up the initial visibility
    update_ai_settings()
    
    # Bind the mode change to update AI settings visibility
    mode_var.trace_add('write', lambda *args: update_ai_settings())

    start_button = tk.Button(
        main_frame,
        text="Start Game",
        font=("Segoe UI Emoji", 14, "bold"),
        command=start_game,
        bg="#6c5ce7",
        fg="white",
        activebackground="#5649b5",
        activeforeground="white",
        relief="flat",
        padx=20,
        pady=10,
        bd=0,
        highlightthickness=0
    )
    start_button.pack(pady=20)

    def on_enter(e): start_button.config(bg="#5649b5")
    def on_leave(e): start_button.config(bg="#6c5ce7")
    start_button.bind("<Enter>", on_enter)
    start_button.bind("<Leave>", on_leave)

    desc = tk.Label(
        main_frame,
        text="Gomoku is a strategy game where players alternate\n"
             "placing stones to form an unbroken line of five.\n\n"
             "Black: ⚫    White: ⚪",
        font=("Segoe UI Emoji", 11),
        bg="#f8f9fa",
        fg="#636e72"
    )
    desc.pack(pady=10)

    input_window.mainloop()

if __name__ == "__main__":
    main()