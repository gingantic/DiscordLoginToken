import requests
import os

if not os.path.exists("token.txt"): open("token.txt", 'w').close()

USER_AGENT = "Mozilla/5.0 (Linux; Android 10; Redmi Note 8 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Mobile Safari/537.36"
TOKEN = ""

def _login(email, 
           password):
    url = "https://discord.com/api/v9/auth/login"
    payload = {
        "login": email,
        "password": password,
        "undelete": False,
        "login_source": None,
        "gift_code_sku_id": None
    }
    headers = {
        "Content-Type": "application/json",
        "User-Agent": USER_AGENT,
    }
    r = requests.post(url, json=payload, headers=headers)
    return r.json()

def _2fa(code, 
         ticket):
    url = "https://discord.com/api/v9/auth/mfa/totp"
    payload = {
        "code": code,
        "ticket": ticket,
        "login_source": None,
        "gift_code_sku_id": None
    }
    headers = {
        "Content-Type": "application/json",
        "User-Agent": USER_AGENT,
    }
    r = requests.post(url, json=payload, headers=headers)
    return r.json()

def _write_token():
    with open("token.txt", "w") as f:
        f.write(TOKEN)

def _read_token():
    with open("token.txt", "r") as f:
        return f.read()

def _get_me():
    url = "https://discord.com/api/v9/users/@me"
    headers = {
        'Authorization': TOKEN,
        'User-Agent': USER_AGENT,
        'Content-Type': 'application/json'
    }
    r = requests.get(url, headers=headers)
    return r.json()

def login(email = None, 
          password = None):
    global TOKEN

    TOKEN = _read_token()
    try:
        if _get_me()["message"] == "401: Unauthorized":
            pass
    except KeyError:
        return TOKEN

    if email is None or password is None or email == "" or password == "":
        email = input("Masukkan Email atau Masukan Token: ")
        if "@" not in email:
            TOKEN = email
            _write_token()
            login()
        password = input("Masukkan Password: ")

    r = _login(email, password)
    if "ticket" in r:
        ticket = r["ticket"]
        code = input("Masukkan Kode 2FA: ")
        r = _2fa(code, ticket)
        if "token" in r:
            pass
        else:
            if "Invalid two-factor code" in str(r):
                raise Exception("Kode 2FA Salah!")
            elif "captcha-required" in str(r):
                raise Exception("Captcha Diperlukan!")
            else:
                raise Exception("Error Tidak Diketahui!\n"+r)
    elif "token" in r:
        pass
    else:
        if "password is invalid" in str(r):
            raise Exception("Email atau Password Salah!")
        elif "captcha-required" in str(r):
            raise Exception("Captcha Diperlukan!")
        else:
            raise Exception("Error Tidak Diketahui!\n"+r)
    
    TOKEN = r["token"]
    _write_token()
    return r["token"]

if __name__ == "__main__":
    token = login()
    getme = _get_me()
    print(f"Login Berhasil!\nUsername: {getme['username']}\nID: {getme['id']}")
    exit()