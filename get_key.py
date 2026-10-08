#!/usr/bin/env python3
"""Get your scooter's Bluetooth key out of your Xiaomi account.

Signs in to Xiaomi, looks for the scooters of your account in every region and asks for the key of
each one. What it prints (64 characters) is what you paste into the app, together with the PIN you
set for the scooter in Mi Home.

    python get_key.py              # sign in with a link: you type the password on xiaomi.com
    python get_key.py --lang es    # mensajes en castellano
    python get_key.py --password   # user and password in the terminal (captcha and e-mail code)
    python get_key.py --server de  # look in one region only (faster)
It only talks to Xiaomi's servers. It stores nothing on disk and sends nothing to third parties.
"""

import argparse
import json
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

MESSAGES = {
    "en": {
        "unknown_region": "Unknown region: {server}. Valid ones: {valid}",
        "login_password": "Sign in with your Xiaomi account (the password is not shown while you type).\n",
        "signin_first": "1. First sign in to Xiaomi in your browser: https://account.xiaomi.com\n"
                        "   (if you open the link below without being signed in, Xiaomi answers\n"
                        "   \"Invalid request\").\n",
        "qr": "2. Then scan this code with that same device, or use the link below.\n",
        "link_open": "2. Then open this link in that same browser:\n",
        "link_back": "3. Come back here: the program carries on by itself.\n",
        "login_failed": "\nCould not sign in.",
        "searching": "\nSigned in. Looking for scooters…\n",
        "searching_all": "\nSigned in. Looking for scooters in every region…\n",
        "no_name": "(no name)",
        "scooter": "Scooter: {name}",
        "details": "  model: {model}   region: {server}   id: {did}",
        "key_failed": "  Could not get the key ({detail}).\n",
        "key": "\n  KEY: {key}\n",
        "odd_type": "  Warning: key type {type}, not the usual one (1, protected with the PIN). "
                    "The app may not accept it.",
        "paste": "  Copy it and paste it into the app, together with the PIN you set for the scooter "
                 "in Mi Home.\n",
        "none": "There is no scooter in this account. Check that you added it in Mi Home with this same\n"
                "account and that it is yours (not shared by someone else).",
        "bad_response": "Xiaomi's response: {response}",
        "no_key": "the response has no key",
    },
    "es": {
        "unknown_region": "Región desconocida: {server}. Valen: {valid}",
        "login_password": "Inicia sesión con tu cuenta de Xiaomi (la contraseña no se ve al escribir).\n",
        "signin_first": "1. Primero inicia sesión en Xiaomi en tu navegador: https://account.xiaomi.com\n"
                        "   (si abres el enlace de abajo sin haber iniciado sesión, Xiaomi contesta\n"
                        "   «Invalid request»).\n",
        "qr": "2. Después escanea este código con ese mismo dispositivo, o usa el enlace de abajo.\n",
        "link_open": "2. Después abre este enlace en ese mismo navegador:\n",
        "link_back": "3. Vuelve aquí: el programa sigue solo.\n",
        "login_failed": "\nNo se pudo iniciar sesión.",
        "searching": "\nSesión iniciada. Buscando patinetes…\n",
        "searching_all": "\nSesión iniciada. Buscando patinetes en todas las regiones…\n",
        "no_name": "(sin nombre)",
        "scooter": "Patinete: {name}",
        "details": "  modelo: {model}   región: {server}   id: {did}",
        "key_failed": "  No se pudo obtener la clave ({detail}).\n",
        "key": "\n  CLAVE: {key}\n",
        "odd_type": "  Aviso: tipo de clave {type}, no el habitual (1, protegida con el PIN). "
                    "Puede que la app no la acepte.",
        "paste": "  Cópiala y pégala en la app, junto con el PIN que le pusiste al patinete en Mi Home.\n",
        "none": "No hay ningún patinete en esta cuenta. Comprueba que lo tienes añadido en Mi Home con esta\n"
                "misma cuenta y que es tuyo (no compartido por otra persona).",
        "bad_response": "respuesta de Xiaomi: {response}",
        "no_key": "la respuesta no trae clave",
    },
}

_lang = "en"


def t(message: str, **values) -> str:
    """The message in the chosen language."""
    return MESSAGES[_lang][message].format(**values)


def _print_qr(url: str) -> None:
    """Draws the QR of the link with text characters, if it fits; otherwise prints nothing.

    Two modules per character (upper half block), with explicit black and white so that it reads
    the same on a dark or a light background. Only on a real terminal: the output of a notebook
    leaves a gap between lines that cuts the code into stripes and no camera reads it.
    """
    if not sys.stdout.isatty():
        return
    try:
        import qrcode
    except ImportError:
        return
    code = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_L, border=2)
    code.add_data(url)
    code.make(fit=True)
    rows = code.get_matrix()
    if len(rows[0]) > shutil.get_terminal_size().columns:
        return
    if len(rows) % 2:
        rows.append([False] * len(rows[0]))
    print(t("qr"))
    for top, bottom in zip(rows[0::2], rows[1::2]):
        line = "".join(f"\033[{30 if up else 97};{40 if down else 107}m▀" for up, down in zip(top, bottom))
        print(line + "\033[0m")
    print()


def _homes(connector, server):
    """Own and shared homes of the account in one region (empty list if none or on failure)."""
    homes = []
    try:
        own = connector.get_homes(server)
        if own:
            for home in own["result"]["homelist"]:
                homes.append((home["id"], connector.userId))
        shared = connector.get_dev_cnt(server)
        if shared:
            for home in shared["result"]["share"]["share_family"]:
                homes.append((home["home_id"], home["home_owner"]))
    except (KeyError, TypeError):
        pass
    return homes


def _scooters(connector, server):
    """Devices of that region whose model is a scooter."""
    found = []
    for home_id, owner_id in _homes(connector, server):
        try:
            devices = connector.get_devices(server, home_id, owner_id)
            infos = (devices or {}).get("result", {}).get("device_info") or []
        except (KeyError, TypeError, AttributeError):
            continue
        for device in infos:
            if "scooter" in str(device.get("model", "")).lower() and device.get("did"):
                found.append(device)
    return found


def _bluetooth_key(connector, server, did):
    """Returns (key in hex, encrypt_type) or (None, reason)."""
    url = connector.get_api_url(server) + "/share/askbluetoothkey"
    data = json.dumps({"type": "own", "did": str(did), "keyid": 0}, separators=(",", ":"))
    try:
        response = connector.execute_api_call_encrypted(url, {"data": data})
    except Exception as error:  # the network or Xiaomi's response can fail in many ways
        return None, f"{type(error).__name__}: {error}"
    if not response or response.get("code") != 0 or "result" not in response:
        return None, t("bad_response", response=response)
    result = response["result"]
    if not result.get("key"):
        return None, t("no_key")
    return result["key"], int(result.get("encrypt_type", 0))


def main() -> int:
    global _lang
    parser = argparse.ArgumentParser(description="Get your scooter's Bluetooth key out of your Xiaomi account.")
    parser.add_argument("--lang", choices=sorted(MESSAGES), default="en",
                        help="language of the messages (default: en)")
    parser.add_argument("--password", action="store_true",
                        help="sign in with user and password in the terminal, instead of with a link")
    parser.add_argument("--server", help="look in this region only (cn, de, us, ru, tw, sg, in, i2)")
    options = parser.parse_args()
    _lang = options.lang

    # token_extractor parses its own arguments on import: give it an empty command line.
    sys.argv = [sys.argv[0]]
    sys.path.insert(0, HERE)
    import token_extractor as xiaomi

    if options.server and options.server not in xiaomi.SERVERS:
        print(t("unknown_region", server=options.server, valid=", ".join(xiaomi.SERVERS)))
        return 2

    if options.password:
        connector = xiaomi.PasswordXiaomiCloudConnector()
        print(t("login_password"))
    else:
        class LinkXiaomiCloudConnector(xiaomi.QrCodeXiaomiCloudConnector):
            """The same sign-in, showing only the link.

            The original also downloads a QR and serves it at http://127.0.0.1:31415, an address
            that does not exist for someone running this in Colab. Here the QR of that same link is
            drawn in the output instead.
            """

            def login_step_2(self) -> bool:
                # The original requests Xiaomi's QR image before showing the link. The image is not
                # used here, but the request is kept so that Xiaomi sees the same steps as before.
                try:
                    self._session.get(self._qr_image_url, timeout=10)
                except Exception:
                    pass
                print(t("signin_first"))
                _print_qr(self._login_url)
                print(t("link_open"))
                print(f"  {self._login_url}\n")
                print(t("link_back"), flush=True)
                return True

        connector = LinkXiaomiCloudConnector()

    if not connector.login():
        print(t("login_failed"))
        return 1

    servers = [options.server] if options.server else xiaomi.SERVERS
    print(t("searching" if options.server else "searching_all"))

    total = 0
    for server in servers:
        for device in _scooters(connector, server):
            total += 1
            print(t("scooter", name=device.get("name") or t("no_name")))
            print(t("details", model=device.get("model"), server=server, did=device["did"]))
            key, detail = _bluetooth_key(connector, server, device["did"])
            if key is None:
                print(t("key_failed", detail=detail))
                continue
            print(t("key", key=key))
            if detail != 1:
                print(t("odd_type", type=detail))
            print(t("paste"))

    if total == 0:
        print(t("none"))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
