import numpy as np

from matrix_engine import (
    CHARS,
    MODES,
    apply_rain,
    ascii_indices,
    parse_args,
    render_ascii,
)


def test_render_ascii_keeps_requested_columns_and_aspect():
    frame = np.full((90, 160, 3), 255, dtype=np.uint8)
    text = render_ascii(frame, cols=20)

    lines = text.split("\n")
    assert all(len(line) == 20 for line in lines)
    assert len(lines) == int(20 * (90 / 160) * 0.42)


def test_render_ascii_maps_bright_and_dark_pixels_to_extreme_chars():
    frame = np.zeros((40, 40, 3), dtype=np.uint8)
    frame[:, :20] = 255

    first_row = render_ascii(frame, cols=20).split("\n")[0]

    assert set(first_row[:10]) == {CHARS[-1]}
    assert set(first_row[10:]) == {" "}


def test_ascii_indices_returns_int_matrix_with_valid_range():
    frame = np.full((30, 30, 3), 128, dtype=np.uint8)
    indices = ascii_indices(frame, cols=10)

    assert indices.dtype.kind == "i"
    assert indices.shape == (int(10 * (30 / 30) * 0.42), 10)
    assert indices.min() >= 0
    assert indices.max() <= len(CHARS) - 1


def test_apply_rain_boosts_head_and_keeps_far_rows_untouched():
    base = np.full((20, 1), 4, dtype=np.int16)
    drops = np.array([5.0])
    speeds = np.array([1.0])

    out, new_drops, new_speeds = apply_rain(
        base, drops, speeds, head_size=1, trail_length=10, rng=np.random.default_rng(0)
    )

    assert out[5, 0] == min(len(CHARS) - 1, 4 + 3)
    assert out[10, 0] == 4
    assert new_drops[0] == 6.0
    assert new_speeds[0] == 1.0


def test_apply_rain_erases_characters_inside_the_trail():
    base = np.full((10, 4), 4, dtype=np.int16)
    drops = np.full(4, 5.0)
    speeds = np.ones(4)

    out, _, _ = apply_rain(
        base, drops, speeds, head_size=1, trail_length=10, rng=np.random.default_rng(7)
    )

    trail_zone = out[0:4, :]
    assert (trail_zone == 0).any()
    assert (trail_zone <= 4).all()


def test_parse_args_defaults_to_desktop_and_reads_mode():
    assert parse_args([]).mode == "desktop"
    assert parse_args(["--mode", "rain"]).mode == "rain"
    assert parse_args(["--mode", "pure"]).mode == "pure"


def test_modes_expose_the_three_supported_engines():
    assert set(MODES) == {"pure", "rain", "desktop"}
