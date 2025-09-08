import requests
import base64

class CiscoPhoneController:
    def __init__(self, ip, user, password):
        self.ip = ip
        self.user = user
        self.password = password

    def _auth_header(self):
        creds = f"{self.user}:{self.password}"
        return {"Authorization": "Basic " + base64.b64encode(creds.encode()).decode()}

    def get_screen(self, file_path="phone_display.png"):
        url = f"http://{self.ip}/CGI/Screenshot"
        resp = requests.get(url, headers=self._auth_header(), timeout=10)
        if resp.status_code == 200:
            with open(file_path, "wb") as f:
                f.write(resp.content)
            return file_path
        raise Exception("Impossibile ottenere screenshot.")

    def send_button(self, button):
        from time import sleep
        # Mappatura semplice. Ampliare con i codici effettivi secondo la Phone XML API.
        cmds = {
            "1": "KeyPad1",
            "2": "KeyPad2",
            "3": "KeyPad3",
            "4": "KeyPad4",
            "5": "KeyPad5",
            "6": "KeyPad6",
            "7": "KeyPad7",
            "8": "KeyPad8",
            "9": "KeyPad9",
            "0": "KeyPad0",
            "*": "KeyPadStar",
            "#": "KeyPadPound",
            "Up": "NavUp",
            "Down": "NavDwn",
            "Left": "NavLeft",
            "Right": "NavRight",
            "Select": "NavSelect",
            "SoftKey1": "Soft1",
            "SoftKey2": "Soft2",
            "SoftKey3": "Soft3",
            "SoftKey4": "Soft4",
            "Settings": "Settings",
            "Directory": "Dir", # This probably doesn't work
            "Applications": "Applications"
        }
        value = cmds.get(button, button)
        url = f"http://{self.ip}/CGI/Execute"
        data = f"XML=<CiscoIPPhoneExecute><ExecuteItem URL='Key:{value}'/></CiscoIPPhoneExecute>"
        resp = requests.post(url, data=data, headers=self._auth_header(), timeout=10)
        sleep(2)
        if resp.status_code not in [200, 204]:
            print(f"Payload Sent: {resp.request.headers}\n{resp.request.body}")
            raise Exception(f"Comando non accettato: {resp.status_code} - {resp.text}")