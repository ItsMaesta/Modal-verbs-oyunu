import tkinter as tk
import win32gui, win32con
from tkinter import ttk, messagebox
import random

class ModalPanel(tk.Tk):
    def __init__(self, user_name):
        super().__init__()
        self.user_name = user_name
        self.title(f'{self.user_name}\'s Modal Verbs Panel')
        self.geometry('600x400')
        self.configure(background='#D6EAF8')  
        self.examples = [
            ("We ____ exercise regularly for good health.", 'should', 'Sağlık için düzenli olarak egzersiz yapmalısınız.'),
            ("You ____ go to the cinema tonight. It's going to be fun.", 'will', "Bu gece sinemaya gideceksiniz. Eğlenceli olacak."),
            ("She ____ play the piano very well when she was young.", 'could', "Gençken piyano çalabilirdi."),
            ("I ____ finish this project by tomorrow.", 'must', "Yarın bu projeyi bitirmeliyim."),
            ("He ____ be tired. He ran a marathon yesterday.", 'must', "Yorgun olmalı. Dün maraton koştu."),
            ("They ____ buy a new car. Their old one broke down.", 'need to', "Yeni bir araba almaları gerekiyor. Eski araba bozuldu."),
            ("I ____ like to visit Japan someday.", 'would', "Bir gün Japonya'yı ziyaret etmek isterdim."),
            ("You ____ study harder to pass the exam.", 'must', "Sınavı geçmek için daha sıkı çalışmalısınız."),
            ("We ____ stay at home because it's raining outside.", 'should', "Dışarıda yağmur yağıyor, evde kalmalıyız."),
            ("She ____ be studying for her final exams right now.", 'should', "Şu anda final sınavlarına çalışıyor olmalı."),
            ("You ____ speak louder. I can't hear you.", 'should', "Daha yüksek sesle konuşmalısınız. Seni duyamıyorum."),
            ("He ____ take the medicine three times a day.", 'must', "Günde üç kez ilacı almalı."),
            ("They ____ be coming to the party. They didn't respond.", 'might', "Partiye gelebilirler. Cevap vermediler."),
            ("She ____ be at work now. It's already 9 o'clock.", 'should', "Şu anda işte olmalı. Saat 9 oldu."),
            ("We ____ ask for permission before leaving the classroom.", 'must', "Sınıftan çıkmadan önce izin istemeliyiz."),
            ("You ____ drive carefully in snowy conditions.", 'should', "Karlı hava koşullarında dikkatli sürmelisiniz."),
            ("I ____ be able to attend the meeting tomorrow.", 'will', "Yarınki toplantıya katılabileceğim."),
            ("He ____ be at home. I saw his car parked outside.", 'must', "Eve gitmeli. Arabasını dışarıda park ettim."),
            ("You ____ help him. He's your friend.", 'should', "Ona yardım etmelisin. O senin arkadaşın."),
            ("We ____ leave early if we want to catch the train.", 'must', "Treni yakalamak istiyorsak erken çıkmalıyız.")
        ]
        
        self.current_example_index = 0
        self.correct_answers = 0
        self.total_answers = 0
        self.modal_verbs = ['can', 'could', 'may', 'might', 'must', 'shall', 'should', 'will', 'would', 'need to']
        self.create_widgets()

    def create_widgets(self):
        self.label_user_name = ttk.Label(self, text=f"Oyuncu: {self.user_name}", font=('Arial', 14), background='#D6EAF8')  
        self.label_user_name.pack(pady=10)

        title_label = ttk.Label(self, text="Modal Verbs Paneli", font=('Arial', 18), background='#D6EAF8') 
        title_label.pack(pady=10)

        self.label_sentence = ttk.Label(self, text="", font=('Arial', 12), wraplength=550, background='#D6EAF8')  
        self.label_sentence.pack(pady=10)

        self.options_var = tk.StringVar()
        self.radio_buttons = []
        for _ in range(3):
            rb = ttk.Radiobutton(self, text="", variable=self.options_var, value="")
            rb.pack(pady=2)
            self.radio_buttons.append(rb)

        self.btn_check = ttk.Button(self, text="Cevap ne?", command=self.check_answer)
        self.btn_check.pack(pady=5)

        self.btn_next = ttk.Button(self, text="Sonraki", command=self.show_next_example)
        self.btn_next.pack(pady=5)

        self.btn_score = ttk.Button(self, text="Sıralama", command=self.show_leaderboard)
        self.btn_score.pack(pady=5)

        self.btn_restart = ttk.Button(self, text="Yeniden Başla", command=self.restart)
        self.btn_restart.pack(pady=5)

        self.randomize_examples()
        self.show_next_example()

    def randomize_examples(self):
        random.shuffle(self.examples)

    def show_next_example(self):
        if self.current_example_index < len(self.examples):
            sentence, correct_answer, explanation = self.examples[self.current_example_index]
            self.label_sentence.config(text=sentence.replace("____", "_________"))
            self.options_var.set(None)

            options = set(random.sample(self.modal_verbs, 2))
            options.add(correct_answer)
            options = list(options)
            random.shuffle(options)
            
            for rb, option in zip(self.radio_buttons, options):
                rb.config(text=option, value=option)
            self.current_example_index += 1

            self.change_background_color()
        else:
            self.show_score()

    def check_answer(self):
        if self.current_example_index <= 0:
            return

        _, modal_verb, explanation = self.examples[self.current_example_index - 1]
        user_answer = self.options_var.get().strip().lower()
        self.total_answers += 1

        if user_answer == modal_verb.lower():
            self.correct_answers += 1
            messagebox.showinfo("Doğru", f"Doğru!\n{explanation}")
        else:
            messagebox.showerror("Yanlış", f"Yanlış!\n{explanation}")


    def show_score(self):
        score_message = f" {self.total_answers} sorudan {self.correct_answers} tanesini doğru bildin."
        messagebox.showinfo("Skor", score_message)

        # Save the score to a leaderboard file
        with open("leaderboard.txt", "a") as f:
            f.write(f"{self.user_name}: {self.correct_answers}/{self.total_answers}\n")

    def show_leaderboard(self):
        leaderboard = []
        with open("leaderboard.txt", "r") as f:
            leaderboard = f.readlines()

        leaderboard = [entry.strip() for entry in leaderboard]
        leaderboard.sort(key=lambda x: int(x.split(": ")[1].split("/")[0]), reverse=True)

        leaderboard_window = tk.Toplevel(self)
        leaderboard_window.title("Sıralama")
        leaderboard_window.geometry("400x300")

        leaderboard_frame = ttk.Frame(leaderboard_window)
        leaderboard_frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        columns = ("Oyuncu", "Skor")
        leaderboard_tree = ttk.Treeview(leaderboard_frame, columns=columns, show="headings")
        leaderboard_tree.heading("Oyuncu", text="Oyuncu")
        leaderboard_tree.heading("Skor", text="Skor")
        leaderboard_tree.pack(expand=True, fill=tk.BOTH)

        for entry in leaderboard:
            user, score = entry.split(": ")
            leaderboard_tree.insert("", tk.END, values=(user, score))

    def change_background_color(self):
        r = random.randint(0, 127) + 128  # 
        g = random.randint(0, 127) + 128
        b = random.randint(0, 127) + 128
        color = f'#{r:02x}{g:02x}{b:02x}'
        self.configure(background=color)

    def restart(self):
        self.destroy()
        app = NameEntryPanel()
        app.mainloop()

class NameEntryPanel(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Adınızı  giriniz.')
        self.geometry('400x200')
        self.configure(background='#D6EAF8')  
        self.create_widgets()

    def create_widgets(self):
        self.label_prompt = ttk.Label(self, text="Lütfen adınızı girin:", font=('Arial', 14), background='#D6EAF8')
        self.label_prompt.pack(pady=20)

        self.entry_name = ttk.Entry(self, font=('Arial', 14))
        self.entry_name.pack(pady=10)

        self.btn_submit = ttk.Button(self, text="Gönder", command=self.submit_name)
        self.btn_submit.pack(pady=10)

    def submit_name(self):
        user_name = self.entry_name.get().strip()
        if user_name:
            # Check if the user name already exists
            if not is_user_name_exists(user_name):
                self.destroy()
                app = ModalPanel(user_name)
                app.mainloop()
            else:
                messagebox.showerror("Hata", "Bu isim zaten kullanılmış. Lütfen farklı bir isim giriniz..")
        else:
            messagebox.showwarning("Giriş hatası", "İsim boş bırakılamaz. Lütfen adınızı giriniz.")

def is_user_name_exists(user_name):
    with open("leaderboard.txt", "r") as f:
        for line in f:
            if user_name in line:
                return True
    return False
def hide_terminal():
    window = win32gui.GetForegroundWindow()
    win32gui.ShowWindow(window, win32con.SW_HIDE)

if __name__ == "__main__":
    app = NameEntryPanel()
    hide_terminal()
    app.mainloop()

