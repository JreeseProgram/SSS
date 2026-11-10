import sys
from PySide6.QtCore import QUrl
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from page_layouts import SnipScreen, SimpleSizeScreen, SaveScreen, LoginScreen, SignUpScreen, SelectFile

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SSS")
        self.resize(800, 550)

        #self.login_screen = LoginScreen()
        #self.signup_screen = SignUpScreen()
        #self.snip_screen = SnipScreen(self)
        #self.simple_size_screen = SimpleSizeScreen()
        #self.saves_screen = SaveScreen()
        self.file_select = SelectFile()

        self.media_path = None
        #TODO: make a dummy widget
        #self.setCentralWidget(self.snip_screen)
        #self.setCentralWidget(self.simple_size_screen)
        #self.setCentralWidget(self.saves_screen)
        #self.setCentralWidget(self.login_screen)
        #self.setCentralWidget(self.signup_screen)
        self.setCentralWidget(self.file_select)


        #self.snip_screen.player.durationChanged.connect(self.snip_screen.handle_duration_change)
        #self.snip_screen.player.positionChanged.connect(self.snip_screen.handle_position_change)


        # 3. Create a top system drop-down file menu
        self.create_menu()


    def create_menu(self):
        """Generates native system menu navigation entries"""
        menu_bar = self.menuBar()
        settings_menu = menu_bar.addMenu("&Settings")
        
        sign_out = settings_menu.addAction("&Sign Out")
        sign_out.triggered.connect(self.addlater)
        
        new_project = settings_menu.addAction("&New Project")
        new_project.triggered.connect(self.addalsolater)

    


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())