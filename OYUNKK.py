from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle, Line
from kivy.clock import Clock


class GameBox(Widget):
    def __init__(self, app, **kwargs):
        super().__init__(**kwargs)
        self.app = app

        self.player_size = 40
        self.enemy_size = 40

        self.player_x = 50
        self.player_y = 50
        self.enemy_x = 200
        self.enemy_y = 200

        # hız değerleri (float → akıcı hareket)
        self.dx = 0
        self.dy = 0
        self.enemy_dx = 4
        self.enemy_dy = 4

        self.game_over = False

        with self.canvas:
            Color(1, 1, 1)
            self.border = Line(rectangle=(self.x, self.y, self.width, self.height), width=2)

            self.player_color = Color(1, 0, 0)
            self.player = Rectangle(pos=(self.player_x, self.player_y), size=(self.player_size, self.player_size))

            self.enemy_color = Color(0, 1, 0)
            self.enemy = Rectangle(pos=(self.enemy_x, self.enemy_y), size=(self.enemy_size, self.enemy_size))

        self.bind(pos=self.update_border, size=self.update_border)
        Clock.schedule_interval(self.update, 1 / 60)  # 60 FPS daha akıcı

    def update_border(self, *args):
        self.border.rectangle = (self.x, self.y, self.width, self.height)

    def move_left(self, *args): self.dx, self.dy = -5, 0
    def move_right(self, *args): self.dx, self.dy = 5, 0
    def move_up(self, *args): self.dx, self.dy = 0, 5
    def move_down(self, *args): self.dx, self.dy = 0, -5

    def update(self, dt):
        if self.game_over:
            return

        # Oyuncu hareketi
        self.player_x += self.dx
        self.player_y += self.dy

        # Oyuncu duvardan sekme
        if self.player_x <= self.x:
            self.player_x = self.x
            self.dx *= -1
        if self.player_x + self.player_size >= self.x + self.width:
            self.player_x = self.x + self.width - self.player_size
            self.dx *= -1
        if self.player_y <= self.y:
            self.player_y = self.y
            self.dy *= -1
        if self.player_y + self.player_size >= self.y + self.height:
            self.player_y = self.y + self.height - self.player_size
            self.dy *= -1

        self.player.pos = (self.player_x, self.player_y)

        # Düşman hareketi (düz sekme)
        self.enemy_x += self.enemy_dx
        self.enemy_y += self.enemy_dy

        if self.enemy_x <= self.x:
            self.enemy_x = self.x
            self.enemy_dx *= -1
        if self.enemy_x + self.enemy_size >= self.x + self.width:
            self.enemy_x = self.x + self.width - self.enemy_size
            self.enemy_dx *= -1
        if self.enemy_y <= self.y:
            self.enemy_y = self.y
            self.enemy_dy *= -1
        if self.enemy_y + self.enemy_size >= self.y + self.height:
            self.enemy_y = self.y + self.height - self.enemy_size
            self.enemy_dy *= -1

        self.enemy.pos = (self.enemy_x, self.enemy_y)

        # Çarpışma kontrolü
        if (self.player_x < self.enemy_x + self.enemy_size and
            self.player_x + self.player_size > self.enemy_x and
            self.player_y < self.enemy_y + self.enemy_size and
            self.player_y + self.player_size > self.enemy_y):
            self.game_over = True
            self.app.show_game_over()


class GameApp(App):
    def build(self):
        self.root_layout = BoxLayout(orientation="vertical")
        self.show_menu()
        return self.root_layout

    def show_menu(self, *args):
        self.root_layout.clear_widgets()

        title = Label(text="👾 Mini Hacker Oyunu 👾", font_size=32, color=(0, 1, 0, 1))
        btn_start = Button(text="▶️ Başla", font_size=24)
        btn_exit = Button(text="❌ Çıkış", font_size=24)

        btn_start.bind(on_press=self.start_game)
        btn_exit.bind(on_press=lambda x: self.stop())

        self.root_layout.add_widget(title)
        self.root_layout.add_widget(btn_start)
        self.root_layout.add_widget(btn_exit)

    def start_game(self, *args):
        self.root_layout.clear_widgets()

        layout = BoxLayout(orientation="vertical")

        self.game_box = GameBox(app=self, size_hint_y=0.8)
        layout.add_widget(self.game_box)

        controls = BoxLayout(size_hint_y=0.2)
        btn_left = Button(text="⬅️ Sol"); btn_left.bind(on_press=self.game_box.move_left)
        btn_right = Button(text="➡️ Sağ"); btn_right.bind(on_press=self.game_box.move_right)
        btn_up = Button(text="⬆️ Yukarı"); btn_up.bind(on_press=self.game_box.move_up)
        btn_down = Button(text="⬇️ Aşağı"); btn_down.bind(on_press=self.game_box.move_down)

        controls.add_widget(btn_left)
        controls.add_widget(btn_right)
        controls.add_widget(btn_up)
        controls.add_widget(btn_down)

        layout.add_widget(controls)
        self.root_layout.add_widget(layout)

    def show_game_over(self):
        self.root_layout.clear_widgets()
        self.root_layout.add_widget(Label(text="💀 HACKLENDİNİZ 💀", font_size=50, color=(0, 1, 0, 1)))

        btn_restart = Button(text="↩️ Menüye Dön", font_size=24)
        btn_restart.bind(on_press=self.show_menu)
        self.root_layout.add_widget(btn_restart)


if __name__ == "__main__":
    GameApp().run()