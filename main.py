from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.graphics import Color, RoundedRectangle
import random

BG      = (0.98, 0.95, 1,    1)
PINK    = (1,    0.45, 0.60, 1)
BLUE    = (0.25, 0.60, 1,    1)
GREEN   = (0.20, 0.78, 0.45, 1)
ORANGE  = (1,    0.65, 0.10, 1)
PURPLE  = (0.65, 0.35, 1,    1)
YELLOW  = (1,    0.88, 0.10, 1)
RED     = (1,    0.25, 0.25, 1)
TEAL    = (0.10, 0.80, 0.80, 1)
WHITE   = (1,    1,    1,    1)
DARK    = (0.15, 0.10, 0.25, 1)
RAINBOW = [PINK, BLUE, GREEN, ORANGE, PURPLE, YELLOW, RED, TEAL]

def make_bg(widget, color):
    with widget.canvas.before:
        Color(*color)
        rect = RoundedRectangle(pos=widget.pos, size=widget.size, radius=[18])
    widget.bind(pos=lambda w, v: setattr(rect, 'pos', v),
                size=lambda w, v: setattr(rect, 'size', v))

class ScoreTracker:
    numbers_seen = 0
    letters_seen = 0
    total_stars  = 0
    quiz_score   = 0
    quiz_total   = 0

score = ScoreTracker()

# ── HOME SCREEN ───────────────────────────────────────────
class HomeScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.layout = BoxLayout(orientation='vertical', padding=40, spacing=20)
        make_bg(self.layout, BG)

        self.layout.add_widget(Label(
            text="👶 Kids Learn! 🌟",
            font_size='52sp', bold=True,
            color=PURPLE, size_hint=(1, 0.20)
        ))

        self.stars_label = Label(
            text="⭐ Stars: 0",
            font_size='30sp', bold=True,
            color=ORANGE, size_hint=(1, 0.10)
        )
        self.layout.add_widget(self.stars_label)

        self.progress_label = Label(
            text="🔢 Numbers: 0/20   🔤 Letters: 0/26",
            font_size='20sp',
            color=DARK, size_hint=(1, 0.08)
        )
        self.layout.add_widget(self.progress_label)

        self.quiz_label = Label(
            text="🧠 Quiz Score: 0 / 0",
            font_size='22sp', bold=True,
            color=TEAL, size_hint=(1, 0.08)
        )
        self.layout.add_widget(self.quiz_label)

        btn_count = Button(
            text="🔢  Numbers  1 – 20",
            font_size='30sp', bold=True,
            background_color=(0,0,0,0),
            color=WHITE, size_hint=(1, 0.16)
        )
        make_bg(btn_count, BLUE)
        btn_count.bind(on_press=lambda x: setattr(self.manager, 'current', 'numbers'))

        btn_abc = Button(
            text="🔤  Letters  A – Z",
            font_size='30sp', bold=True,
            background_color=(0,0,0,0),
            color=WHITE, size_hint=(1, 0.16)
        )
        make_bg(btn_abc, PINK)
        btn_abc.bind(on_press=lambda x: setattr(self.manager, 'current', 'letters'))

        btn_quiz = Button(
            text="🧠  ABC Quiz!",
            font_size='30sp', bold=True,
            background_color=(0,0,0,0),
            color=WHITE, size_hint=(1, 0.16)
        )
        make_bg(btn_quiz, TEAL)
        btn_quiz.bind(on_press=lambda x: setattr(self.manager, 'current', 'quiz'))

        self.layout.add_widget(btn_count)
        self.layout.add_widget(btn_abc)
        self.layout.add_widget(btn_quiz)
        self.add_widget(self.layout)

    def on_enter(self):
        self.stars_label.text   = f"⭐ Stars: {score.total_stars}"
        self.progress_label.text = (
            f"🔢 Numbers: {score.numbers_seen}/20   "
            f"🔤 Letters: {score.letters_seen}/26"
        )
        self.quiz_label.text = f"🧠 Quiz Score: {score.quiz_score} / {score.quiz_total}"

# ── NUMBERS SCREEN ────────────────────────────────────────
class NumbersScreen(Screen):
    WORDS = ["","ONE","TWO","THREE","FOUR","FIVE","SIX","SEVEN",
             "EIGHT","NINE","TEN","ELEVEN","TWELVE","THIRTEEN",
             "FOURTEEN","FIFTEEN","SIXTEEN","SEVENTEEN","EIGHTEEN",
             "NINETEEN","TWENTY"]

    def __init__(self, **kw):
        super().__init__(**kw)
        self.current_num = 1
        self.layout = BoxLayout(orientation='vertical', padding=30, spacing=15)
        make_bg(self.layout, BG)

        self.layout.add_widget(Label(
            text="🔢 Let's Count!",
            font_size='40sp', bold=True,
            color=BLUE, size_hint=(1, 0.10)
        ))

        self.progress = Label(
            text="Progress: 1 / 20 ⭐",
            font_size='24sp',
            color=PURPLE, size_hint=(1, 0.08)
        )
        self.layout.add_widget(self.progress)

        self.stars_row = Label(text="⭐", font_size='24sp', size_hint=(1, 0.08))
        self.layout.add_widget(self.stars_row)

        self.num_label = Label(
            text="1", font_size='140sp', bold=True,
            color=PURPLE, size_hint=(1, 0.35)
        )
        self.layout.add_widget(self.num_label)

        self.word_label = Label(
            text="ONE", font_size='44sp', bold=True,
            color=ORANGE, size_hint=(1, 0.10)
        )
        self.layout.add_widget(self.word_label)

        nav = BoxLayout(orientation='horizontal', spacing=20, size_hint=(1, 0.16))
        btn_prev = Button(text="◀  Back", font_size='30sp', bold=True, background_color=(0,0,0,0), color=WHITE)
        make_bg(btn_prev, ORANGE)
        btn_prev.bind(on_press=self.prev_num)
        btn_next = Button(text="Next  ▶", font_size='30sp', bold=True, background_color=(0,0,0,0), color=WHITE)
        make_bg(btn_next, GREEN)
        btn_next.bind(on_press=self.next_num)
        nav.add_widget(btn_prev)
        nav.add_widget(btn_next)
        self.layout.add_widget(nav)

        btn_home = Button(text="🏠 Home", font_size='26sp', background_color=(0,0,0,0), color=WHITE, size_hint=(1, 0.10))
        make_bg(btn_home, PINK)
        btn_home.bind(on_press=lambda x: setattr(self.manager, 'current', 'home'))
        self.layout.add_widget(btn_home)
        self.add_widget(self.layout)

    def update(self):
        self.num_label.text  = str(self.current_num)
        self.word_label.text = self.WORDS[self.current_num]
        self.num_label.color = RAINBOW[(self.current_num - 1) % len(RAINBOW)]
        self.progress.text   = f"Progress: {self.current_num} / 20 ⭐"
        self.stars_row.text  = "⭐" * min(self.current_num, 20)
        if self.current_num > score.numbers_seen:
            score.numbers_seen = self.current_num
            score.total_stars += 1

    def next_num(self, *a):
        if self.current_num < 20:
            self.current_num += 1
            self.update()

    def prev_num(self, *a):
        if self.current_num > 1:
            self.current_num -= 1
            self.update()

# ── LETTERS SCREEN ────────────────────────────────────────
class LettersScreen(Screen):
    WORDS  = ["Apple","Bear","Cat","Dog","Elephant","Frog","Grapes",
              "House","Ice cream","Jelly","King","Lion","Moon","Nest",
              "Octopus","Penguin","Queen","Rainbow","Star","Taco",
              "Umbrella","Violin","Wave","X-ray","Yoyo","Zap"]
    EMOJIS = ["🍎","🐻","🐱","🐶","🐘","🐸","🍇","🏠","🍦","🃏",
              "👑","🦁","🌙","🐢","🐙","🐧","👑","🌈","⭐","🌮",
              "☂️","🎻","🌊","❌","🪀","⚡"]

    def __init__(self, **kw):
        super().__init__(**kw)
        self.current_idx = 0
        self.letters = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        self.layout = BoxLayout(orientation='vertical', padding=30, spacing=15)
        make_bg(self.layout, BG)

        self.layout.add_widget(Label(
            text="🔤 Let's Learn ABC!",
            font_size='40sp', bold=True,
            color=PINK, size_hint=(1, 0.10)
        ))

        self.progress = Label(
            text="Progress: A (1 / 26) ⭐",
            font_size='24sp', color=PURPLE, size_hint=(1, 0.08)
        )
        self.layout.add_widget(self.progress)

        self.stars_row = Label(text="⭐", font_size='22sp', size_hint=(1, 0.08))
        self.layout.add_widget(self.stars_row)

        self.letter_label = Label(
            text="A", font_size='150sp', bold=True,
            color=BLUE, size_hint=(1, 0.32)
        )
        self.layout.add_widget(self.letter_label)

        self.emoji_label = Label(
            text="🍎  is for  Apple",
            font_size='34sp', color=DARK, size_hint=(1, 0.10)
        )
        self.layout.add_widget(self.emoji_label)

        nav = BoxLayout(orientation='horizontal', spacing=20, size_hint=(1, 0.16))
        btn_prev = Button(text="◀  Back", font_size='30sp', bold=True, background_color=(0,0,0,0), color=WHITE)
        make_bg(btn_prev, ORANGE)
        btn_prev.bind(on_press=self.prev_letter)
        btn_next = Button(text="Next  ▶", font_size='30sp', bold=True, background_color=(0,0,0,0), color=WHITE)
        make_bg(btn_next, GREEN)
        btn_next.bind(on_press=self.next_letter)
        nav.add_widget(btn_prev)
        nav.add_widget(btn_next)
        self.layout.add_widget(nav)

        btn_home = Button(text="🏠 Home", font_size='26sp', background_color=(0,0,0,0), color=WHITE, size_hint=(1, 0.10))
        make_bg(btn_home, PURPLE)
        btn_home.bind(on_press=lambda x: setattr(self.manager, 'current', 'home'))
        self.layout.add_widget(btn_home)
        self.add_widget(self.layout)

    def update(self):
        i = self.current_idx
        self.letter_label.text  = self.letters[i]
        self.emoji_label.text   = f"{self.EMOJIS[i]}  is for  {self.WORDS[i]}"
        self.letter_label.color = RAINBOW[i % len(RAINBOW)]
        self.progress.text      = f"Progress: {self.letters[i]} ({i+1} / 26) ⭐"
        self.stars_row.text     = "⭐" * min(i + 1, 26)
        if i + 1 > score.letters_seen:
            score.letters_seen = i + 1
            score.total_stars += 1

    def next_letter(self, *a):
        if self.current_idx < 25:
            self.current_idx += 1
            self.update()

    def prev_letter(self, *a):
        if self.current_idx > 0:
            self.current_idx -= 1
            self.update()

# ── QUIZ SCREEN ───────────────────────────────────────────
class QuizScreen(Screen):
    WORDS  = ["Apple","Bear","Cat","Dog","Elephant","Frog","Grapes",
              "House","Ice cream","Jelly","King","Lion","Moon","Nest",
              "Octopus","Penguin","Queen","Rainbow","Star","Taco",
              "Umbrella","Violin","Wave","X-ray","Yoyo","Zap"]
    EMOJIS = ["🍎","🐻","🐱","🐶","🐘","🐸","🍇","🏠","🍦","🃏",
              "👑","🦁","🌙","🐢","🐙","🐧","👑","🌈","⭐","🌮",
              "☂️","🎻","🌊","❌","🪀","⚡"]
    LETTERS = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

    def __init__(self, **kw):
        super().__init__(**kw)
        self.correct_answer = ""
        self.layout = BoxLayout(orientation='vertical', padding=30, spacing=15)
        make_bg(self.layout, BG)

        self.layout.add_widget(Label(
            text="🧠 ABC Quiz!",
            font_size='44sp', bold=True,
            color=TEAL, size_hint=(1, 0.10)
        ))

        self.score_label = Label(
            text="Score: 0 / 0 ⭐",
            font_size='26sp', bold=True,
            color=ORANGE, size_hint=(1, 0.08)
        )
        self.layout.add_widget(self.score_label)

        self.emoji_label = Label(
            text="🍎",
            font_size='100sp',
            size_hint=(1, 0.28)
        )
        self.layout.add_widget(self.emoji_label)

        self.question_label = Label(
            text="Which letter does Apple start with?",
            font_size='26sp', bold=True,
            color=DARK, size_hint=(1, 0.10)
        )
        self.layout.add_widget(self.question_label)

        self.feedback = Label(
            text="",
            font_size='32sp', bold=True,
            size_hint=(1, 0.08)
        )
        self.layout.add_widget(self.feedback)

        # 4 answer buttons in a grid
        self.btn_grid = GridLayout(cols=2, spacing=15, size_hint=(1, 0.28))
        self.answer_btns = []
        btn_colors = [BLUE, PINK, GREEN, PURPLE]
        for i in range(4):
            btn = Button(
                text="A",
                font_size='40sp', bold=True,
                background_color=(0,0,0,0),
                color=WHITE
            )
            make_bg(btn, btn_colors[i])
            btn.bind(on_press=self.check_answer)
            self.answer_btns.append(btn)
            self.btn_grid.add_widget(btn)
        self.layout.add_widget(self.btn_grid)

        btn_home = Button(
            text="🏠 Home", font_size='24sp',
            background_color=(0,0,0,0),
            color=WHITE, size_hint=(1, 0.08)
        )
        make_bg(btn_home, ORANGE)
        btn_home.bind(on_press=lambda x: setattr(self.manager, 'current', 'home'))
        self.layout.add_widget(btn_home)

        self.add_widget(self.layout)

    def on_enter(self):
        self.new_question()

    def new_question(self):
        self.feedback.text = ""
        idx = random.randint(0, 25)
        self.correct_answer = self.LETTERS[idx]
        self.emoji_label.text = self.EMOJIS[idx]
        self.question_label.text = f"Which letter does {self.WORDS[idx]} start with?"

        # pick 3 wrong answers
        wrong = random.sample([l for l in self.LETTERS if l != self.correct_answer], 3)
        options = wrong + [self.correct_answer]
        random.shuffle(options)

        for i, btn in enumerate(self.answer_btns):
            btn.text = options[i]

    def check_answer(self, instance):
        score.quiz_total += 1
        if instance.text == self.correct_answer:
            self.feedback.text  = "🎉 Correct! Well done!"
            self.feedback.color = GREEN
            score.quiz_score   += 1
            score.total_stars  += 1
        else:
            self.feedback.text  = f"❌ It was  {self.correct_answer}!"
            self.feedback.color = RED
        self.score_label.text = f"Score: {score.quiz_score} / {score.quiz_total} ⭐"
        # next question after short delay
        from kivy.clock import Clock
        Clock.schedule_once(lambda dt: self.new_question(), 1.5)

# ── APP ───────────────────────────────────────────────────
class KidsLearnApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(HomeScreen(name='home'))
        sm.add_widget(NumbersScreen(name='numbers'))
        sm.add_widget(LettersScreen(name='letters'))
        sm.add_widget(QuizScreen(name='quiz'))
        return sm

if __name__ == "__main__":
    KidsLearnApp().run()