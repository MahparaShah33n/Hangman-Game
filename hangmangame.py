import tkinter as tk
import random

WORDS_AND_HINTS = {
    "python": "I’m a snake, yet I code. What am I?",
    "apple": "I fall from trees and keep doctors away. What am I?",
    "robot": "I can move and talk, but I'm not alive. What am I?",
    "house": "I have walls and a roof, but I'm not a box. What am I?",
    "music": "I have notes but no letters. What am I?",
    "moon": "I light the night without a flame. What am I?",
    "elephant": "I have big ears and walk with pride. What am I?",
    "rainbow": "I come with rain and colors wide. What am I?",
    "pencil": "I help you draw then shrink and die. What am I?",
    "clock": "I tick all day and never cry. What am I?",
    "library": "I'm full of books where stories lie. What am I?",
    "butterfly": "I flutter past with wings that fly. What am I?",
    "mountain": "I touch the clouds and stand up high. What am I?",
    "doctor": "I cure your pain and don’t ask why. What am I?",
    "school": "I teach you things from low to high. What am I?",
    "guitar": "I sing with strings, just give me a try. What am I?",
    "spider": "I spin my web where insects die. What am I?",
    "kitchen": "I’m where you cook and food will fry. What am I?",
    "fireman": "I fight the flames and don’t say bye. What am I?",
    "candle": "I light the dark and melt nearby. What am I?",
    "pirate": "I search for gold with patch on eye. What am I?",
    "desert": "I’m hot and dry with sand supply. What am I?",
    "bicycle": "I ride on roads with wheels that glide. What am I?",
    "camera": "I freeze your smile before it’s gone by. What am I?",
    "hospital": "I help you heal when tears are nigh. What am I?",
    "chocolate": "I melt so sweet, you can't deny. What am I?",
    "planet": "I spin in space and float up high. What am I?",
    "detective": "I find the truth and catch the lie. What am I?",
    "bridge": "I help you cross from side to side. What am I?",
    "laptop": "I’m smart and small and live inside. What am I?",
    "volcano": "I burst with fire from deep inside. What am I?",
    "iceberg": "I float in seas, my bulk I hide. What am I?",
    "astronaut": "I roam in space and do not cry. What am I?",
    "garden": "I bloom with life and bees that fly. What am I?"
}

class HangmanGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Hangman Game")
        self.root.geometry("700x600")
        self.word, self.hint = random.choice(list(WORDS_AND_HINTS.items()))
        self.guessed_letters = []
        self.max_attempts = 6
        self.attempts_left = self.max_attempts
        self.lives = 3
        self.time_limit = 15
        self.time_left = self.time_limit
        self.timer = None
        self.timer_running = False
        self.won = False

        self.word_display = tk.StringVar()
        self.status_display = tk.StringVar()
        self.hint_display = tk.StringVar(value=f"Hint: {self.hint}")
        self.heart_display = tk.StringVar()
        self.update_hearts()

        self.create_widgets()
        self.update_display()
        self.start_timer()

    def create_widgets(self):
        title_frame = tk.Frame(self.root)
        title_frame.pack(pady=10)
        rainbow_colors = ["red", "orange", "yellow", "green", "blue", "indigo", "violet"]
        title_text = "Hangman Game"
        for i, char in enumerate(title_text):
            color = rainbow_colors[i % len(rainbow_colors)]
            tk.Label(title_frame, text=char, font=("Comic Sans MS", 20, "bold"), fg=color).pack(side="left")

        tk.Label(self.root, textvariable=self.hint_display, font=("Comic Sans MS", 14), fg="navy").pack(pady=5)
        tk.Label(self.root, textvariable=self.word_display, font=("Courier", 24)).pack(pady=10)
        self.heart_label = tk.Label(self.root, textvariable=self.heart_display, font=("Arial", 16), fg="red")
        self.heart_label.pack(pady=5)

        self.buttons_frame = tk.Frame(self.root)
        self.buttons_frame.pack()
        self.letter_buttons = {}
        for i, letter in enumerate("abcdefghijklmnopqrstuvwxyz"):
            btn = tk.Button(self.buttons_frame, text=letter, width=4, height=2, bg="pink",
                            command=lambda l=letter: self.guess_letter(l))
            btn.grid(row=i // 9, column=i % 9, padx=3, pady=3)
            self.letter_buttons[letter] = btn

        tk.Label(self.root, textvariable=self.status_display, font=("Arial", 14)).pack(pady=10)

        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=5)

        self.restart_btn = tk.Button(btn_frame, text="Restart Game", bg="light blue", command=self.restart_game, state='disabled')
        self.restart_btn.grid(row=0, column=0, padx=10)

        self.next_btn = tk.Button(btn_frame, text="Next Word", bg="light blue", command=self.next_word, state='disabled')
        self.next_btn.grid(row=0, column=1, padx=10)

        self.timer_canvas = tk.Canvas(self.root, width=100, height=100)
        self.timer_canvas.pack(pady=5)
        self.timer_text = self.timer_canvas.create_text(50, 50, text=str(self.time_limit), font=("Arial", 18, "bold"), fill="navy")

    def update_hearts(self):
        self.heart_display.set("❤️ " * self.lives)

    def start_timer(self):
        self.time_left = self.time_limit
        self.timer_running = True
        self.update_timer()

    def update_timer(self):
        self.timer_canvas.delete("arc")
        angle = 360 * (self.time_left / self.time_limit)
        self.timer_canvas.create_arc(10, 10, 90, 90, start=90, extent=-angle, style="arc", width=6, outline="blue")
        self.timer_canvas.itemconfig(self.timer_text, text=str(self.time_left))

        if self.time_left > 0:
            self.time_left -= 1
            self.timer = self.root.after(1000, self.update_timer)
        else:
            self.timer_running = False
            if not self.won:
                self.status_display.set("⏰ Time's up! You lost this round.")
                self.lives -= 1
                self.update_hearts()
                if self.lives == 0:
                    self.status_display.set("💀 Game Over! No lives left.")
                self.disable_buttons()

    def guess_letter(self, letter):
        if letter in self.guessed_letters or self.attempts_left <= 0:
            return

        if self.timer_running:
            self.root.after_cancel(self.timer)
        self.start_timer()

        self.guessed_letters.append(letter)
        btn = self.letter_buttons[letter]
        btn.config(state='disabled')

        if letter in self.word:
            btn.config(bg='light green', fg='black')
        else:
            btn.config(text='❌', fg='red')
            self.attempts_left -= 1

        self.update_display()

        if self.attempts_left == 0:
            self.status_display.set(f"You lost! The word was '{self.word}'.")
            self.lives -= 1
            self.update_hearts()
            self.disable_buttons()
            if self.lives == 0:
                self.status_display.set("💀 Game Over! No lives left.")
        elif all(l in self.guessed_letters for l in self.word):
            self.status_display.set("🎉 You won! Click 'Next Word'")
            self.won = True
            self.disable_buttons()

    def update_display(self):
        display_word = ' '.join([letter if letter in self.guessed_letters else '_' for letter in self.word])
        self.word_display.set(display_word)
        self.status_display.set(f"Attempts left: {self.attempts_left}")

    def disable_buttons(self):
        for btn in self.letter_buttons.values():
            btn.config(state='disabled')
        self.restart_btn.config(state='normal')
        self.next_btn.config(state='normal')

    def restart_game(self):
        self.lives = 3
        self.next_word()

    def next_word(self):
        if self.won:
            self.lives += 1
        self.word, self.hint = random.choice(list(WORDS_AND_HINTS.items()))
        self.hint_display.set(f"Hint: {self.hint}")
        self.guessed_letters = []
        self.attempts_left = self.max_attempts
        self.won = False
        for letter, btn in self.letter_buttons.items():
            btn.config(state='normal', text=letter, bg='pink', fg='black')
        self.restart_btn.config(state='disabled')
        self.next_btn.config(state='disabled')
        self.status_display.set("")
        self.update_hearts()
        self.update_display()
        self.start_timer()

if __name__ == "__main__":
    root = tk.Tk()
    game = HangmanGame(root)
    root.mainloop()
