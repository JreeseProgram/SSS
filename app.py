import sys
from PySide6.QtCore import QUrl
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from page_layouts import SnipScreen, SimpleSizeScreen 

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SSS")
        self.resize(800, 550)

        #self.snip_screen = SnipScreen(self)
        self.simple_size_screen = SimpleSizeScreen()
        self.media_path = None
        #TODO: make a dummy widget
        #self.setCentralWidget(self.snip_screen)
        self.setCentralWidget(self.simple_size_screen)

        #self.snip_screen.player.durationChanged.connect(self.snip_screen.handle_duration_change)
        #self.snip_screen.player.positionChanged.connect(self.snip_screen.handle_position_change)


        # 3. Create a top system drop-down file menu
        self.create_menu()


    def create_menu(self):
        """Generates native system menu navigation entries"""
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("&File")
        
        open_action = file_menu.addAction("&Open Video...")
        open_action.triggered.connect(self.open_file_dialog)
        
        exit_action = file_menu.addAction("&Exit")
        exit_action.triggered.connect(self.close)

    def open_file_dialog(self):
        """Triggers local file browser dialog context"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Video Container", "", "Video Files (*.mp4 *.mov *.avi *.mkv)"
        )
        if file_path:
            self.media_path = file_path
            self.snip_screen.player.setSource(QUrl.fromLocalFile(file_path))
            self.snip_screen.player.pause() # Stage the initial clip frame onto our player surface


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
