import random
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle

class MenuScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=50, spacing=30)
        with layout.canvas.before:
            Color(0.02, 0.02, 0.08, 1)
            self.rect = Rectangle(size=(2000, 2000), pos=(0,0))
        title = Label(text="INFINITE UNIVERSE\nROCKET", font_size='36sp', bold=True, halign='center', color=(0, 0.8, 1, 1))
        play_btn = Button(text="GIOCA", font_size='28sp', bold=True, size_hint=(1, 0.3), background_color=(0, 0.5, 1, 1))
        play_btn.bind(on_press=self.vai_al_gioco)
        layout.add_widget(title)
        layout.add_widget(play_btn)
        self.add_widget(layout)
    def vai_al_gioco(self, instance):
        self.manager.current = 'game'
        self.manager.get_screen('game').avvia_partita()

class Razzo(Widget):
    pass

class Proiettile(Widget):
    def muovi(self, velocita):
        self.y += velocita

class Asteroide(Widget):
    def muovi(self, velocita):
        self.y -= velocita

class GameScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout_gioco = Widget()
        self.add_widget(self.layout_gioco)
        with self.layout_gioco.canvas.before:
            Color(0.01, 0.01, 0.05, 1)
            Rectangle(size=(2000, 2000))
        self.monete = 0
        self.punteggio = 0
        self.stats = {'PAC': 50, 'SHO': 50, 'PAS': 50, 'DRI': 50, 'DEF': 50, 'PHY': 50}
        self.label_info = Label(text="Goal: 0  |  Monete: 0", pos=(20, 1100), font_size='18sp', color=(1,1,1,1))
        self.layout_gioco.add_widget(self.label_info)
        self.razzo = Razzo(size=(60, 90))
        self.layout_gioco.add_widget(self.razzo)
        self.proiettili = []
        self.asteroidi = []
        self.btn_upgrade = Button(text="FIFA UPGRADES", size=(160, 50), pos=(10, 10))
        self.btn_upgrade.bind(on_press=self.apri_potenziamenti)
        self.layout_gioco.add_widget(self.btn_upgrade)

    def avvia_partita(self):
        self.razzo.pos = (self.width / 2 - 30, 100)
        Clock.schedule_interval(self.aggiorna_gioco, 1.0 / 60.0)
        Clock.schedule_interval(self.genera_asteroide, 1.2)
        Clock.schedule_interval(self.spara_proiettile, 0.4 - (self.stats['SHO'] * 0.002))

    def spara_proiettile(self, dt):
        with self.layout_gioco.canvas:
            Color(0, 1, 0.5, 1)
            p = Proiettile(size=(8, 20), pos=(self.razzo.center_x - 4, self.razzo.top))
            self.proiettili.append(p)

    def genera_asteroide(self, dt):
        with self.layout_gioco.canvas:
            Color(0.8, 0.2, 0.2, 1)
            pos_x = random.randint(10, max(50, int(self.width - 70)))
            a = Asteroide(size=(50, 50), pos=(pos_x, self.height))
            self.asteroidi.append(a)

    def aggiorna_gioco(self, dt):
        vel_tiro = 10 + (self.stats['SHO'] * 0.1)
        for p in self.proiettili[:]:
            p.muovi(vel_tiro)
            if p.y > self.height:
                self.layout_gioco.canvas.remove(p)
                self.proiettili.remove(p)
        vel_caduta = 4 + (self.punteggio * 0.1)
        for a in self.asteroidi[:]:
            a.muovi(vel_caduta)
            for p in self.proiettili[:]:
                if (a.x < p.x < a.x + 50) and (a.y < p.y < a.y + 50):
                    self.punteggio += 1
                    self.monete += 1
                    self.label_info.text = f"Goal: {self.punteggio}  |  Monete: {self.monete}"
                    try:
                        self.layout_gioco.canvas.remove(p)
                        self.proiettili.remove(p)
                    except: pass
                    try:
                        self.layout_gioco.canvas.remove(a)
                        self.asteroidi.remove(a)
                    except: pass
                    break

    def on_touch_move(self, touch):
        limite_vel = self.stats['DRI'] * 0.5
        if abs(touch.x - self.razzo.center_x) < limite_vel * 10:
            self.razzo.center_x = touch.x

    def apri_potenziamenti(self, instance):
        Clock.unschedule(self.aggiorna_gioco)
        Clock.unschedule(self.genera_asteroide)
        Clock.unschedule(self.spara_proiettile)
        upgrade_screen = self.manager.get_screen('upgrades')
        upgrade_screen.aggiorna_interfaccia(self)
        self.manager.current = 'upgrades'

class UpgradeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout_principale = BoxLayout(orientation='vertical', padding=20, spacing=10)
        with self.layout_principale.canvas.before:
            Color(0.15, 0.12, 0.05, 1)
            Rectangle(size=(2000, 2000))
        self.label_monete = Label(text="Monete Rimaste: 0", font_size='22sp', bold=True, color=(1, 0.8, 0, 1))
        self.layout_principale.add_widget(self.label_monete)
        self.lista_stats_layout = BoxLayout(orientation='vertical', spacing=5)
        self.layout_principale.add_widget(self.lista_stats_layout)
        btn_indietro = Button(text="TORNA ALLA BATTAGLIA", size_hint=(1, 0.15), background_color=(0, 0.7, 0.3, 1))
        btn_indietro.bind(on_press=self.ritorna_al_gioco)
        self.layout_principale.add_widget(btn_indietro)
        self.add_widget(self.layout_principale)

    def aggiorna_interfaccia(self, game_screen):
        self.game_screen = game_screen
        self.label_monete.text = f"Monete Ultimate Team: {self.game_screen.monete}"
        self.lista_stats_layout.clear_widgets()
        for stat, valore in self.game_screen.stats.items():
            box = BoxLayout(orientation='horizontal', spacing=10)
            lbl = Label(text=f"{stat}: {valore} OVR", font_size='18sp')
            btn = Button(text="Migliora (+5 OVR) [5 Monete]", size_hint_x=0.6)
            btn.bind(on_press=lambda instance, s=stat: self.compra_upgrade(s))
            box.add_widget(lbl)
            box.add_widget(btn)
            self.lista_stats_layout.add_widget(box)

    def compra_upgrade(self, stat):
        if self.game_screen.monete >= 5:
            self.game_screen.monete -= 5
            self.game_screen.stats[stat] += 5
            if self.game_screen.stats[stat] > 99:
                self.game_screen.stats[stat] = 99
            self.aggiorna_interfaccia(self.game_screen)

    def ritorna_al_gioco(self, instance):
        self.manager.current = 'game'
        self.game_screen.avvia_partita()

class UniversoInfinitoApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(GameScreen(name='game'))
        sm.add_widget(UpgradeScreen(name='upgrades'))
        return sm

if __name__ == '__main__':
    UniversoInfinitoApp().run()
