from PySide6.QtCore import QThreadPool, QTime, Qt
from PySide6.QtWidgets import QButtonGroup, QComboBox, QFileDialog, QGridLayout, QMessageBox, QRadioButton, QStackedLayout, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QSlider, QLineEdit
from PySide6.QtMultimedia import QAudioOutput, QMediaPlayer
from PySide6.QtMultimediaWidgets import QVideoWidget
from pymediainfo import MediaInfo
from video_helpers import CreateThumbnails
from superqt import QLabeledRangeSlider, QLabeledSlider, QRangeSlider
from PySide6.QtGui import QIntValidator

class LoginScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        #TODO: Add Later

class SignUpScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        #TODO: Add Later

class SelectFile(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        #TODO: add Later

class SnipScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)

    # Video Player
        self.video_player = QVideoWidget()
        self.video_player.setStyleSheet(
            "background-color: #1A1A1A; border: 1px solid #333333;"
        )
        layout.addWidget(self.video_player, stretch=6)

        self.snip_active = False
        self.frame_time = None

        self.player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.player.setAudioOutput(self.audio_output)
        self.player.setVideoOutput(self.video_player)
        
    # Control bar (play controls and such)
        self.control_container = QVBoxLayout()
        self.control_bar = QHBoxLayout()
        self.snip_times = QVBoxLayout()
        self.controls = QHBoxLayout()
        self.timestamp = QVBoxLayout()

        #Snip Times
        self.snip_start = QLineEdit()
        self.snip_start.setPlaceholderText("00:00:00.000")
        self.snip_start.setMaximumWidth(80)
        self.snip_start.setMinimumHeight(25)
        self.snip_start.setMaximumHeight(25)
        self.snip_times.addWidget(self.snip_start)

        self.snip_end = QLineEdit()
        self.snip_end.setPlaceholderText("99:59:59.999")
        self.snip_end.setMaximumWidth(80)
        self.snip_end.setMinimumHeight(25)
        self.snip_end.setMaximumHeight(25)
        self.snip_times.addWidget(self.snip_end)

        # Controls
        # Letters are place holders until images are added
        self.snip_button = QPushButton("S")
        self.snip_button.setFixedSize(25,25)
        self.snip_button.setCheckable(True)
        self.snip_button.setChecked(False)
        self.snip_button.clicked.connect(self.handle_snip_toggle)

        self.rewind_button = QPushButton("<")
        self.rewind_button.setFixedSize(25,25)
        self.rewind_button.clicked.connect(self.back_frame)

        self.play_button = QPushButton("P")
        self.play_button.setFixedSize(25,25)
        self.play_button.clicked.connect(self.toggle_play)
        self.play_button.setCheckable(True)

        self.forward_button = QPushButton(">")
        self.forward_button.setFixedSize(25,25)
        self.forward_button.clicked.connect(self.fwd_frame)

        self.repeat_button = QPushButton("R")
        self.repeat_button.setFixedSize(25,25)
        self.repeat_button.setCheckable(True)
        self.repeat_button.setChecked(False)

        self.controls.addWidget(self.snip_button)
        self.controls.addWidget(self.rewind_button)
        self.controls.addWidget(self.play_button)
        self.controls.addWidget(self.forward_button)
        self.controls.addWidget(self.repeat_button)

        # Timestamp
        self.timestamp_time = QLineEdit()
        self.timestamp_time.setPlaceholderText("55:55:55.555")
        self.timestamp_time.setMaximumWidth(80)
        self.timestamp.addWidget(self.timestamp_time)

        # Bring together Control bar
        self.control_bar.addLayout(self.snip_times)
        self.control_bar.addStretch()
        self.control_bar.addLayout(self.controls)
        self.control_bar.addStretch()
        self.control_bar.addLayout(self.timestamp)

        self.control_container.addLayout(self.control_bar)
        self.control_container.addStretch()

    # Audio Volume
        self.audio_container = QWidget()
        self.audio_layout = QVBoxLayout(self.audio_container)
        
        self.audio_label = QLabel()
        self.audio_label.setText("Audio: 100%")
        self.audio_label.setAlignment(Qt.AlignCenter)

        self.audio_slider = QSlider(Qt.Horizontal)
        self.audio_slider.setRange(0,100)
        self.audio_slider.setValue(100)

        # TODO: update values to allow up to 200%
        self.audio_slider.valueChanged.connect(
            lambda val: self.audio_output.setVolume(val/100.0))
        self.audio_slider.valueChanged.connect(
            lambda val: self.audio_label.setText(str(f"Audio: {val}%"))
        )
        self.audio_layout.addWidget(self.audio_label)
        self.audio_layout.addWidget(self.audio_slider)

        self.control_container.addWidget(self.audio_container)
        self.control_container.addStretch()

    # Playback Slider TODO: Make this alot better

        self.timeline_widget = QWidget()

        self.timeline_grid = QGridLayout(self.timeline_widget)
        self.timeline_grid.setContentsMargins(0,0,0,0)
        self.timeline_grid.setSpacing(0)
        self.final_start_bound = None
        self.final_end_bound = None

        self.thumbnail_container = QWidget()
        self.thumbnail_layout = QHBoxLayout(self.thumbnail_container)
        self.thumbnail_layout.setContentsMargins(0,0,0,0)
        self.thumbnail_layout.setSpacing(0)

        self.thumbnails = []

        for i in range(10):
            label = QLabel()

            label.setStyleSheet("background-color: #222222; border-right: 1px solid #111111;")
            label.setAlignment(Qt.AlignCenter)
            label.setFixedSize(80,45)
            self.thumbnail_layout.addWidget(label)
            self.thumbnails.append(label)

        self.timeline_grid.addWidget(self.thumbnail_container)


        self.playback_bar = QRangeSlider(Qt.Horizontal)
        self.playback_bar.setMaximumHeight(165)
        self.playback_bar.setRange(0,100)
        self.playback_bar.setValue((0,50,100))

        self.playback_bar.setStyleSheet("""
            QRangeSlider {
                    background: transparent;
                    height: 45px;
                }
                QRangeSlider::groove:horizontal {
                    background: transparent;
                    height: 45px;
                }
                QRangeSlider::sub-page:horizontal {
                    background: transparent;
                    height: 45px;
                }
                QRangeSlider::handle:horizontal {
                    background: #FFFFFF;
                    width: 4px;
                    height: 45px;
                    margin: 0px;
                }
        """)

        self.playback_bar.valueChanged.connect(self.handle_timeline_value_changes)

        self.timeline_grid.addWidget(self.playback_bar,0,0)
        self.playback_bar.raise_()


        self.control_container.addWidget(self.timeline_widget)

        layout.addLayout(self.control_container, stretch=4)

    def resizeEvent(self, event):
        """Ensures that the player is no more than 60% of the screen"""
        super().resizeEvent(event)
        max_height = int(self.height() * 0.60)
        self.video_player.setMaximumHeight(max_height)

    def toggle_play(self):
        """Toggles the video player"""
        if self.player.playbackState() == QMediaPlayer.PlayingState:
            self.player.pause()

        else:
            self.player.play()
    
    def back_frame(self):
        """Sends the video player back by one frame"""
        if not self.parent().media_path:
            return
        
        new_time = self.player.position() - self.frame_time
        self.player.setPosition(max(0,self.frame_time_helper(new_time))) 

    def fwd_frame(self):
        """Sends the video player forward by one frame"""
        
        if not self.parent().media_path:
            return
        
        
        new_time = self.player.position() + self.frame_time
        self.player.setPosition(min(self.frame_time_helper(new_time), self.player.duration()))

    def handle_duration_change(self, duration_ms):
        """Adds ranges and time"""
        self.playback_bar.setRange(0, duration_ms)
        self.playback_bar.setValue((0,1,duration_ms))

        self.final_start_bound = 0
        self.final_end_bound = duration_ms

        media_info = MediaInfo.parse(self.parent().media_path)
        track = next((t for t in media_info.tracks if t.track_type == "Video"),None)
        self.frame_rate = float(track.frame_rate)

        self.frame_time = 1000/self.frame_rate
        self.playback_bar.setSingleStep(round(self.frame_time))
        self.playback_bar.setPageStep(1000)


        self.snip_end.setText(self.format_time(duration_ms))
        self.snip_start.setText("00:00:00.000")
        self.timestamp_time.setText("00:00:00.000")

        for label in self.thumbnails:
            label.clear()
            label.setStyleSheet("background-color: #222222; border-right: 1px solid #111111;")

        self.active_thumbnail_worker = CreateThumbnails(self.parent().media_path, duration_ms)

        self.active_thumbnail_worker.signals.frame_ready.connect(self.update_thumbnails)

        QThreadPool.globalInstance().start(self.active_thumbnail_worker)

    def update_thumbnails(self, index, pixmap):
        if index < len(self.thumbnails):
            scaled_pixmap = pixmap.scaled(
                self.thumbnails[index].size(),
                Qt.KeepAspectRatioByExpanding,
                Qt.SmoothTransformation
            )
            self.thumbnails[index].setPixmap(scaled_pixmap)

    def handle_position_change(self, position_ms):
        """Updates the playback bar when its scrubbed in the ui"""
        current_val = self.playback_bar.value()

        if isinstance(current_val, (tuple,list)):
            vals = list(current_val)
        else:
            vals = [0,0, self.playback_bar.maximum()]

        if len(vals) == 3:
            if self.repeat_button.isChecked():
                if position_ms >= self.final_end_bound:
                    self.player.setPosition(self.final_start_bound)
                    position_ms = self.final_start_bound
                

            vals[1] = position_ms

            self.playback_bar.blockSignals(True)
            self.playback_bar.setValue(tuple(vals))
            self.playback_bar.blockSignals(False)

        self.timestamp_time.setText(self.format_time(position_ms))

    def set_player_position(self, playhead_ms):
        """Sets player position to a target ms"""
        if not self.parent().media_path or not self.frame_time:
            return
        math_corrected_target = self.frame_time_helper(playhead_ms)
        self.player.setPosition(math_corrected_target)
        return math_corrected_target
    
    def frame_time_helper(self, target_ms):
        """Snaps milliseconds to the nearest valid frame time boundary line"""
        return (round(round(target_ms / self.frame_time) * self.frame_time))

    def format_time(self, ms):
        """Helper Method To Format Time into hh:mm:ss.zzz"""
        time = QTime(0, 0, 0).addMSecs(ms)
        return time.toString("hh:mm:ss.zzz")

    def handle_snip_toggle(self):
        """Toggles snip mode view styling and enables/disables text boxes"""
        self.snip_active = not self.snip_active

        if self.snip_active: 
            self.playback_bar.setStyleSheet("""
                QRangeSlider {
                    background: transparent;
                    height: 45px;
                    qproperty-barColor: rgba(255, 215, 0, 0.25);
                }
                QRangeSlider::groove:horizontal {
                    background: transparent;
                    height: 45px;
                }
                QRangeSlider::handle:horizontal {
                    background: #FFD700;
                    width: 4px;
                    height: 45px;
                    margin: 0px;
                }
            """)

            self.snip_start.setStyleSheet("")
            self.snip_end.setStyleSheet("")
            self.snip_start.setEnabled(True)
            self.snip_end.setEnabled(True)
            
            vals = self.playback_bar.value()
            if len(vals) == 3:
                self.snip_start.setText(self.format_time(vals[0]))
                self.snip_end.setText(self.format_time(vals[2]))

        else: 
            self.playback_bar.setStyleSheet("""
                 QRangeSlider {
                    background: transparent;
                    height: 45px;
                    qproperty-barColor: transparent;
                }
                QRangeSlider::groove:horizontal {
                    background: transparent;
                    height: 45px;
                }
                QRangeSlider::handle:horizontal {
                    background: #FFFFFF;
                    width: 4px;
                    height: 45px;
                    margin: 0px;
                }
            """)
            self.snip_start.setStyleSheet("background: transparent; border: 2px solid transparent; color: transparent")
            self.snip_end.setStyleSheet("background: transparent; border: 2px solid transparent; color: transparent")
            self.snip_start.setEnabled(False)
            self.snip_end.setEnabled(False)

    def handle_timeline_value_changes(self, values_tuple):
        if not self.frame_time: return
        vals = list(values_tuple)
        if len(vals) == 3:
            start_ms = self.frame_time_helper(vals[0])
            playhead = self.frame_time_helper(vals[1])
            end_ms = self.frame_time_helper(vals[2])

            if not self.snip_active:
                if self.final_start_bound is None:
                    self.final_start_bound = 0
                if self.final_end_bound is None:
                    self.final_end_bound = self.playback_bar.maximum()

                start_ms = self.final_start_bound
                end_ms = self.final_end_bound

            self.playback_bar.blockSignals(True)
            self.playback_bar.setValue((start_ms, playhead, end_ms))
            self.playback_bar.blockSignals(False)

            self.set_player_position(playhead)
            self.timestamp_time.setText(self.format_time(playhead))
            self.snip_start.setText(self.format_time(start_ms))
            self.snip_end.setText(self.format_time(end_ms))
            
            if self.snip_active:
                self.snip_start.setText(self.format_time(start_ms))
                self.final_start_bound = start_ms
                self.snip_end.setText(self.format_time(end_ms))
                self.final_end_bound = end_ms

class SimpleSizeScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)

        self.selected_option = QButtonGroup(self)
    # top predicted Size
        self.size_info = QHBoxLayout()
        self.size_info_list = QVBoxLayout()
        #left half
        self.predicted_size_label = QLabel()
        self.predicted_size_label.setText("Predicted Size: ##.## MB")
        self.size_info.addWidget(self.predicted_size_label)

        #right half
        self.predicted_resolution = QLabel()
        self.predicted_resolution.setText("Resolution: ####x####")
        self.size_info_list.addWidget(self.predicted_resolution)

        self.predicted_fps = QLabel()
        self.predicted_fps.setText("Frame Rate: ##FPS")
        self.size_info_list.addWidget(self.predicted_fps)

        self.predicted_codec = QLabel()
        self.predicted_codec.setText("Codec: H.265")
        self.size_info_list.addWidget(self.predicted_codec)

        self.predicted_bitrate = QLabel()
        self.predicted_bitrate.setText("Bitrate: ## Mbps")
        self.size_info_list.addWidget(self.predicted_bitrate)

        self.size_info.addLayout(self.size_info_list)

        layout.addLayout(self.size_info)
        layout.addStretch()
    #Desired Bitrate
        self.desired_bitrate_layout = QVBoxLayout()


        self.center_radio1 = QHBoxLayout()
        self.center_radio1.addStretch()
        self.desired_bitrate_radio = QRadioButton()
        self.selected_option.addButton(self.desired_bitrate_radio)
        self.center_radio1.addWidget(self.desired_bitrate_radio)
        self.desired_bitrate_radio.setChecked(True)
        self.center_radio1.addStretch()
        self.desired_bitrate_layout.addLayout(self.center_radio1)

        self.desired_size_label = QLabel()
        self.desired_size_label.setAlignment(Qt.AlignCenter)
        self.desired_size_label.setText("Select Desired Bitrate:")
        self.desired_size_label.setStyleSheet("font-weight: bold; font-size: 30px;")
        self.desired_bitrate_layout.addWidget(self.desired_size_label)

        self.size_increment_hbox = QHBoxLayout()

        self.size_increment_label = QLabel()
        self.size_increment_label.setText("Size Increment: ")
        self.size_increment_hbox.addWidget(self.size_increment_label)

        self.size_increment_num = QLineEdit()
        self.size_increment_num.setValidator(QIntValidator(0,9999999,self))
        self.size_increment_num.setText("5")
        self.size_increment_hbox.addWidget(self.size_increment_num)

        self.size_increment_dropdown = QComboBox()
        self.size_increment_dropdown.addItems(["KB","MB"])
        self.size_increment_dropdown.setCurrentIndex(0)
        self.size_increment_hbox.addWidget(self.size_increment_dropdown)

        self.desired_bitrate_layout.addLayout(self.size_increment_hbox)

        self.size_increment_slider = QLabeledSlider(Qt.Horizontal)
        self.size_increment_slider.setRange(0, 100)
        self.size_increment_slider.setValue(5)
        self.size_increment_slider.setSingleStep(5)
        self.size_increment_slider.setPageStep(5)
        self.size_increment_slider.setTickPosition(QSlider.TicksAbove)
        self.size_increment_slider.setTickInterval(5)
        self.desired_bitrate_layout.addWidget(self.size_increment_slider)

        layout.addLayout(self.desired_bitrate_layout)
        layout.addStretch()

        #Big OR

        self.or_label = QLabel()
        self.or_label.setText("-----OR-----")
        self.or_label.setStyleSheet("font-weight: bold; font-size: 50px;")
        self.or_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.or_label)
        layout.addStretch()

        #Bottom Desired Size
        self.select_size_layout = QVBoxLayout()

        self.center_radio2 = QHBoxLayout()
        self.center_radio2.addStretch()
        self.desired_size_radio = QRadioButton()
        self.selected_option.addButton(self.desired_size_radio)
        self.center_radio2.addWidget(self.desired_size_radio)
        self.center_radio2.addStretch()
        self.select_size_layout.addLayout(self.center_radio2)

        self.desired_size_label2 = QLabel()
        self.desired_size_label2.setAlignment(Qt.AlignCenter)
        self.desired_size_label2.setStyleSheet("font-weight: bold; font-size: 30px;")
        self.desired_size_label2.setText("Select Desired Size:")
        self.select_size_layout.addWidget(self.desired_size_label2)

        self.size_select_hbox = QHBoxLayout()

        self.size_select_label = QLabel()
        self.size_select_label.setText("Desired Output Size: ")
        self.size_select_hbox.addWidget(self.size_select_label)

        self.size_select_num = QLineEdit()
        self.size_select_num.setValidator(QIntValidator(0,9999999,self))
        self.size_select_num.setText("5")
        self.size_select_hbox.addWidget(self.size_select_num)

        self.size_select_dropdown = QComboBox()
        self.size_select_dropdown.addItems(["KB","MB","GB"])
        self.size_select_dropdown.setCurrentIndex(0)
        self.size_select_hbox.addWidget(self.size_select_dropdown)

        self.select_size_layout.addLayout(self.size_select_hbox)
        layout.addLayout(self.select_size_layout)
        layout.addStretch()

        self.advanced_button = QPushButton()
        self.advanced_button.setText("Advanced")
        layout.addWidget(self.advanced_button)

class SaveScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)
        layout.addSpacing(50)

        self.header = QLabel()
        self.header.setText("Enter in File Name:")
        self.header.setStyleSheet("font-weight: bold; font-size: 30px;")
        self.header.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.header)
        layout.addSpacing(30)

        self.center_file_name = QHBoxLayout()
        self.center_file_name.addStretch()
        self.file_name = QLineEdit()
        self.file_name.setMaximumWidth(400)
        self.center_file_name.addWidget(self.file_name)
        self.center_file_name.addStretch()
        layout.addLayout(self.center_file_name)
        layout.addSpacing(100)

        self.buttons = QHBoxLayout()
        self.buttons.addStretch()

        self.quick_button = QPushButton("Quick\nExport")
        self.quick_button.setFixedSize(100,50)
        self.quick_button.clicked.connect(self.finished_popup)
        self.buttons.addWidget(self.quick_button)
        #TODO: Hookup File Browser
        
        self.buttons.addSpacing(50)

        self.export_button = QPushButton("Export\nTo...")
        self.export_button.setFixedSize(100,50)
        self.export_button.clicked.connect(self.open_file_dialog)
        self.buttons.addWidget(self.export_button)
        #TODO: Hookup File Browser
        self.buttons.addStretch()

        layout.addLayout(self.buttons)
        layout.addSpacing(100)

    def open_file_dialog(self):
        default_name = self.file_name.text() if self.file_name.text() else "untitled"
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save File",
            default_name,
            "Video Files (*.mp4, *.mkv, *.mov)"
        )

        if file_path:
            print(file_path)
            self.finished_popup()

    def finished_popup(self):
        message_box = QMessageBox(self)
        message_box.setWindowTitle("Export Complete!")
        message_box.setText("Your Video Has been Saved")

        new_project=message_box.addButton("Start New Project", QMessageBox.AcceptRole) # TODO: Hook this up to open new file load
        remain=message_box.addButton("Remain in project", QMessageBox.RejectRole)

        message_box.setDefaultButton(remain)

        message_box.exec()

        




class AdvancedSizeScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        #TODO: Add Later

class ErrorScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        #TODO: Add Later