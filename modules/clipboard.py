import pyperclip


def copy_to_clipboard(text: str) -> bool:
    """
    Copy teks ke clipboard sistem pakai pyperclip.
    Return True kalau berhasil, False kalau teks kosong atau gagal
    (misal di Linux tanpa xclip/xsel terpasang).
    """
    if not text:
        return False

    try:
        pyperclip.copy(text)
        return True
    except pyperclip.PyperclipException:
        return False
