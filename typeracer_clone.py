import tkinter
import api_module


class RandomProject:

    def __init__(self):
        self.window = tkinter.Tk()
        self.textBox = tkinter.Text(self.window, wrap=tkinter.WORD)
        self.textBox.tag_config('GREEN', foreground='green')
        self.textBox.tag_config('RED', foreground='red')
        self.textBox.tag_config('DEFAULT', foreground='black')
        # self.textBox2 = tkinter.Entry(self.window)
        self.wpm = 0
        self.quote, self.author, self.book_title = api_module.get_random_quote()
        self.wpm_label = tkinter.Label(self.window, text=f'WPM: {str(self.wpm)}')
        self.quote_label = tkinter.Label(self.window, text=self.quote, wraplength=500)
        self.start_button = tkinter.Button(self.window)
        self.typos = 0
        self.typos_label = tkinter.Label(self.window, text='Typos: ' + str(self.typos))
        self.istypo = False
        self.gameOver = False
        self.author_label = tkinter.Label(self.window, text=f'- {self.author}, {self.book_title}')

        self.timer = 0

    def run(self):
        try:
            self.quote_label.grid(row=0, column=0)
            self.author_label.grid(row=1, column=1)
            self.textBox.grid(row=2, column=0, padx=10, pady=10)
            self.wpm_label.grid(row=3, column=0)
            self.typos_label.grid(row=3, column=1)
            self.start_button.grid(row=2, column=1)
            # self.textBox.bind('<Return>', self._on_return)
            self._update_wpm()
            self._update_text()
            self._handle_typos(self.typos)
            self.window.mainloop()
        finally:
            pass

    # def _on_return(self, event):
    #     print(self.textBox.get('0.0', tkinter.END))
    #     self.textBox.delete('0.0', tkinter.END)

    def _update_wpm(self):
        print(self.gameOver)
        self.window.after(100, self._update_wpm)
        if not self.gameOver:

            text = self.textBox.get('0.0', tkinter.END).split()

            self.timer += (0.1 / 60)
            self.wpm = len(text) / self.timer
            self.wpm_label.configure(text='WPM: {:.2f}'.format(self.wpm))

    def _update_text(self):
        self.window.after(150, self._update_text)
        if not self.gameOver:
            user_text = self.textBox.get('0.0', tkinter.END).rstrip('\n')
            if user_text == self.quote:
                self.gameOver = True
                self.wpm_label.configure(text='Congratulations! Final WPM: {:.2f}'.format(self.wpm))
                self.start_button.configure(text='Play again', command=self._reset_game)

            first_incorrect_character = -1
            for index in range(len(user_text)):

                if user_text[index] != self.quote[index]:

                    first_incorrect_character = index
                    break
            self._handle_text_coloring(first_incorrect_character)

    def _handle_text_coloring(self, first_incorrect_character):
        if first_incorrect_character > -1:
            self.istypo = True
            self.textBox.tag_add('GREEN', '0.0', f'0.0 + {first_incorrect_character}c')
            self.textBox.tag_add('RED', f'0.0 + {first_incorrect_character}c', tkinter.END)
        else:
            self.istypo = False
            self.textBox.tag_add('GREEN', '0.0', tkinter.END)

    def _handle_typos(self, current):
        after = self.istypo

        self.window.after(100, self._handle_typos, after)

        if not current and after:
            self.typos += 1
        self.typos_label.configure(text='Typos: ' + str(self.typos))

    def _reset_game(self):
        self.wpm = 0
        self.timer = 0
        self.typos = 0
        self.quote, self.author, self.book_title = api_module.get_random_quote()
        self.quote_label.configure(text=self.quote)
        self.author_label.configure(text=f'- {self.author}, {self.book_title}')
        self.textBox.delete('0.0', tkinter.END)
        self.istypo = False
        self.gameOver = False


if __name__ == '__main__':
    RandomProject().run()
