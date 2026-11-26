"""PyPython server calls and dialogs: talks to the JSON API (/api/...) and drives the two HTML dialogs
(username prompt and "Is this you?"). Runs in the browser (Pyodide)."""
import asyncio
import json

from js import document
from pyodide.ffi import create_proxy
from pyodide.http import pyfetch


async def api(path, method="GET", body=None):
    try:
        kwargs = {"method": method}
        if body is not None:
            kwargs.update(headers={"Content-Type": "application/json"}, body=json.dumps(body))
        resp = await pyfetch("/api/" + path, **kwargs)
        try:
            data = await resp.json()
        except Exception:
            data = {}
        return resp.ok, data
    except Exception:
        return False, {"error": "Could not reach the server."}


class Dialogs:
    """The two HTML dialogs (username prompt, 'is this you?'), driven entirely from Python."""
    def __init__(self):
        el = document.getElementById
        self.login, self.form, self.name, self.err, self.cancel = (
            el("login-dlg"), el("login-form"), el("name"), el("err"), el("login-cancel"))
        self.confirm, self.confirm_text, self.yes, self.no = (
            el("confirm-dlg"), el("confirm-text"), el("yes"), el("no"))
        self.fut, self.allow_cancel = None, False
        self.form.addEventListener("submit", create_proxy(self._submit))
        self.cancel.addEventListener("click", create_proxy(self._cancel))
        self.login.addEventListener("cancel", create_proxy(self._cancel))            # Esc key
        self.yes.addEventListener("click", create_proxy(lambda e: self._resolve(True)))
        self.no.addEventListener("click", create_proxy(lambda e: self._resolve(False)))
        self.confirm.addEventListener("cancel", create_proxy(self._decline))         # Esc key

    def _resolve(self, value):
        if self.fut and not self.fut.done():
            self.fut.set_result(value)

    def _submit(self, e):
        e.preventDefault()
        self._resolve(str(self.name.value).strip())

    def _cancel(self, e):
        e.preventDefault()
        if self.allow_cancel:
            self._resolve(None)

    def _decline(self, e):
        e.preventDefault()
        self._resolve(False)

    async def ask_name(self, allow_cancel, msg=""):
        """Returns the typed name, or None if the player cancelled."""
        self.allow_cancel = allow_cancel
        self.err.textContent = msg
        self.cancel.hidden = not allow_cancel
        self.name.value = ""
        self.fut = asyncio.get_running_loop().create_future()
        self.login.showModal()
        self.name.focus()
        try:
            return await self.fut
        finally:
            if self.login.open:
                self.login.close()

    async def confirm_user(self, name, high_score):
        self.confirm_text.textContent = f"Welcome back, {name}!\nPrevious High Score: {high_score}\n\nIs this you?"
        self.fut = asyncio.get_running_loop().create_future()
        self.confirm.showModal()
        self.yes.focus()
        try:
            return await self.fut
        finally:
            if self.confirm.open:
                self.confirm.close()
