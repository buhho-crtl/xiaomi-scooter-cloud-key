# Clave de Xiaomi para tu patinete

*[English below](#english)*

Los Xiaomi Electric Scooter 4 Pro (y otros de su generación) no dejan conectar a una app sin una
**clave** que Xiaomi guarda en tu cuenta. La app te la pide una sola vez, junto con el **PIN** que le
pusiste al patinete en Mi Home.

Esta guía sirve para sacar esa clave de tu propia cuenta.

## Qué necesitas

- El patinete añadido en **Mi Home** con tu cuenta de Xiaomi (tuyo, no compartido por otra persona).
- El **PIN** del patinete: el que configuraste en Mi Home.
- Cinco minutos.

## Opción A: desde el navegador, sin instalar nada

1. Abre el cuaderno [`clave_xiaomi.ipynb`](clave_xiaomi.ipynb) en Google Colab (hace falta una cuenta de Google).
2. Pulsa **Entorno de ejecución → Ejecutar todo**.
3. Aparecerá un enlace de Xiaomi («visit the following URL»). Ábrelo, inicia sesión **en la página de
   Xiaomi** y vuelve al cuaderno: sigue solo.
4. Copia los 64 caracteres que salen junto a `CLAVE:`.

El programa se ejecuta en una máquina de Google asociada a tu cuenta de Google, no en un servidor
nuestro, y se borra al cerrar el cuaderno.

## Opción B: en tu ordenador

Con Python 3.10 o posterior:

```bash
git clone <URL de este repositorio>
cd xiaomi-scooter-cloud-key
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt      # en Windows: .venv\Scripts\pip
.venv/bin/python get_key.py                    # en Windows: .venv\Scripts\python
```

Abre el enlace que aparece, inicia sesión en Xiaomi y copia la `CLAVE:`.

Si prefieres escribir usuario y contraseña en la terminal (admite captcha y código por correo):
`python get_key.py --password`. Si sabes tu región, `--server de` va más rápido.

## Pegarla en la app

1. Conecta con el patinete. La app dirá **«Este patinete necesita una clave»**.
2. Toca **Introducir clave y PIN**.
3. Pega la clave y escribe el PIN de Mi Home.
4. **Guardar y conectar**.

La clave se guarda cifrada en tu móvil. El PIN solo se usa para abrirla y no se guarda.

## Si no funciona

| Qué pasa | Qué hacer |
|---|---|
| «El patinete no ha aceptado la clave o el PIN» | Revisa el PIN. Si es el correcto, vuelve a sacar la clave: Xiaomi la cambia a veces (por ejemplo, al volver a vincular el patinete). |
| «No hay ningún patinete en esta cuenta» | Comprueba que lo añadiste en Mi Home con esta misma cuenta. |
| No conecta aunque la clave es buena | Cierra Mi Home en todos los móviles cercanos: el patinete solo admite una conexión a la vez. |
| No recuerdas el PIN | Restablece el patinete desde Mi Home y vuelve a vincularlo. Después saca la clave de nuevo. |

## Privacidad

- El programa solo habla con los servidores de Xiaomi (`account.xiaomi.com` y `*.api.io.mi.com`).
- Con el inicio de sesión por enlace, tu contraseña la escribes en la web de Xiaomi; el programa no la ve.
- No guarda nada en disco. La clave solo sale por pantalla.
- La clave sola no sirve: va cifrada con tu PIN. Aun así, **no la publiques** ni la subas a un repositorio.

## Créditos y licencias

- `token_extractor.py` es de [Piotr Machowski](https://github.com/PiotrMachowski/Xiaomi-cloud-tokens-extractor)
  (MIT), en la versión incluida en [mehesbalazs/xiaomi-scooter-4-pro-2](https://github.com/mehesbalazs/xiaomi-scooter-4-pro-2).
- La llamada que devuelve la clave (`/share/askbluetoothkey`) sale de ese mismo proyecto (MIT).

Las licencias originales están en [`LICENSES/`](LICENSES/). Este proyecto no está afiliado a Xiaomi.

---

<a name="english"></a>

# Xiaomi key for your scooter

Xiaomi Electric Scooter 4 Pro (and others of its generation) only accept an app that knows a **key**
Xiaomi keeps in your account. The app asks for it once, together with the **PIN** you set for the
scooter in Mi Home. This guide gets that key out of your own account.

**You need:** the scooter added in Mi Home with your Xiaomi account (owned, not shared), and its PIN.

**In the browser, nothing to install:** open [`clave_xiaomi.ipynb`](clave_xiaomi.ipynb) in Google
Colab, choose *Runtime → Run all*, open the Xiaomi link it prints, sign in on Xiaomi's page, come
back and copy the 64 characters next to `CLAVE:`.

**On your computer** (Python 3.10+):

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python get_key.py          # add --password to type credentials in the terminal
```

**In the app:** connect to the scooter, tap *Enter key and PIN*, paste the key, type the Mi Home PIN,
*Save and connect*.

**If the scooter rejects it:** check the PIN; if it is right, fetch the key again (Xiaomi rotates it,
for instance after re-linking the scooter). Close Mi Home on nearby phones: the scooter takes one
connection at a time.

The tool only talks to Xiaomi's servers and stores nothing. Do not publish your key.
