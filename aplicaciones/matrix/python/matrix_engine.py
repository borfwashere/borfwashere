import argparse
import random
import sys

import cv2
import numpy as np
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QColor, QFont
from PyQt6.QtWidgets import (
    QApplication,
    QColorDialog,
    QComboBox,
    QFileDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSlider,
    QVBoxLayout,
    QWidget,
)

CHARS = np.array(list(" .:-=+*#%@"))
MODES = ("pure", "rain", "desktop")
ASPECT_FACTOR = 0.42
DEFAULT_COLS = 180
DEFAULT_GAMMA = 1.8


def gamma_table(gamma):
    inv_gamma = 1.0 / gamma
    return np.array(
        [((i / 255.0) ** inv_gamma) * 255 for i in range(256)]
    ).astype("uint8")


def ascii_indices(frame, cols, gamma=DEFAULT_GAMMA, normalize=True):
    aspect = frame.shape[0] / frame.shape[1]
    rows = max(1, int(cols * aspect * ASPECT_FACTOR))
    small = cv2.resize(frame, (cols, rows))
    gray = cv2.cvtColor(small, cv2.COLOR_BGR2GRAY)
    gray = cv2.LUT(gray, gamma_table(gamma))
    if normalize:
        gray = cv2.normalize(gray, None, 0, 255, cv2.NORM_MINMAX)
    bins = np.linspace(0, 255, len(CHARS))
    indices = np.digitize(gray, bins) - 1
    return np.clip(indices, 0, len(CHARS) - 1).astype(np.int16)


def render_ascii(frame, cols, gamma=DEFAULT_GAMMA):
    indices = ascii_indices(frame, cols, gamma)
    return "\n".join("".join(CHARS[row]) for row in indices)


def apply_rain(base, drops, speeds, head_size=4, trail_length=22, rng=None):
    rng = rng or random
    height, width = base.shape
    drops = drops + speeds
    for x in range(width):
        if drops[x] - trail_length > height:
            drops[x] = rng.uniform(-40, 0)
            speeds[x] = rng.uniform(0.4, 1.2)
    out = base.copy()
    for x in range(width):
        head = drops[x]
        for y in range(height):
            idx = int(base[y, x])
            if head - head_size <= y <= head:
                boosted = min(len(CHARS) - 1, idx + 3)
                out[y, x] = boosted if idx > 0 else 0
            elif head - trail_length <= y < head - head_size:
                distance = (head - head_size) - y
                delete_chance = distance / max(1, trail_length - head_size)
                if rng.random() < delete_chance * 0.85:
                    out[y, x] = 0
    return out, drops, speeds


def parse_args(argv=None):
    parser = argparse.ArgumentParser(prog="matrix_engine")
    parser.add_argument("--mode", choices=MODES, default="desktop")
    parser.add_argument("--cols", type=int, default=DEFAULT_COLS)
    return parser.parse_args(argv)


class MatrixEngine(QWidget):
    def __init__(self, mode="desktop", cols=DEFAULT_COLS):
        super().__init__()
        self.mode = mode if mode in MODES else "desktop"
        self.cols = cols
        self.gamma = DEFAULT_GAMMA
        self.cap = None
        self.current_camera_index = 0
        self.available_cams = self.scan_cameras()
        self.is_fullscreen = False
        self.bg_color = QColor("#000080")
        self.fg_color = QColor("#ffffff")
        self.font_size = 8
        self.drops = None
        self.speeds = None
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.init_ui()

    def scan_cameras(self):
        found = []
        for index in range(4):
            capture = cv2.VideoCapture(index, cv2.CAP_DSHOW)
            if capture.isOpened():
                found.append(index)
                capture.release()
        return found if found else [0]

    def init_ui(self):
        self.setWindowTitle(f"Matrix Engine - Unified ({self.mode})")
        self.setFixedSize(1100, 850)
        self.setStyleSheet("background-color: #018281;")

        self.main_layout = QVBoxLayout(self)
        self.body = QFrame()
        self.body.setStyleSheet("background-color: #c0c0c0; border: 2px solid white;")
        self.body_layout = QVBoxLayout(self.body)
        self.body_layout.setContentsMargins(2, 2, 2, 2)

        self.title_bar = QLabel(" Matrix Engine - Unified Core")
        self.title_bar.setFixedHeight(22)
        self.title_bar.setStyleSheet(
            "background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #000080, stop:1 #1084d0);"
            " color: white; font-weight: bold; padding-left: 5px;"
        )
        self.body_layout.addWidget(self.title_bar)

        self.viewport = QLabel("SYSTEM READY\nWAITING FOR DATA...")
        self.viewport.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.update_viewport_style()
        self.body_layout.addWidget(self.viewport, 10)

        self.controls_container = QWidget()
        self.controls_layout = QVBoxLayout(self.controls_container)
        self.controls_layout.setContentsMargins(0, 4, 0, 0)

        btn_style = (
            "QPushButton { background-color: #c0c0c0; border: 2px outset white;"
            " padding: 6px; font-weight: bold; min-width: 85px; }"
            "QPushButton:pressed { border: 2px inset white; }"
        )

        row1 = QHBoxLayout()
        self.btn_toggle = QPushButton("START CAM")
        self.btn_toggle.setStyleSheet(btn_style)
        self.btn_toggle.clicked.connect(self.toggle_camera)

        self.btn_switch = QPushButton(f"DEVICE: {self.current_camera_index}")
        self.btn_switch.setStyleSheet(btn_style)
        self.btn_switch.clicked.connect(self.next_camera)

        self.btn_import = QPushButton("LOAD VIDEO")
        self.btn_import.setStyleSheet(btn_style)
        self.btn_import.clicked.connect(self.load_video)

        row1.addWidget(self.btn_toggle)
        row1.addWidget(self.btn_switch)
        row1.addWidget(self.btn_import)

        self.mode_box = QComboBox()
        self.mode_box.addItems(list(MODES))
        self.mode_box.setCurrentText(self.mode)
        self.mode_box.currentTextChanged.connect(self.set_mode)
        row1.addWidget(self.mode_box)

        self.btn_bg = QPushButton("BG COLOR")
        self.btn_bg.setStyleSheet(btn_style)
        self.btn_bg.clicked.connect(self.pick_bg_color)

        self.btn_fg = QPushButton("FG COLOR")
        self.btn_fg.setStyleSheet(btn_style)
        self.btn_fg.clicked.connect(self.pick_fg_color)
        row1.addWidget(self.btn_bg)
        row1.addWidget(self.btn_fg)
        self.controls_layout.addLayout(row1)

        row2 = QHBoxLayout()
        row2.addWidget(QLabel("DIGIT SIZE:"))
        self.size_slider = QSlider(Qt.Orientation.Horizontal)
        self.size_slider.setRange(4, 40)
        self.size_slider.setValue(self.font_size)
        self.size_slider.valueChanged.connect(self.set_font_size)
        row2.addWidget(self.size_slider)

        self.status_lbl = QLabel("CORE: WAITING\nSOURCE: NONE")
        self.status_lbl.setStyleSheet(
            "color: #000080; font-family: 'Courier New'; font-weight: bold;"
        )
        row2.addWidget(self.status_lbl)
        self.controls_layout.addLayout(row2)

        self.body_layout.addWidget(self.controls_container)
        self.main_layout.addWidget(self.body)

    def set_mode(self, mode):
        if mode not in MODES:
            return
        self.mode = mode
        self.setWindowTitle(f"Matrix Engine - Unified ({self.mode})")
        self.drops = None
        self.speeds = None

    def set_font_size(self, value):
        self.font_size = value
        self.update_viewport_style()

    def pick_bg_color(self):
        color = QColorDialog.getColor(self.bg_color, self)
        if color.isValid():
            self.bg_color = color
            self.update_viewport_style()

    def pick_fg_color(self):
        color = QColorDialog.getColor(self.fg_color, self)
        if color.isValid():
            self.fg_color = color
            self.update_viewport_style()

    def update_viewport_style(self):
        background = self.bg_color.name()
        foreground = self.fg_color.name()
        border = "none" if self.is_fullscreen else "4px inset white"
        self.viewport.setStyleSheet(
            f"background-color: {background}; color: {foreground};"
            f" border: {border}; line-height: 95%;"
        )
        self.viewport.setFont(QFont("Courier New", self.font_size, QFont.Weight.Bold))

    def toggle_camera(self):
        if self.timer.isActive():
            self.stop_current()
            self.btn_toggle.setText("START CAM")
            self.status_lbl.setText("CORE: IDLE\nSOURCE: NONE")
            return
        cam_id = self.available_cams[self.current_camera_index]
        self.cap = cv2.VideoCapture(cam_id, cv2.CAP_DSHOW)
        if self.cap.isOpened():
            self.timer.start(30)
            self.btn_toggle.setText("STOP CAM")
            self.status_lbl.setText(f"CORE: RUNNING\nSOURCE: CAM {cam_id}")
        else:
            self.status_lbl.setText("CORE: ERROR\nCAM NOT FOUND")

    def next_camera(self):
        self.current_camera_index = (self.current_camera_index + 1) % len(self.available_cams)
        self.btn_switch.setText(f"DEVICE: {self.current_camera_index}")
        if self.timer.isActive():
            self.toggle_camera()
            self.toggle_camera()

    def load_video(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Open Matrix Video", "", "Video Files (*.mp4 *.avi *.mov)"
        )
        if not path:
            return
        self.stop_current()
        self.cap = cv2.VideoCapture(path)
        if self.cap.isOpened():
            self.timer.start(30)
            self.btn_toggle.setText("STOP CAM")
            self.status_lbl.setText("CORE: RUNNING\nSOURCE: VIDEO")

    def stop_current(self):
        self.timer.stop()
        if self.cap:
            self.cap.release()
            self.cap = None

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_F11:
            self.toggle_fullscreen()
        elif event.key() == Qt.Key.Key_Escape and self.is_fullscreen:
            self.toggle_fullscreen()

    def toggle_fullscreen(self):
        self.is_fullscreen = not self.is_fullscreen
        if self.is_fullscreen:
            self.title_bar.hide()
            self.controls_container.hide()
            self.main_layout.setContentsMargins(0, 0, 0, 0)
            self.body_layout.setContentsMargins(0, 0, 0, 0)
            self.showFullScreen()
        else:
            self.title_bar.show()
            self.controls_container.show()
            self.main_layout.setContentsMargins(10, 10, 10, 10)
            self.body_layout.setContentsMargins(2, 2, 2, 2)
            self.showNormal()
        self.update_viewport_style()

    def target_cols(self):
        if self.mode == "desktop":
            width = max(1, self.viewport.width())
            return max(20, int(width / max(1.0, self.font_size * 0.6)))
        return self.cols

    def ensure_rain_state(self, cols):
        if self.drops is None or len(self.drops) != cols:
            self.drops = np.array([random.uniform(-100, 0) for _ in range(cols)])
            self.speeds = np.array([random.uniform(0.4, 1.2) for _ in range(cols)])

    def update_frame(self):
        if not self.cap or not self.cap.isOpened():
            return
        ret, frame = self.cap.read()
        if not ret:
            if self.cap.get(cv2.CAP_PROP_FRAME_COUNT) > 0:
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            return

        cols = self.target_cols()
        indices = ascii_indices(frame, cols, self.gamma)

        if self.mode == "rain":
            self.ensure_rain_state(cols)
            indices, self.drops, self.speeds = apply_rain(
                indices, self.drops, self.speeds, head_size=4, trail_length=22
            )

        text = "\n".join("".join(CHARS[row]) for row in indices)
        self.viewport.setText(text)

    def closeEvent(self, event):
        self.stop_current()


def main(argv=None):
    args = parse_args(argv)
    app = QApplication(sys.argv)
    window = MatrixEngine(mode=args.mode, cols=args.cols)
    window.show()
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
