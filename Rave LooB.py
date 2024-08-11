from base64 import b64encode
from hashlib import sha256
from hmac import new
from time import time
from uuid import uuid4
from json import JSONDecodeError, dumps
from requests import get as _get, post as _post, delete as _delete, put as _put

"""
Jailbreak Rave App Version 4.3 

- Kratos |	Saudi flag flying 🇸🇦

- Light Xc |	The flag of the Kingdom of Saudi Arabia is flying 🇸🇦
"""
SECRET_KEY = "c3ab8ff13720e8ad9047dd39466b3c8974e592c2fa383d4a3960714caef0c4f2".encode()

def nonce() -> str:
    return str(uuid4())

def gen_dev_id() -> str:
   return str(uuid4()).replace("-", "")

def ts() -> str:
    return str(int(time() * 1000))

def req_hash(ts, sess_id, content_len):
    msg = f"{ts}:{sess_id}:{content_len}"
    mac = new(SECRET_KEY, msg.encode(), sha256).digest()
    return b64encode(mac).decode()

# Headers
TOKEN = None
FIREBASE_TOKEN = None

class Hdrs:
    def __init__(self, body: dict = None, **kwargs):
        api_ver = kwargs.get("api_ver")
        cli_ver = kwargs.get("cli_ver")
        ts_val = ts()

        self.hdrs = {
            "client-version": cli_ver if cli_ver else "5.5.9",
            "request-hash": req_hash(ts_val, TOKEN, len(body) if body else 0),
            "request-ts": str(ts_val),
            "wemesh-api-version": api_ver if api_ver else "4.0",
            "wemesh-platform": "android",
            "content-type": "application/json; charset=UTF-8",
            "Host": "api.red.wemesh.ca",
            "user-agent": "Rave/1450 (5.5.9) (Android 9; SM-J701F; samsung j7velte; en)",
            "accept-encoding": "gzip, deflate"
        }

        self.mojo = {
            "x-api-key": "45af6a2e-4c1c-45a5-9874-df1eb3a22fe2"
        }

        self.soboro = {
            "x-parse-app-build-version": "1450",
            "x-parse-app-display-version": "5.5.9",
            "x-parse-application-id": "83a03c48-0f97-4f01-8a80-f603ea2a2270",
            "x-parse-installation-id": "67f181a4-6714-4859-a1f1-02cb8c3541d1",
            "x-parse-os-version": "9",
            "content-type": "application/json"
        }

        if TOKEN:
            self.hdrs["authorization"] = f"Bearer {TOKEN}"

# Service
class Svc:
    def __init__(self, proxies: dict = None):
        self.api = "https://api.red.wemesh.ca{}".format
        self.mojo_api = "https://api.mojoauth.com{}".format
        self.proxies = proxies
        self.dev_id = None
        self.sess_id = None

    def _compose(self, response):
        try:
            return response.json()
        except JSONDecodeError:
            print(response.text)
            return {}

    def _mojo_post(self, path: str, data: dict = None, params: dict = None) -> dict:
        response = _post(self.mojo_api(path), data=dumps(data), params=params, headers=Hdrs().mojo, proxies=self.proxies)
        return self._compose(response)

    def _mojo_get(self, path: str, params: dict = None) -> dict:
        response = _get(self.mojo_api(path), params=params, headers=Hdrs().mojo, proxies=self.proxies)
        return self._compose(response)

    def _post(self, path: str, data: dict = None, params: dict = None) -> dict:
        response = _post(self.api(path), data=dumps(data), params=params, headers=Hdrs(data).hdrs, proxies=self.proxies)
        return self._compose(response)

    def _get(self, path: str, params: dict = None) -> dict:
        response = _get(self.api(path), params=params, headers=Hdrs().hdrs, proxies=self.proxies)
        return self._compose(response)
    
    def _del(self, path: str, params: dict = None) -> dict:
        response = _delete(self.api(path), params=params, headers=Hdrs().hdrs, proxies=self.proxies)
        return self._compose(response)

    def _put(self, path: str, data: dict = None) -> dict:
        response = _put(self.api(path), data=data, headers=Hdrs(data).hdrs, proxies=self.proxies)
        return self._compose(response)

# Client
class Clnt(Svc):
    def __init__(self, proxies: dict = None):
        super().__init__(proxies)
        self.dev_id = gen_dev_id()

    def req_verif(self, email: str, lang: str = "en"):
        params = {"language": lang, "redirect_url": "https://rave.watch/mojoauth"}
        return self._mojo_post("/users/magiclink", {"email": email}, params)["state_id"]

    def mojo_status(self, state_id: str):
        return self._mojo_get("/users/status", params={"state_id": state_id})

    def soborol_login(self, email: str, mojo_id_token: str):
        data = {
            "authData": {
                "mojo": {
                    "id_token": mojo_id_token,
                    "id": email
                }
            }
        }
        return self._post("https://api.soborol.com/parse/users", data, headers=Hdrs().soboro)
    
    def login(self, email, password, **kwargs):
        # Implement login
        Hdrs.token = None
        self.token = Hdrs.token
        return self.get("/users/self")

    def login_token(self, token, **kwargs):
        Hdrs.token = token
        self.token = Hdrs.token
        return self.get("/users/self")

    def chk_usr(self, username: str):
        return self._post(f"/users/self/handle", {"handle": username})

    def acct_info(self):
        return self._get("/users/self")

    def usr_info(self, user_id: str):
        return self._get(f"/users/{user_id}")

    def edit_prof(self, name: str = None, handle: str = None, avatar: str = None):
        data = {}
        if name:
            data["displayName"] = name
        if handle:
            data["handel"] = handle
        if avatar:
            data["displayAvatar"] = avatar

        return self._put("/users/self", dumps(data))

    def del_disp(self, avatar: bool = False, name: bool = False):
        return self._del("/users/self/display", {"displayName": name, "displayAvatar": avatar})

    def push_notif(self, friends_only: bool = False):
        return self._post("/users/self/notification_prefs", {"friendsOnly": friends_only})

    def hide_loc(self, hide: bool = True):
        return self._post("/users/self/location", {"hideLocation": hide})

    def hide_mature(self, hide: bool = False):
        return self._post("/users/self/maturity", {"hideMature": hide})

    def set_dob(self, date: str = None):
        return self._post("/users/self/dob", {"date": date})

    def get_avatar_url(self):
        return self._post("/users/self/avatar/upload", {"mime":"image/jpeg"})

    def add_frnd(self, user_id: str):
        return self._post("/friendships", {"id": user_id})

    def rem_frnd(self, user_id: str):
        return self._del("/friendships/unfriend", {"id": user_id})
    
    def get_frnd_reqs(self):
        return self._get("/friendships/requests", {"state": "pendingactionable"})
    
    def accept_frnd(self, user_id: str):
        return self._post("/friendships", {"state": "accepted", "user_id": user_id})

    def decline_frnd(self, user_id: str):
        return self._del("/friendships", {"user_id": user_id})
