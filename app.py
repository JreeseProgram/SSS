import sys
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QPushButton, QLabel, QStackedWidget
)

class MultiPageApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Multi-Page Video Suite")
        self.resize(800, 500)

        # 1. Master Layout Setup
        # Like before, we need a central widget and a layout to split the screen left-to-right
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.split_layout = QHBoxLayout(self.central_widget)
        self.split_layout.setContentsMargins(0, 0, 0, 0) # Edge-to-edge look
        self.split_layout.setSpacing(0)

        # ==========================================
        # LEFT PANEL: Navigation Sidebar
        # ==========================================
        self.sidebar_frame = QWidget()
        self.sidebar_frame.setFixedWidth(180)
        self.sidebar_frame.setStyleSheet("background-color: #202020;")
        
        self.sidebar_layout = QVBoxLayout(self.sidebar_frame)
        self.sidebar_layout.setContentsMargins(10, 20, 10, 20)
        self.sidebar_layout.setSpacing(10)

        # Create the navigation buttons
        self.nav_home_btn = QPushButton("🏠 Home Dash")
        self.nav_trim_btn = QPushButton("🎥 Video Trimmer")
        self.nav_settings_btn = QPushButton("⚙️ Settings")

        # Style the buttons to look clean in the dark sidebar
        btn_style = "QPushButton { color: white; padding: 10px; text-align: left; background: transparent; border: none; font-size: 13px; } QPushButton:hover { background-color: #333333; border-radius: 4px; }"
        for btn in [self.nav_home_btn, self.nav_trim_btn, self.nav_settings_btn]:
            btn.setStyleSheet(btn_style)

        # Add buttons to the sidebar
        self.sidebar_layout.addWidget(self.nav_home_btn)
        self.sidebar_layout.addWidget(self.nav_trim_btn)
        self.sidebar_layout.addWidget(self.nav_settings_btn)
        self.sidebar_layout.addStretch() # Push everything to the top

        # Mount the sidebar into our master split screen
        self.split_layout.addWidget(self.sidebar_frame)

        # ==========================================
        # RIGHT PANEL: The Page Deck (QStackedWidget)
        # ==========================================
        # This is the magic container that acts as our page switcher
        self.page_deck = QStackedWidget()
        self.split_layout.addWidget(self.page_deck)

        # Create our 3 distinct page layout views
        self.create_home_page()
        self.create_trimmer_page()
        self.create_settings_page()

        # Connect the sidebar button click triggers to switch pages
        # .setCurrentIndex() tells the deck which page to bring to the front
        self.nav_home_btn.clicked.connect(lambda: self.page_deck.setCurrentIndex(0))
        self.nav_trim_btn.clicked.connect(lambda: self.page_deck.setCurrentIndex(1))
        self.nav_settings_btn.clicked.connect(lambda: self.page_deck.setCurrentIndex(2))

    # ==========================================
    # PAGE DEFINITIONS (Views)
    # ==========================================

    def create_home_page(self):
        """Page Index 0: The landing dashboard"""
        page = QWidget()
        layout = QVBoxLayout(page)
        
        title = QLabel("Welcome to Video Suite")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        title.setAlignment(Qt.AlignCenter)
        
        layout.addWidget(title)
        
        # Add this page container to our master deck
        self.page_deck.addWidget(page)

    def create_trimmer_page(self):
        """Page Index 1: The video trimming workspace"""
        page = QWidget()
        layout = QVBoxLayout(page)
        
        title = QLabel("Video Trimming Workspace")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        
        # This is where your previous video canvas, slider, and inputs would be packed
        mock_canvas = QWidget()
        mock_canvas.setStyleSheet("background-color: #111111; border: 1px solid #333333;")
        
        layout.addWidget(title)
        layout.addWidget(mock_canvas, stretch=1)
        
        # Add this page container to our master deck
        self.page_deck.addWidget(page)

    def create_settings_page(self):
        """Page Index 2: App settings configurations"""
        page = QWidget()
        layout = QVBoxLayout(page)
        
        title = QLabel("Application Settings")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        
        layout.addWidget(title)
        layout.addStretch()
        
        # Add this page container to our master deck
        self.page_deck.addWidget(page)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MultiPageApp()
    window.show()
    sys.exit(app.exec())
