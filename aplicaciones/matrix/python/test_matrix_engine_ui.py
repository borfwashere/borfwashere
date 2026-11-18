import os

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PyQt6.QtWidgets import QApplication

import matrix_engine


def test_window_builds_with_each_mode_and_switches():
    app = QApplication.instance() or QApplication([])

    for mode in matrix_engine.MODES:
        window = matrix_engine.MatrixEngine(mode=mode)
        assert window.mode == mode
        assert window.viewport is not None
        assert window.btn_toggle.text() == "START CAM"
        window.set_mode("rain")
        assert window.mode == "rain"
        window.set_mode("invalid")
        assert window.mode == "rain"
        window.close()

    assert app is not None


def test_rain_state_is_rebuilt_when_column_count_changes():
    app = QApplication.instance() or QApplication([])

    window = matrix_engine.MatrixEngine(mode="rain")
    window.ensure_rain_state(40)
    assert len(window.drops) == 40
    window.ensure_rain_state(90)
    assert len(window.drops) == 90
    window.close()

    assert app is not None
