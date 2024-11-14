import secrets
import json
import requests
from requests.auth import HTTPBasicAuth

def get_request(url, headers):
     response = requests.get(url, headers=headers)
     if response.status_code == 200:
          return response.text
     else:
          print(f"Error {response.status_code}: {response.text}")
          return None

def post_request(url, headers, data=None, auth=None):
     response = requests.post(url, headers=headers, json=data, auth=auth)
     if response.status_code == 200:
          return response.text
     else:
          print(f"Error {response.status_code}: {response.text}")
          return None
     
def authenticate_user(user, password):
    BASE_URL="https://hosted.mender.io/api/management/v1/useradm"
    API_ENDPOINT="/auth/login"
    url=BASE_URL+API_ENDPOINT

    headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'X-MEN-Signature': 'string'
    }

    jwt_temp = post_request(url, headers, auth=HTTPBasicAuth(user, password))
    return jwt_temp

def create_token(jwt_temp):
    BASE_URL="https://hosted.mender.io/api/management/v1/useradm"
    API_ENDPOINT="/settings/tokens"
    url=BASE_URL+API_ENDPOINT

    unique = secrets.token_hex(5)

    headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'Authorization': f'Bearer {jwt_temp}'
    }

    body = {
    "name": f"demo-pat-{unique}",
    "expires_in": 7200
    }

    jwt = post_request(url, headers, body)
    return jwt

def get_list_devices(jwt):
    BASE_URL="https://hosted.mender.io/api/management/v2/devauth"
    API_ENDPOINT="/devices"
    url=BASE_URL+API_ENDPOINT

    headers = {
        'Accept': 'application/json',
        'Authorization': f'Bearer {jwt}'
    }

    devices = get_request(url, headers)
    return devices

def get_device_inventory(jwt, device_mac):
    BASE_URL="https://hosted.mender.io/api/management/v2/devauth"
    API_ENDPOINT=f"/devices/{device_mac}"
    url=BASE_URL+API_ENDPOINT

    headers = {
        'Accept': 'application/json',
        'Authorization': f'Bearer {jwt}'
    }

    device_inventory = get_request(url, headers)
    return device_inventory

def menu(jwt):
    print("Mender Menu\nOption: ")
    option = ""

    while option != "3":
        print("[1] Get list devices")
        print("[2] Get device inventory")
        print("[3] Exit")

        option = input()

        if option == "1":
            devices = get_list_devices(jwt)
            if not devices:
                print ("Error al obtener los dispositivos")
            else:
                print(devices)

        if option == "2":
            print("Device mac: ")
            device_mac = input()
            device_inventory = get_device_inventory(jwt, device_mac)
            if not device_inventory:
                print ("Error al obtener los inventarios")
            else:
                print(device_inventory)
        
        if option == "3":
            return


def main(user, password):
    # Paso 1: Autenticación del usuario
    jwt_temp = authenticate_user(user, password)
    if not jwt_temp:
        print ("Error al autenticar el usuario")
        return
     
    # Paso 2: Creación de token
    jwt = create_token(jwt_temp)
    if not jwt:
        print ("Error al crear el token")
        return
     
    # Paso 3: Opciones
    menu(jwt)

if __name__ == "__main__":
    user="your@email.com"
    password="yourStrongPass"
    main(user, password)



