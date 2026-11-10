import sys
from PySide6.QtCore import QUrl
from PySide6.QtWidgets import QApplication, QHBoxLayout, QMainWindow, QFileDialog, QPushButton, QStackedWidget, QVBoxLayout, QWidget
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from page_layouts import SnipScreen, SimpleSizeScreen, SaveScreen, LoginScreen, SignUpScreen, SelectFile


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SSS")
        self.resize(800, 550)
        self.media_path = None
        self.snip_screen = SnipScreen(self)
        self.login_screen = LoginScreen(self)
        self.signup_screen = SignUpScreen(self)
        self.simple_size_screen = SimpleSizeScreen(self)
        self.saves_screen = SaveScreen(self)
        self.file_select = SelectFile(self)

        self.master_stack = QStackedWidget()
        self.login_stack = QStackedWidget()
        self.main_workflow_stack = QStackedWidget()
        self.main_workflow = QWidget()
        
        main_workflow_layout = QVBoxLayout(self.main_workflow)
        main_workflow_layout.addWidget(self.main_workflow_stack, stretch=9)

        
        main_workflow_shelf = QHBoxLayout()
        self.button_snip = QPushButton("Snip")
        self.button_size = QPushButton("Size")
        self.button_save = QPushButton("Save")


        main_workflow_shelf.addWidget(self.button_snip)
        main_workflow_shelf.addWidget(self.button_size)
        main_workflow_shelf.addWidget(self.button_save)

        main_workflow_layout.addLayout(main_workflow_shelf, stretch=1)

        self.login_stack.addWidget(self.login_screen) # [0]
        self.login_stack.addWidget(self.signup_screen) # [1]
        self.login_stack.addWidget(self.file_select) # [2]

        self.main_workflow_stack.addWidget(self.snip_screen)
        self.main_workflow_stack.addWidget(self.simple_size_screen)
        self.main_workflow_stack.addWidget(self.saves_screen)

        self.button_snip.clicked.connect(lambda: self.main_workflow_stack.setCurrentIndex(0))
        self.button_size.clicked.connect(lambda: self.main_workflow_stack.setCurrentIndex(1))
        self.button_save.clicked.connect(lambda: self.main_workflow_stack.setCurrentIndex(2))

        
        

        self.master_stack.addWidget(self.login_stack) # [0]
        self.master_stack.addWidget(self.main_workflow) # [1]
        self.setCentralWidget(self.master_stack)

        self.login_stack.setCurrentIndex(0)
        self.main_workflow_stack.setCurrentIndex(0)

        
        #TODO: make a dummy widget
        #self.setCentralWidget(self.snip_screen)
        #self.setCentralWidget(self.simple_size_screen)
        #self.setCentralWidget(self.saves_screen)
        #self.setCentralWidget(self.login_screen)
        #self.setCentralWidget(self.signup_screen)
        #self.setCentralWidget(self.file_select)

    #Connections

        self.signup_screen.sign_up_button.clicked.connect(lambda: self.login_stack.setCurrentIndex(2))

        self.snip_screen.player.durationChanged.connect(self.snip_screen.handle_duration_change)
        self.snip_screen.player.positionChanged.connect(self.snip_screen.handle_position_change)

        self.bind_navigation_routes()
        self.create_menu()

    def bind_navigation_routes(self):
        # Flow A: Login branches
        self.login_screen.sign_in_button.clicked.connect(lambda: self.login_stack.setCurrentIndex(2)) # -> File Pick
        self.login_screen.sign_up_button.clicked.connect(lambda: self.login_stack.setCurrentIndex(1)) # -> Sign Up

        # Flow B: Sign Up branches
        # Assumes your signup layout has a completion button. Adjust the attribute name if different!
        if hasattr(self.signup_screen, 'register_button'):
            self.signup_screen.register_button.clicked.connect(lambda: self.login_stack.setCurrentIndex(2)) # -> File Pick
        # Fallback helper path back down to sign-in card context
        if hasattr(self.signup_screen, 'back_to_login_button'):
            self.signup_screen.back_to_login_button.clicked.connect(lambda: self.login_stack.setCurrentIndex(0))

    def create_menu(self):
        """Generates native system menu navigation entries"""
        menu_bar = self.menuBar()
        settings_menu = menu_bar.addMenu("&Settings")
        
        sign_out = settings_menu.addAction("&Sign Out")
        sign_out.triggered.connect(lambda: self.master_stack.setCurrentIndex(0))
        sign_out.triggered.connect(lambda: self.login_stack.setCurrentIndex(0))
        sign_out.triggered.connect(lambda: self.main_workflow_stack.setCurrentIndex(0))
        
        new_project = settings_menu.addAction("&New Project")
        new_project.triggered.connect(lambda: self.master_stack.setCurrentIndex(0))
        new_project.triggered.connect(lambda: self.login_stack.setCurrentIndex(3))
        sign_out.triggered.connect(lambda: self.main_workflow_stack.setCurrentIndex(0))

    


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())