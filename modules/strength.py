def get_strength_label(entropy_bits: float) -> dict:
    """
    Klasifikasikan kekuatan password berdasarkan entropy (bit).
    Return dict berisi label, warna, dan persentase progress bar (0.0 - 1.0).
    """
    if entropy_bits < 28:
        return {"label": "Sangat Lemah", "color": "#e74c3c", "progress": 0.2}
    elif entropy_bits < 36:
        return {"label": "Lemah", "color": "#e67e22", "progress": 0.4}
    elif entropy_bits < 60:
        return {"label": "Sedang", "color": "#f1c40f", "progress": 0.6}
    elif entropy_bits < 100:
        return {"label": "Kuat", "color": "#2ecc71", "progress": 0.85}
    else:
        return {"label": "Sangat Kuat", "color": "#27ae60", "progress": 1.0}
