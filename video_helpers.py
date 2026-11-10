import subprocess
import os
from PySide6.QtCore import QObject, QRunnable, QThread, Signal
from PySide6.QtGui import QImage, QPixmap

class WorkerSignal(QObject):
    frame_ready = Signal(int, QPixmap)

class CreateThumbnails(QRunnable):
    # sort of an transmission object, whereas we will use this to send our frames
    

    def __init__(self, file_path, total_duration_ms):
        super().__init__()
        self.file_path = file_path
        self.duration = total_duration_ms
        self.signals = WorkerSignal()

    def run(self) -> None:
        timestamps = self.duration / 10.0

        for i in range(10):
            # gives the center of each section
            target_ms = int((i * timestamps) + (timestamps / 2))
            seconds = target_ms/1000.0

            cmd = [
                'ffmpeg', 
                '-nostdin',
                '-err_detect', 'ignore_err',
                '-fflags', '+genpts',
                '-ss', str(seconds),
                '-i', self.file_path,
                '-vframes', '1',
                '-s', '80x45',
                '-f', 'image2pipe',
                '-vcodec', 'mjpeg',
                'pipe:1'
            ]

            startup_info = subprocess.STARTUPINFO()
            startup_info.dwFlags |= subprocess.STARTF_USESHOWWINDOW

            try:
                process = subprocess.Popen(
                    cmd, 
                    stdout=subprocess.PIPE, 
                    stderr=subprocess.PIPE,
                    startupinfo=startup_info)
                stdout, _ = process.communicate()

                q_img = QImage.fromData(stdout)

                if not q_img.isNull():
                    pixmap = QPixmap.fromImage(q_img)

                    self.signals.frame_ready.emit(i, pixmap)
            except Exception as e:
                print(e)
                pass