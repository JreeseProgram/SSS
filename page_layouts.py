from typing import Literal

from PySide6.QtCore import QThreadPool, QTime, QUrl, Qt
from PySide6.QtWidgets import QButtonGroup, QCheckBox, QComboBox, QFileDialog, QGridLayout, QMessageBox, QRadioButton, QStackedLayout, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QSlider, QLineEdit
from PySide6.QtMultimedia import QAudioOutput, QMediaPlayer
from PySide6.QtMultimediaWidgets import QVideoWidget
from pymediainfo import MediaInfo
from video_helpers import CreateThumbnails
from superqt import QLabeledRangeSlider, QLabeledSlider, QRangeSlider
from PySide6.QtGui import QIntValidator

class LoginScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)
        layout.addStretch()

        self.sign_in_label = QLabel()
        self.sign_in_label.setAlignment(Qt.AlignCenter)
        self.sign_in_label.setText("Sign In")
        self.sign_in_label.setStyleSheet("font-weight: bold; font-size: 30px;")
        layout.addWidget(self.sign_in_label)
        layout.addSpacing(30)

        self.center_username = QHBoxLayout()
        self.center_username.addStretch()
        self.username_field = QLineEdit()
        self.username_field.setPlaceholderText("Username")
        self.username_field.setMinimumWidth(250)
        self.center_username.addWidget(self.username_field)
        self.center_username.addStretch()
        

        layout.addLayout(self.center_username)
        layout.addSpacing(25)

        self.center_password = QHBoxLayout()
        self.center_password.addStretch()
        self.password_field = QLineEdit()
        self.password_field.setPlaceholderText("Password")
        self.password_field.setMinimumWidth(250)
        self.center_password.addWidget(self.password_field)
        self.center_password.addStretch()

        layout.addLayout(self.center_password)
        layout.addSpacing(100)

        self.center_sign_button = QHBoxLayout()
        self.center_sign_button.addStretch()
        self.sign_in_button = QPushButton("Sign In")
        self.center_sign_button.addWidget(self.sign_in_button)
        self.center_sign_button.addStretch()

        layout.addLayout(self.center_sign_button)
        layout.addSpacing(10)

        self.sign_up_label = QLabel()
        self.sign_up_label.setAlignment(Qt.AlignCenter)
        self.sign_up_label.setText("Not a User?")
        self.sign_up_label.setStyleSheet("font-weight: bold; font-size: 30px;")
        layout.addWidget(self.sign_up_label)
        layout.addSpacing(50)

        self.center_sign_up = QHBoxLayout()
        self.center_sign_up.addStretch()
        self.sign_up_button = QPushButton("Sign Up Here")
        self.center_sign_up.addWidget(self.sign_up_button)
        self.center_sign_up.addStretch()
        layout.addLayout(self.center_sign_up)
        layout.addStretch()

class SignUpScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        layout = QVBoxLayout(self)
        layout.addSpacing(70)

        self.sign_up_label = QLabel()
        self.sign_up_label.setAlignment(Qt.AlignCenter)
        self.sign_up_label.setText("Sign Up")
        self.sign_up_label.setStyleSheet("font-weight: bold; font-size: 30px;")
        layout.addWidget(self.sign_up_label)
        layout.addSpacing(30)

        self.center_email = QHBoxLayout()
        self.center_email.addStretch()
        self.email_field = QLineEdit()
        self.email_field.setPlaceholderText("Email")
        self.email_field.setMinimumWidth(250)
        self.center_email.addWidget(self.email_field)
        self.center_email.addStretch()
        layout.addLayout(self.center_email)
        layout.addSpacing(25)

        self.center_username = QHBoxLayout()
        self.center_username.addStretch()
        self.username_field = QLineEdit()
        self.username_field.setPlaceholderText("Username")
        self.username_field.setMinimumWidth(250)
        self.center_username.addWidget(self.username_field)
        self.center_username.addStretch()
        

        layout.addLayout(self.center_username)
        layout.addSpacing(25)

        self.center_password = QHBoxLayout()
        self.center_password.addStretch()
        self.password_field = QLineEdit()
        self.password_field.setPlaceholderText("Password")
        self.password_field.setMinimumWidth(250)
        self.center_password.addWidget(self.password_field)
        self.center_password.addStretch()

        layout.addLayout(self.center_password)
        layout.addSpacing(100)

        self.t_and_c = QHBoxLayout()
        self.t_and_c.addStretch()
        self.box = QCheckBox()
        self.t_and_c.addWidget(self.box)

        self.agree = QLabel()
        self.agree.setText("I Agree to the Terms and Conditions")
        self.t_and_c.addWidget(self.agree)
        self.t_and_c.addStretch()
        layout.addLayout(self.t_and_c)


        self.center_sign_up = QHBoxLayout()
        self.center_sign_up.addStretch()
        self.sign_up_button = QPushButton("Sign Up")
        self.center_sign_up.addWidget(self.sign_up_button)
        self.center_sign_up.addStretch()
        layout.addLayout(self.center_sign_up)
        layout.addStretch()

class SelectFile(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        #TODO: Add more robust error handling
        layout = QVBoxLayout(self)

        layout.addStretch()
        self.button_center = QHBoxLayout()
        self.button_center.addStretch()
        self.button = QPushButton("Select Your File")
        self.button.clicked.connect(self.open_file_dialog)
        self.button_center.addWidget(self.button)
        self.button_center.addStretch()

        layout.addLayout(self.button_center)
        layout.addStretch()

    def open_file_dialog(self):

            main_window = self.window()
            file_path, _ = QFileDialog.getOpenFileName(
                self, "Select Video Container", "", "Video Files (*.mp4 *.mov *.avi *.mkv)"
            )
            if file_path:
                main_window.media_path = file_path
                main_window.snip_screen.player.setSource(QUrl.fromLocalFile(file_path))
                main_window.snip_screen.player.pause() 
                
                main_window.master_stack.setCurrentIndex(1)

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
        self.snip_start.setEnabled(False)

        self.snip_end = QLineEdit()
        self.snip_end.setPlaceholderText("99:59:59.999")
        self.snip_end.setMaximumWidth(80)
        self.snip_end.setMinimumHeight(25)
        self.snip_end.setMaximumHeight(25)
        self.snip_times.addWidget(self.snip_end)
        self.snip_end.setEnabled(False)

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
            label.setMinimumSize(10,45)
            label.setFixedHeight(45)
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

        self.snip_start.editingFinished.connect(lambda: self.handle_timestamp_manipulation(self.snip_start, "start"))
        self.timestamp_time.editingFinished.connect(lambda: self.handle_timestamp_manipulation(self.timestamp_time, "playhead"))
        self.snip_end.editingFinished.connect(lambda: self.handle_timestamp_manipulation(self.snip_end, "end"))

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

        main_window = self.window()
        if not main_window.media_path:
            return
        
        new_time = self.player.position() - self.frame_time
        self.player.setPosition(max(0,self.frame_time_helper(new_time))) 

    def fwd_frame(self):
        """Sends the video player forward by one frame"""
        main_window = self.window()
        if not main_window.media_path:
            return
        
        
        new_time = self.player.position() + self.frame_time
        self.player.setPosition(min(self.frame_time_helper(new_time), self.player.duration()))

    def handle_duration_change(self, duration_ms):
        """Adds ranges and time"""
        main_window = self.window()
        self.playback_bar.setRange(0, duration_ms)
        self.playback_bar.setValue((0,1,duration_ms))

        self.final_start_bound = 0
        self.final_end_bound = duration_ms

        media_info = MediaInfo.parse(main_window.media_path)
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
        
        main_window = self.window()

        self.active_thumbnail_worker = CreateThumbnails(main_window.media_path, duration_ms)

        self.active_thumbnail_worker.signals.frame_ready.connect(self.update_thumbnails)

        QThreadPool.globalInstance().start(self.active_thumbnail_worker)

    def handle_timestamp_manipulation(self, field_obj:QLineEdit, current_field: Literal["start","playhead","end"]):
        current_text = field_obj.text().strip()

        time = QTime.fromString(current_text, "hh:mm:ss.zzz")
        duration = self.player.duration()

        if time.isValid():
            ms = QTime(0,0,0).msecsTo(time)

            if 0 <= ms <= duration:
                corrected_ms = self.frame_time_helper(ms)
                time_tuple = list(self.playback_bar.value())
                if current_field == "start" and corrected_ms < self.final_end_bound:
                    time_tuple[0] = corrected_ms
                    self.handle_timeline_value_changes(tuple(time_tuple))
                    return
                elif current_field == "playhead" and corrected_ms <= self.final_end_bound and corrected_ms >= self.final_start_bound:
                    time_tuple[1] = corrected_ms
                    self.handle_timeline_value_changes(tuple(time_tuple))
                    return
                elif current_field == "end" and corrected_ms > self.final_start_bound:
                    time_tuple[2] = corrected_ms
                    self.handle_timeline_value_changes(tuple(time_tuple))

        if current_field == "start":
            field_obj.setText(self.format_time(self.final_start_bound))
        elif current_field == "playhead":
            field_obj.setText(self.format_time(self.player.position()))
        elif current_field == "end":
            field_obj.setText(self.format_time(self.final_end_bound))

    def update_thumbnails(self, index, pixmap):
        if index < len(self.thumbnails):
            scaled_pixmap = pixmap.scaled(
                self.thumbnails[index].size(),
                Qt.KeepAspectRatio,
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
        main_window = self.window()
        if not main_window.media_path or not self.frame_time:
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

    def playback_state_change(self, state):
        if state == QMediaPlayer.PlayingState:
            self.play_button.setChecked(True)
        else:
            self.play_button.setChecked(False)

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
        self.predicted_resolution.setText("Resolution: 1920x1080")
        self.size_info_list.addWidget(self.predicted_resolution)

        self.predicted_fps = QLabel()
        self.predicted_fps.setText("Frame Rate: 30FPS")
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

        self.desired_size_label = QLabel()
        self.desired_size_label.setAlignment(Qt.AlignCenter)
        self.desired_size_label.setText("Select Desired Bitrate:")
        self.desired_size_label.setStyleSheet("font-weight: bold; font-size: 30px;")
        self.center_radio1.addWidget(self.desired_size_label)
        self.center_radio1.addStretch()
        self.desired_bitrate_layout.addLayout(self.center_radio1)

        self.size_increment_hbox = QHBoxLayout()

        self.size_increment_label = QLabel()
        self.size_increment_label.setText("Size Increment: ")
        self.size_increment_hbox.addWidget(self.size_increment_label)

        self.size_increment_num = QLineEdit()
        self.size_increment_num.setValidator(QIntValidator(0,9999999,self))
        self.size_increment_num.setText("5")
        self.size_increment_hbox.addWidget(self.size_increment_num)

        self.size_increment_dropdown = QComboBox()
        self.size_increment_dropdown.addItems(["Kbps","Mbps"])
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
        self.select_size_layout.addLayout(self.center_radio2)

        self.desired_size_label2 = QLabel()
        self.desired_size_label2.setStyleSheet("font-weight: bold; font-size: 30px;")
        self.desired_size_label2.setText("Select Desired Size:")
        self.center_radio2.addWidget(self.desired_size_label2)
        self.center_radio2.addStretch()

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

    #Connections
        self.size_increment_slider.valueChanged.connect(self.calc_bitrate)
        self.size_increment_num.textChanged.connect(self.calc_bitrate)
        self.size_select_num.textChanged.connect(self.calc_bitrate)

        self.size_increment_dropdown.currentTextChanged.connect(self.calc_bitrate)
        self.size_select_dropdown.currentTextChanged.connect(self.calc_bitrate)

        self.desired_bitrate_radio.toggled.connect(self.handle_radio_toggle_sync)
        self.desired_size_radio.toggled.connect(self.handle_radio_toggle_sync)

        self.advanced_button.clicked.connect(lambda: self.window().main_workflow_stack.setCurrentIndex(3))
        self.advanced_button.clicked.connect(lambda: self.window().toggle_advanced())

        self.handle_radio_toggle_sync()
        self.calc_bitrate()

    def calc_bitrate(self):
        main_window = self.window()

        duration_seconds = main_window.snip_screen.player.duration() / 1000.0

        if self.desired_bitrate_radio.isChecked():
            bitrate_mbps = float(self.size_increment_slider.value())

            self.predicted_bitrate.setText(f"Bitrate: {int(bitrate_mbps)} {self.size_increment_dropdown.currentText()}")
        else: 
            try:
                desired_size = float(self.size_select_num.text())
            except ValueError:
                desired_size = 0.0
                
            unit = self.size_select_dropdown.currentText()
            if unit == "KB":
                bitrate_mbps = (desired_size * 8) / (1024.0 * duration_seconds) if duration_seconds > 0 else 0
            elif unit == "GB":
                bitrate_mbps = (desired_size * 8 * 1024.0) / duration_seconds if duration_seconds > 0 else 0
            else:
                bitrate_mbps = (desired_size * 8) / duration_seconds if duration_seconds > 0 else 0
                
            self.predicted_bitrate.setText(f"Bitrate: {bitrate_mbps:.2f} Mbps")
        
        final_size = (bitrate_mbps * duration_seconds) / 8.0

        final_measure = "MB" if self.desired_bitrate_radio.isChecked() else self.size_select_dropdown.currentText()

        self.predicted_size_label.setText(f"Predicted Size: {final_size:.2f} {final_measure}")

    def handle_radio_toggle_sync(self):
        """Toggle usability based off selection"""
        is_bitrate = self.desired_bitrate_radio.isChecked()

        self.size_increment_num.setEnabled(is_bitrate)
        self.size_increment_dropdown.setEnabled(is_bitrate)
        self.size_increment_slider.setEnabled(is_bitrate)

        self.size_select_num.setEnabled(not is_bitrate)
        self.size_select_dropdown.setEnabled(not is_bitrate)

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
        
        self.buttons.addSpacing(50)

        self.export_button = QPushButton("Export\nTo...")
        self.export_button.setFixedSize(100,50)
        self.export_button.clicked.connect(self.open_file_dialog)
        self.buttons.addWidget(self.export_button)
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

        if message_box.clickedButton() == new_project:
            main_window = self.window()
            main_window.master_stack.setCurrentIndex(0)
            main_window.login_stack.setCurrentIndex(3)
            main_window.main_workflow_stack.setCurrentIndex(0)
            self.file_name.setText(None)

class AdvancedSizeScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)

    # top predicted Size
        self.size_info = QHBoxLayout()
        self.size_info_list = QVBoxLayout()
        #left half
        self.predicted_size_label = QLabel()
        self.predicted_size_label.setText("Predicted Size: 0.00 MB")
        self.size_info.addWidget(self.predicted_size_label)

        #right half
        self.predicted_resolution = QLabel()
        self.predicted_resolution.setText("Resolution: 1920x1080")
        self.size_info_list.addWidget(self.predicted_resolution)

        self.predicted_fps = QLabel()
        self.predicted_fps.setText("Frame Rate: 30 FPS")
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

    #Selection boxes
        self.all_selections = QHBoxLayout()
        self.all_selections.addStretch()

        #Left half
        self.selections_left = QVBoxLayout()

        self.framerate_container = QHBoxLayout()
        self.framerate_label = QLabel()
        self.framerate_label.setText("Frame Rate: ")
        self.framerate_container.addWidget(self.framerate_label)
        self.framerate_input = QLineEdit()
        self.framerate_input.setValidator(QIntValidator(1,999999,self))
        self.framerate_input.setText("30")
        self.framerate_container.addWidget(self.framerate_input)
        self.framerate_suffix = QLabel()
        self.framerate_suffix.setText(" FPS")
        self.framerate_container.addWidget(self.framerate_suffix)
        self.selections_left.addLayout(self.framerate_container)

        self.width_container = QHBoxLayout()
        self.width_label = QLabel()
        self.width_label.setText("Width: ")
        self.width_container.addWidget(self.width_label)
        self.width_input = QLineEdit()
        self.width_input.setValidator(QIntValidator(1,999999,self))
        self.width_input.setText("1920")
        self.width_container.addWidget(self.width_input)
        self.width_suffix = QLabel()
        self.width_suffix.setText(" Px")
        self.width_container.addWidget(self.width_suffix)
        self.selections_left.addLayout(self.width_container)

        self.height_container = QHBoxLayout()
        self.height_label = QLabel()
        self.height_label.setText("Height: ")
        self.height_container.addWidget(self.height_label)
        self.height_input = QLineEdit()
        self.height_input.setValidator(QIntValidator(1,999999,self))
        self.height_input.setText("1080")
        self.height_container.addWidget(self.height_input)
        self.height_suffix = QLabel()
        self.height_suffix.setText(" Px")
        self.height_container.addWidget(self.height_suffix)
        self.selections_left.addLayout(self.height_container)

        self.all_selections.addLayout(self.selections_left)
        self.all_selections.addSpacing(50)

    # Right Selections
        self.selection_right = QVBoxLayout()

        self.codec_container = QHBoxLayout()
        self.codec_label = QLabel()
        self.codec_label.setText("Codec: ")
        self.codec_container.addWidget(self.codec_label)
        self.codec_dropdown = QComboBox()
        self.codec_dropdown.addItems(["H.264", "H.265", "AV1"])
        self.codec_dropdown.setCurrentIndex(1)
        self.codec_container.addWidget(self.codec_dropdown)
        self.selection_right.addLayout(self.codec_container)

        self.bitrate_container = QHBoxLayout()
        self.bitrate_label = QLabel()
        self.bitrate_label.setText("Bitrate: ")
        self.bitrate_container.addWidget(self.bitrate_label)
        self.bitrate_input = QLineEdit()
        self.bitrate_input.setValidator(QIntValidator(1,999999,self))
        self.bitrate_input.setText("15")
        self.bitrate_container.addWidget(self.bitrate_input)
        self.bitrate_dropdown = QComboBox()
        self.bitrate_dropdown.addItems(["Kbps", "Mbps"])
        self.bitrate_dropdown.setCurrentIndex(1)
        self.bitrate_container.addWidget(self.bitrate_dropdown)
        self.selection_right.addLayout(self.bitrate_container)

        self.all_selections.addLayout(self.selection_right)
        self.all_selections.addStretch()

        layout.addLayout(self.all_selections)
        layout.addSpacing(40)

    # Button
        self.basic_button = QPushButton("Basic")
        layout.addWidget(self.basic_button)
        layout.addStretch()

    #Connections
        self.basic_button.clicked.connect(lambda: self.window().main_workflow_stack.setCurrentIndex(1))
        self.basic_button.clicked.connect(lambda: self.window().toggle_advanced())

        self.framerate_input.textChanged.connect(lambda text: self.predicted_fps.setText(f"Frame Rate: {text or '0'} FPS"))
        self.width_input.textChanged.connect(lambda text: self.predicted_resolution.setText(f"Resolution: {text or '0'}x{self.height_input.text() or '0'}"))
        self.height_input.textChanged.connect(lambda text: self.predicted_resolution.setText(f"Resolution: {self.width_input.text() or '0'}x{text or '0'}"))
        self.codec_dropdown.currentTextChanged.connect(lambda text: self.predicted_codec.setText(f"Codec: {text}"))
        self.bitrate_input.textChanged.connect(lambda text: self.predicted_bitrate.setText(f"Bitrate: {text or '0'} {self.bitrate_dropdown.currentText() or 'Mbps'}"))
        self.bitrate_dropdown.currentTextChanged.connect(lambda text: self.predicted_bitrate.setText(f"Bitrate: {self.bitrate_input.text() or '0'} {text}"))

        self.framerate_input.textChanged.connect(lambda: self.calc_bitrate())
        self.width_input.textChanged.connect(lambda: self.calc_bitrate())
        self.height_input.textChanged.connect(lambda: self.calc_bitrate())
        self.codec_dropdown.currentTextChanged.connect(lambda: self.calc_bitrate())
        self.bitrate_input.textChanged.connect(lambda: self.calc_bitrate())
        self.bitrate_dropdown.currentTextChanged.connect(lambda: self.calc_bitrate())

        self.calc_bitrate()
        
    def calc_bitrate(self):
        #TODO: calculate it in a real way
        result = (
            int(self.framerate_input.text() or 0) 
            + int(self.width_input.text() or 0) 
            + int(self.height_input.text() or 0)
            + int(self.bitrate_input.text() or 0)
        )

        result = result/20
        result = float(result/3.14)
        
        self.predicted_size_label.setText(f"Predicted Size: {round(result,2)} MB")

        
class ErrorScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        #TODO: Add Later