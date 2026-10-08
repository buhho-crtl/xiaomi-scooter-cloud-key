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

[![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/buhho-crtl/xiaomi-scooter-cloud-key/blob/main/clave_xiaomi.ipynb)

**Qué es Google Colab.** Es una web gratuita de Google que ejecuta programas de Python en un
ordenador suyo y te enseña el resultado en una página. Un «cuaderno» es esa página: texto con
instrucciones y unas cajas grises con el programa. No instalas nada y funciona igual desde un móvil.
Solo necesitas una cuenta de Google (la de Gmail vale); no tiene que ser la misma que la de Xiaomi.

Paso a paso:

1. **Abre el cuaderno** con el botón «Open in Colab» de arriba. Si Colab te lo pide, inicia sesión
   con tu cuenta de Google (botón **Acceder**, arriba a la derecha).
2. **Ejecútalo.** En el menú de arriba: **Entorno de ejecución → Ejecutar todo** (en inglés,
   *Runtime → Run all*). En el móvil el menú está en el icono **☰**.
3. **Acepta el aviso.** Colab avisa de que el cuaderno no lo ha escrito Google: es lo normal con
   cualquier cuaderno de GitHub. Pulsa **Ejecutar de todos modos**. El programa es
   [`get_key.py`](get_key.py), son cien líneas y puedes leerlo antes.
4. **Espera medio minuto.** La primera caja descarga este repositorio y lo que necesita. Mientras
   trabaja, el botón de la caja gira; cuando acaba, sale una marca verde.
5. **Inicia sesión en Xiaomi.** Debajo de la segunda caja aparecerá un texto como este:

   ```
   Alternatively you can visit the following URL:
     https://account.xiaomi.com/...
   ```

   Abre ese enlace (se abre en otra pestaña), entra con la cuenta de Xiaomi que usas en Mi Home y
   acepta. No hace falta copiar nada de vuelta: deja la pestaña de Colab abierta y el programa
   continúa solo en unos segundos. El enlace caduca a los pocos minutos; si se te pasa, vuelve a
   ejecutar.

   Ignora la línea `QR code URL: http://127.0.0.1:31415`: esa dirección solo sirve cuando el
   programa corre en tu propio ordenador.
6. **Copia la clave.** Al terminar verás algo así:

   ```
   Patinete: Mi Scooter
     modelo: xiaomi.scooter.…   región: de   id: 123456789

     CLAVE: 3f9a…(64 letras y números)…c21e
   ```

   Copia los 64 caracteres que van después de `CLAVE:`, sin espacios. Si tienes varios patinetes,
   sale una clave por cada uno.
7. **Cierra la pestaña.** Ya puedes [pegar la clave en la app](#pegarla-en-la-app).

Buscar en todas las regiones tarda uno o dos minutos; es normal que parezca parado.

**Dónde se ejecuta.** En una máquina de Google asociada a tu cuenta de Google, no en un servidor
nuestro. Tu contraseña de Xiaomi la escribes en la página de Xiaomi, no en el cuaderno. La máquina
se borra al cerrar la pestaña y la clave no se guarda en ningún sitio.

## Opción B: en tu ordenador

Con Python 3.10 o posterior:

```bash
git clone https://github.com/buhho-crtl/xiaomi-scooter-cloud-key.git
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

**In the browser, nothing to install:** Google Colab is a free Google site that runs Python programs
on one of their machines and shows the output in a page (a "notebook"); you only need a Google
account. [Open the notebook in Colab](https://colab.research.google.com/github/buhho-crtl/xiaomi-scooter-cloud-key/blob/main/clave_xiaomi.ipynb),
choose *Runtime → Run all* and accept the "not authored by Google" warning (*Run anyway*). After
about half a minute it prints *visit the following URL*: open that Xiaomi link, sign in on Xiaomi's
page and leave the Colab tab open; it carries on by itself. Copy the 64 characters next to `CLAVE:`
and close the tab. Ignore the `QR code URL: http://127.0.0.1:31415` line; it only works when
running on your own computer.

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
