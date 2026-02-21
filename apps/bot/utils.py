import hashlib
import hmac
from urllib.parse import parse_qsl


def verify_telegram_data(init_data: str, bot_token: str):
    data = dict(parse_qsl(init_data, strict_parsing=True))

    hash_value = data.pop("hash", None)

    if not hash_value:
        return False, None

    data_check_string = "\n".join(
        f"{k}={v}" for k, v in sorted(data.items())
    )

    secret_key = hashlib.sha256(bot_token.encode()).digest()

    calculated_hash = hmac.new(
        secret_key,
        data_check_string.encode(),
        hashlib.sha256
    ).hexdigest()

    if calculated_hash != hash_value:
        return False, None

    return True, data
