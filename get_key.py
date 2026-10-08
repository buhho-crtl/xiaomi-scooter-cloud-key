#!/usr/bin/env python3
"""Saca de tu cuenta de Xiaomi la clave Bluetooth de tu patinete.

Inicia sesión en Xiaomi, busca los patinetes de tu cuenta en todas las regiones y pide la clave de
cada uno. Lo que imprime (64 caracteres) es lo que se pega en la app, junto con el PIN que le
pusiste al patinete en Mi Home.

    python get_key.py              # inicio de sesión con enlace: la contraseña la escribes en xiaomi.com
    python get_key.py --password   # usuario y contraseña en la terminal (captcha y código por correo)
    python get_key.py --server de  # mirar solo una región (más rápido)

Solo habla con los servidores de Xiaomi. No guarda nada en disco ni envía nada a terceros.
"""

import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def _homes(connector, server):
    """Casas propias y compartidas de la cuenta en una región (lista vacía si no hay o falla)."""
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
    """Dispositivos de esa región cuyo modelo es un patinete."""
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
    """Devuelve (clave en hex, encrypt_type) o (None, motivo)."""
    url = connector.get_api_url(server) + "/share/askbluetoothkey"
    data = json.dumps({"type": "own", "did": str(did), "keyid": 0}, separators=(",", ":"))
    try:
        response = connector.execute_api_call_encrypted(url, {"data": data})
    except Exception as error:  # la red o la respuesta de Xiaomi pueden fallar de muchas formas
        return None, f"{type(error).__name__}: {error}"
    if not response or response.get("code") != 0 or "result" not in response:
        return None, f"respuesta de Xiaomi: {response}"
    result = response["result"]
    if not result.get("key"):
        return None, "la respuesta no trae clave"
    return result["key"], int(result.get("encrypt_type", 0))


def main() -> int:
    parser = argparse.ArgumentParser(description="Saca de tu cuenta de Xiaomi la clave Bluetooth de tu patinete.")
    parser.add_argument("--password", action="store_true",
                        help="iniciar sesión con usuario y contraseña en la terminal, en vez de con enlace")
    parser.add_argument("--server", help="mirar solo esta región (cn, de, us, ru, tw, sg, in, i2)")
    options = parser.parse_args()

    # token_extractor lee sus propios argumentos al importarse: se le deja la línea de órdenes vacía.
    sys.argv = [sys.argv[0]]
    sys.path.insert(0, HERE)
    import token_extractor as xiaomi

    if options.server and options.server not in xiaomi.SERVERS:
        print(f"Región desconocida: {options.server}. Valen: {', '.join(xiaomi.SERVERS)}")
        return 2

    if options.password:
        connector = xiaomi.PasswordXiaomiCloudConnector()
        print("Inicia sesión con tu cuenta de Xiaomi (la contraseña no se ve al escribir).\n")
    else:
        connector = xiaomi.QrCodeXiaomiCloudConnector()
        print("Abre el enlace que sale abajo («visit the following URL»), inicia sesión en la página de")
        print("Xiaomi y vuelve aquí: el programa sigue solo. También puedes escanear el QR con Mi Home.\n")

    if not connector.login():
        print("\nNo se pudo iniciar sesión.")
        return 1

    servers = [options.server] if options.server else xiaomi.SERVERS
    print("\nSesión iniciada. Buscando patinetes" + ("" if options.server else " en todas las regiones") + "…\n")

    total = 0
    for server in servers:
        for device in _scooters(connector, server):
            total += 1
            name = device.get("name", "(sin nombre)")
            print(f"Patinete: {name}")
            print(f"  modelo: {device.get('model')}   región: {server}   id: {device['did']}")
            key, detail = _bluetooth_key(connector, server, device["did"])
            if key is None:
                print(f"  No se pudo obtener la clave ({detail}).\n")
                continue
            print(f"\n  CLAVE: {key}\n")
            if detail != 1:
                print(f"  Aviso: tipo de clave {detail}, no el habitual (1, protegida con el PIN). Puede que la app no la acepte.")
            print("  Cópiala y pégala en la app, junto con el PIN que le pusiste al patinete en Mi Home.\n")

    if total == 0:
        print("No hay ningún patinete en esta cuenta. Comprueba que lo tienes añadido en Mi Home con esta")
        print("misma cuenta y que es tuyo (no compartido por otra persona).")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
