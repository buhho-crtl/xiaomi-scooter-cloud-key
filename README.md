# Xiaomi key for your scooter

*[Instrucciones en castellano más abajo](#castellano)*

Xiaomi Electric Scooter 4 Pro (and others of its generation) will not let an app connect without a
**key** that Xiaomi keeps in your account. The app asks for it once, together with the **PIN** you
set for the scooter in Mi Home.

This guide gets that key out of your own account.

## What you need

- The scooter added in **Mi Home** with your Xiaomi account (yours, not shared by someone else).
- The scooter's **PIN**: the one you set in Mi Home.
- Five minutes.

## Option A: in the browser, nothing to install

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/buhho-crtl/xiaomi-scooter-cloud-key/blob/main/clave_xiaomi.ipynb)

**What Google Colab is.** A free Google site that runs Python programs on one of their computers
and shows you the result in a page. A "notebook" is that page: text with instructions and a few
grey boxes with the program. You install nothing and it works the same from a phone. You only need
a Google account (a Gmail one will do); it does not have to be the same as your Xiaomi one.

> **Sign in to Xiaomi first.** Before you start, open <https://account.xiaomi.com> in your browser
> and sign in with the account you use in Mi Home. If you open the program's link without being
> signed in already, Xiaomi answers "Invalid request" or "QR code has expired".

Step by step:

1. **Open the notebook** with the "Open in Colab" button above. If Colab asks, sign in with your
   Google account (**Sign in** button, top right).
2. **Run it.** In the top menu: **Runtime → Run all**. On a phone the menu is under the **☰** icon.
3. **Accept the warning.** Colab warns that the notebook was not authored by Google: that is normal
   for any notebook from GitHub. Press **Run anyway**. The program is [`get_key.py`](get_key.py), a
   short file you can read first.
4. **Wait half a minute.** The first box downloads this repository and what it needs. While it
   works, the button of the box spins; when it is done, a green tick shows up.
5. **Open Xiaomi's link.** Under the second box a text like this will appear:

   ```
   1. First sign in to Xiaomi in your browser: https://account.xiaomi.com
      (if you open the link below without being signed in, Xiaomi answers
      "Invalid request").

   2. Then open this link in that same browser:

     https://eu.account.xiaomi.com/longPolling/login?ticket=...

   3. Come back here: the program carries on by itself.
   ```

   If you have not signed in to Xiaomi yet, do it now at <https://account.xiaomi.com>. Then open
   the link in that same browser and accept. There is nothing to copy back: leave the Colab tab open
   and the program carries on by itself in a few seconds. The link is valid once and for five
   minutes; if you miss it, run again.
6. **Copy the key.** When it finishes you will see something like this:

   ```
   Scooter: Mi Scooter
     model: xiaomi.scooter.…   region: de   id: 123456789

     KEY: 3f9a…(64 letters and digits)…c21e
   ```

   Copy the 64 characters after `KEY:`, without spaces. If you have several scooters, there is one
   key for each.
7. **Close the tab.** You can now [paste the key into the app](#paste-it-into-the-app).

Looking in every region takes a minute or two; it is normal for it to look stuck.

**Where it runs.** On a Google machine tied to your Google account, not on a server of ours. You
type your Xiaomi password on Xiaomi's page, not in the notebook. The machine is wiped when you
close the tab and the key is not stored anywhere.

## Option B: on your computer

With Python 3.10 or later:

```bash
git clone https://github.com/buhho-crtl/xiaomi-scooter-cloud-key.git
cd xiaomi-scooter-cloud-key
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt      # on Windows: .venv\Scripts\pip
.venv/bin/python get_key.py                    # on Windows: .venv\Scripts\python
```

Sign in at <https://account.xiaomi.com> first, then open the link that shows up in that same browser
and copy the `KEY:`. The terminal also draws a QR of that same link, in case you prefer to use a
phone where you are already signed in to Xiaomi.

If you prefer to type user and password in the terminal (it handles captcha and e-mail code):
`python get_key.py --password`. If you know your region, `--server de` is faster.

## Paste it into the app

1. Connect to the scooter. The app will say **"This scooter needs a key"**.
2. Tap **Enter key and PIN**.
3. Paste the key and type the Mi Home PIN.
4. **Save and connect**.

The key is stored encrypted on your phone. The PIN is only used to unlock it and is not stored.

## If it does not work

| What happens | What to do |
|---|---|
| Xiaomi's page says "Invalid request" or "QR code has expired" | Sign in at <https://account.xiaomi.com> first, then run again and open the new link in that same browser. Each link is valid once and for five minutes. |
| "The scooter did not accept the key or the PIN" | Check the PIN. If it is right, get the key again: Xiaomi changes it sometimes (for instance, after linking the scooter again). |
| "There is no scooter in this account" | Check that you added it in Mi Home with this same account. |
| It does not connect although the key is good | Close Mi Home on every nearby phone: the scooter takes one connection at a time. |
| You do not remember the PIN | Reset the scooter from Mi Home and link it again. Then get the key again. |

## Privacy

- The program only talks to Xiaomi's servers (`account.xiaomi.com` and `*.api.io.mi.com`).
- With the link sign-in, you type your password on Xiaomi's site; the program does not see it.
- It stores nothing on disk. The key is only shown on screen.
- The key is useless on its own: it is encrypted with your PIN. Even so, **do not publish it** or
  push it to a repository.

## Credits and licences

- `token_extractor.py` is by [Piotr Machowski](https://github.com/PiotrMachowski/Xiaomi-cloud-tokens-extractor)
  (MIT), in the version included in [mehesbalazs/xiaomi-scooter-4-pro-2](https://github.com/mehesbalazs/xiaomi-scooter-4-pro-2).
- The call that returns the key (`/share/askbluetoothkey`) comes from that same project (MIT).

The original licences are in [`LICENSES/`](LICENSES/). This project is not affiliated with Xiaomi.

---

<a name="castellano"></a>

# Clave de Xiaomi para tu patinete

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

> **Inicia sesión en Xiaomi antes.** Antes de empezar, abre <https://account.xiaomi.com> en tu
> navegador y entra con la cuenta que usas en Mi Home. Si abres el enlace del programa sin haber
> iniciado sesión ya, Xiaomi contesta «Invalid request» o «QR code has expired».

Paso a paso:

1. **Abre el cuaderno** con el botón «Open in Colab» de arriba. Si Colab te lo pide, inicia sesión
   con tu cuenta de Google (botón **Acceder**, arriba a la derecha).
2. **Ejecútalo.** Si quieres los mensajes en castellano, elige `es` en el desplegable `LANG` de la
   primera caja (por defecto salen en inglés). Después, en el menú de arriba: **Entorno de
   ejecución → Ejecutar todo** (en inglés, *Runtime → Run all*). En el móvil el menú está en el
   icono **☰**.
3. **Acepta el aviso.** Colab avisa de que el cuaderno no lo ha escrito Google: es lo normal con
   cualquier cuaderno de GitHub. Pulsa **Ejecutar de todos modos**. El programa es
   [`get_key.py`](get_key.py), un fichero corto que puedes leer antes.
4. **Espera medio minuto.** La primera caja descarga este repositorio y lo que necesita. Mientras
   trabaja, el botón de la caja gira; cuando acaba, sale una marca verde.
5. **Abre el enlace de Xiaomi.** Debajo de la segunda caja aparecerá un texto como este:

   ```
   1. Primero inicia sesión en Xiaomi en tu navegador: https://account.xiaomi.com
      (si abres el enlace de abajo sin haber iniciado sesión, Xiaomi contesta
      «Invalid request»).

   2. Después abre este enlace en ese mismo navegador:

     https://eu.account.xiaomi.com/longPolling/login?ticket=...

   3. Vuelve aquí: el programa sigue solo.
   ```

   Si aún no has iniciado sesión en Xiaomi, hazlo ahora en <https://account.xiaomi.com>. Después
   abre el enlace en ese mismo navegador y acepta. No hace falta copiar nada de vuelta: deja la
   pestaña de Colab abierta y el programa continúa solo en unos segundos. El enlace vale una vez y
   durante cinco minutos; si se te pasa, vuelve a ejecutar.
6. **Copia la clave.** Al terminar verás algo así (en inglés pone `KEY:` en vez de `CLAVE:`):

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
.venv/bin/python get_key.py --lang es          # en Windows: .venv\Scripts\python
```

Inicia sesión antes en <https://account.xiaomi.com>, abre el enlace que aparece en ese mismo
navegador y copia la `CLAVE:`. En la terminal sale también un QR de ese mismo enlace, por si
prefieres usar un móvil donde ya tengas la sesión de Xiaomi abierta. Sin `--lang es` los mensajes
salen en inglés.

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
| La página de Xiaomi dice «Invalid request» o «QR code has expired» | Inicia sesión antes en <https://account.xiaomi.com>, ejecuta otra vez y abre el enlace nuevo en ese mismo navegador. Cada enlace vale una vez y durante cinco minutos. |
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
