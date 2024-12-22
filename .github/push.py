import requests
from datetime import datetime
import os
import sys
import json

file_path = sys.argv[1]

udc_webhook = os.environ["UDC_WEBHOOK"]
udc_vanilla_webhook = os.environ["UDC_VANILLA_WEBHOOK"]
vic_webhook = os.environ["VIC_WEBHOOK"]
vic_vanilla_webhook = os.environ["VIC_VANILLA_WEBHOOK"]


def parse_device():
    with open(file_path) as f:
        codename = f.name.split("/")[-1].split(".")[0]
        data = json.load(f)
        response = data["response"]
        filename = response[0]["filename"]
        oem = response[0]["oem"]
        device = response[0]["device"]
        maintainer = response[0]["maintainer"]
        version = response[0]["version"]
        build_date = response[0]["timestamp"]
        file_size = response[0]["size"]
        download_link = response[0]["download"]
        xda_thread = response[0]["forum"]
        github = response[0]["github"]
    return filename, codename, oem, device, maintainer, version, build_date, file_size, download_link, xda_thread, github


def humanize(num, suffix='B'):
    for unit in ['', 'K', 'M', 'G', 'T', 'P', 'E', 'Z']:
        if abs(num) < 1024.0:
            return f"{num:3.1f}{unit}{suffix}"
        num /= 1024.0
    return f"{num:.1f}Yi{suffix}"


def webhook_send():
    filename, codename, oem, device, maintainer, version, build_date, file_size, download_link, xda_thread, github = parse_device()

    if "Vanilla" in filename and "10." in version:
        webhook_url = vic_vanilla_webhook
    if "Vanilla" in filename and "9." in version:
        webhook_url = udc_vanilla_webhook
    if "Vanilla" not in filename and "10." in version:
        webhook_url = vic_webhook
    if "Vanilla" not in filename and "9." in version:
        webhook_url = udc_webhook

    if xda_thread != "null":
        pass
    else:
        xda_thread = "https://evolution-x.org"
    if "Vanilla" in filename:
        color = 0xffe7c4
    else:
        color = 0x2986cc
    data = {
        "embeds": [
    {
            "type": "rich",
            "description": f"""
            📲 • New build available for **{oem} {device}** ({codename})
            👤 • **By [{maintainer}](https://github.com/{github})**\n
            📦 • **Version**: {version}
            🕒 • **Build date**: {datetime.fromtimestamp(build_date, tz=None).date()}
            📎 • **Build size**: {humanize(file_size)}
            <:Evo:670530693985730570> • **Check [device's infos](https://evolution-x.org/downloads/{codename}) directly on our website!**\n
            
            ⬇️ [Download link]({download_link}) ⬇️\n 
            🌐 [XDA Thread]({xda_thread}) 🌐
            """,
            "image": {
                "url": "https://wiki.evolution-x.org/keepevolving.png"
            },
            "color": f"{color}",
            "thumbnail": {
                "url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS7DK6a--HvqADA_u3mGjXSVUvxxZ5sw3x9Sw&s"
                },
            "author": {
                "name": f"New build available !",
                "icon_url": f"https://github.com/{github}.png"
                },
            "timestamp": datetime.now().isoformat(),
            "footer": {
                "text": "Evolution X",
                "icon_url": "https://avatars.githubusercontent.com/u/165590896?s=200&v=4"
            }}]
    }

    result = requests.post(webhook_url, json=data)

    try:
        result.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)
    else:
        print("Payload delivered successfully, code {}.".format(result.status_code))


webhook_send()
