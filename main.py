import builtins
from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.lang import Builder
from kivymd.uix import screen
from helpers import screens_handler
from colors import colors
from AddAccountScreen import AddAccountsScreen
from GeneralJournal import GeneralJournalScreen
from Leidgers import LeidgersScreen
from Balance_Sheet import BalanceSheetScreen
from IncomeStatement import IncomeStatementScreen
from Trail_Balance import TrailBalanceScreen
#source kivy_venv/bin/activate


sm = ScreenManager()
sm.add_widget(AddAccountsScreen(name='account'))
sm.add_widget(GeneralJournalScreen(name='general-journal'))
sm.add_widget(LeidgersScreen(name='leidgers'))
sm.add_widget(TrailBalanceScreen(name='trail-balance'))
sm.add_widget(IncomeStatementScreen(name='income-statement'))
sm.add_widget(BalanceSheetScreen(name='balance-sheet'))

class Accounting_Project(MDApp):
    def build(self):
        self.theme_cls.colors = colors
        self.theme_cls.primary_palette = "Red"
        self.theme_cls.accent_palette = "Teal"
        self.screen = Builder.load_string(screens_handler)
        return self.screen
    # Change screen
    def change_screen(self, screen: str):
        self.root.current = screen


if __name__ == "__main__":
    Accounting_Project().run()
