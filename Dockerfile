FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    ffmpeg \
    mediainfo \
    xvfb \
    x11vnc \
    novnc \
    websockify \
    fluxbox \
    libegl1 \
    libgl1 \
    libdbus-1-3 \
    libxcb-cursor0 \
    libxcb-icccm4 \
    libxcb-image0 \
    libxcb-keysyms1 \
    libxcb-randr0 \
    libxcb-render-util0 \
    libxcb-shape0 \
    libxcb-xinerama0 \
    libxcb-xkb1 \
    libxkbcommon-x11-0 \
    libfontconfig1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir PySide6 pymediainfo superqt

ENV DISPLAY=:0
ENV QT_QPA_PLATFORM=xcb

EXPOSE 7860

CMD ["sh", "-c", "rm -f /tmp/.X0-lock && Xvfb :0 -screen 0 1024x680x24 & sleep 2 && fluxbox & x11vnc -display :0 -forever -nopw -rfbport 5900 & websockify --web=/usr/share/novnc/ 7860 localhost:5900 & python app.py"]
