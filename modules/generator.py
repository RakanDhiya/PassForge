import secrets
import string

AMBIGUOUS_CHARS = "Il1O0"
SYMBOL_CHARS = "!@#$%^&*()-_=+[]{};:,.<>?/"


def _filter_ambiguous(chars: str, exclude_ambiguous: bool) -> str:
    if not exclude_ambiguous:
        return chars
    return "".join(c for c in chars if c not in AMBIGUOUS_CHARS)


def get_charset_pools(use_upper=True, use_lower=True, use_digits=True,
                    use_symbols=True, exclude_ambiguous=False) -> list[str]:
    """
    Return list pool karakter per kategori yang aktif.
    Berguna untuk memastikan minimal 1 karakter tiap kategori muncul.
    """
    pools = []

    if use_upper:
        pools.append(_filter_ambiguous(string.ascii_uppercase, exclude_ambiguous))
    if use_lower:
        pools.append(_filter_ambiguous(string.ascii_lowercase, exclude_ambiguous))
    if use_digits:
        pools.append(_filter_ambiguous(string.digits, exclude_ambiguous))
    if use_symbols:
        pools.append(SYMBOL_CHARS)

    # buang pool yang kosong gara-gara difilter habis
    return [p for p in pools if p]


def build_charset(**kwargs) -> str:
    pools = get_charset_pools(**kwargs)
    return "".join(pools)


def generate_password(length=16, use_upper=True, use_lower=True, use_digits=True,
                    use_symbols=True, exclude_ambiguous=False) -> str:
    """
    Generate password random secara aman (pakai random.SystemRandom).
    Menjamin minimal 1 karakter dari tiap kategori yang aktif.
    """
    pools = get_charset_pools(
        use_upper=use_upper,
        use_lower=use_lower,
        use_digits=use_digits,
        use_symbols=use_symbols,
        exclude_ambiguous=exclude_ambiguous,
    )

    if not pools:
        raise ValueError("Minimal satu jenis karakter harus dipilih!")

    full_charset = "".join(pools)

    if length < 1:
        raise ValueError("Panjang password minimal 1 karakter!")

    # pastikan tiap kategori aktif terwakili minimal 1 karakter
    guaranteed = [secrets.choice(pool) for pool in pools[:length]]

    remaining = max(length - len(guaranteed), 0)
    password_chars = guaranteed + [secrets.choice(full_charset) for _ in range(remaining)]

    _secure_shuffle(password_chars)

    return "".join(password_chars[:length])


def _secure_shuffle(chars: list) -> None:
    """
    Fisher-Yates shuffle pakai secrets.randbelow (in-place),
    biar konsisten pakai sumber random cryptographically secure.
    """
    for i in range(len(chars) - 1, 0, -1):
        j = secrets.randbelow(i + 1)
        chars[i], chars[j] = chars[j], chars[i]


def detect_charset_size(password: str) -> int:
    """
    Deteksi ukuran charset dari sebuah password yang sudah ada
    (dipakai oleh Password Strength Checker untuk hitung entropy).
    """
    size = 0
    if any(c.islower() for c in password):
        size += 26
    if any(c.isupper() for c in password):
        size += 26
    if any(c.isdigit() for c in password):
        size += 10
    if any(not c.isalnum() for c in password):
        size += len(SYMBOL_CHARS)

    return size
