from zxcvbn import zxcvbn

from modules.entropy import calculate_entropy
from modules.generator import detect_charset_size

SCORE_STYLE = {
    0: {"label": "Sangat Lemah", "color": "#e74c3c", "progress": 0.15},
    1: {"label": "Lemah", "color": "#e67e22", "progress": 0.35},
    2: {"label": "Sedang", "color": "#f1c40f", "progress": 0.6},
    3: {"label": "Kuat", "color": "#2ecc71", "progress": 0.85},
    4: {"label": "Sangat Kuat", "color": "#27ae60", "progress": 1.0},
}


def check_password_strength(password: str) -> dict:
    """
    Analisis kekuatan password yang diinput manual oleh user.
    Pakai zxcvbn untuk deteksi pola lemah (dictionary, keyboard pattern,
    pengulangan, dsb) + entropy.py buat estimasi bit entropy dari charset.
    """
    if not password:
        return {
            "label": "-",
            "color": "#9e9e9e",
            "progress": 0.0,
            "score": None,
            "entropy_bits": 0.0,
            "crack_time": "-",
            "warning": "",
            "suggestions": [],
        }

    result = zxcvbn(password)
    score = result["score"]
    style = SCORE_STYLE[score]

    charset_size = detect_charset_size(password)
    entropy_bits = calculate_entropy(len(password), charset_size)

    crack_time = result["crack_times_display"]["offline_slow_hashing_1e4_per_second"]
    feedback = result.get("feedback", {})

    return {
        "label": style["label"],
        "color": style["color"],
        "progress": style["progress"],
        "score": score,
        "entropy_bits": entropy_bits,
        "crack_time": crack_time,
        "warning": feedback.get("warning", ""),
        "suggestions": feedback.get("suggestions", []),
    }
