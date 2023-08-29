


# https://pdf-services-ue1.adobe.io/token

#   "client_id": "71d2c5ded07748889b86e68730b5780e",
#   "client_secret": "p8e-7zzsRzTT1Bb9XK1ASvKFsn_5uhETb5E9"


import requests
import time     

def create_access_token():
    url = "https://pdf-services-ue1.adobe.io/token"
    client_id = "71d2c5ded07748889b86e68730b5780e"
    client_secret = "p8e-7zzsRzTT1Bb9XK1ASvKFsn_5uhETb5E9"

    payload = {
        "client_id": client_id,
        "client_secret": client_secret
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    response = requests.post(url, data=payload, headers=headers)

    if response.status_code == 200:
        access_token = response.json().get("access_token")
        print("Access Token:", access_token)
        return access_token
    else:
        return None
    

# def create_access_token():
#     url = "https://pdf-services-ue1.adobe.io/token"
#     client_id = settings.CLIENT_ID
#     client_secret = settings.CLIENT_SECRET 

#     payload = {
#         "client_id": client_id,
#         "client_secret": client_secret
#     }

#     headers = {
#         "Content-Type": "application/x-www-form-urlencoded"
#     }

#     response = requests.post(url, data=payload, headers=headers)

#     if response.status_code == 200:
#         access_token = response.json().get("access_token")
#         return access_token
#     else:
#         return None


def upload_pdf_file(upload_uri, file_path):
    media_type = 'application/pdf'
    with open(file_path, "rb") as file:
        files = {"file": (file.name, file, media_type)}
        headers = {
            "Content-Type": "application/pdf",
        }
        response = requests.put(upload_uri, files=files, headers=headers)
        print(response)
        print(response.text)


def get_upload_presigned_uri(access_token, file_path):
    url = "https://pdf-services-ue1.adobe.io/assets"  

    headers = {
        "Authorization": "Bearer " + access_token,
        "x-api-key": "71d2c5ded07748889b86e68730b5780e",
    }

    payload = {
        "mediaType": 'application/pdf'
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        data = response.json()
        asset_id = data["assetID"]
        upload_uri = data["uploadUri"]
        media_type = "application/pdf"

        upload_pdf_file(upload_uri, file_path)
        return asset_id

    return None


def get_download_uri(access_token, assetId, client_id):
    url = f"https://pdf-services-ue1.adobe.io/assets/{assetId}"
    headers = {
        "Authorization": "Bearer " + access_token,
        "x-api-key": client_id,
        "x-request-id": "your-request-id"  
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        download_uri = data.get("downloadUri")
        size = data.get("size")
        resource_type = data.get("type")
        print("Download URI:", download_uri)
        print("Size:", size)
        print("Resource Type:", resource_type)
        return download_uri
    else:
        return None


def poll_export_pdf_job_status(access_token, client_id, url):
    headers = {
        "Authorization": "Bearer " + access_token,
        "x-api-key": client_id
    }

    while True:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            status = data.get("status")
            print("Job status:", status)

            if status == "done":
                asset_id = data['asset']['assetID']
                print(asset_id)
                return asset_id
            elif status == "failed":
                break
            else:
                time.sleep(5)
        else:
            print("Failed to poll job status.")
            break


def export_pdf_to_docx(access_token, client_id, asset_id):
    url = "https://pdf-services-ue1.adobe.io/operation/exportpdf"
    headers = {
        "Authorization": "Bearer " + access_token,
        "x-api-key": client_id
    }
    payload = {
        "assetID": asset_id,
        "targetFormat": "docx"
    }

    response = requests.post(url, headers=headers, json=payload)
    print(response)

    if response.status_code == 201:
        location = response.headers.get("location")
        print("Export job status URI:", location)

        status = poll_export_pdf_job_status(access_token, client_id, location)
        print(status)
        return location
    else:
        return None
    

def download_file(url, file_path):
    response = requests.get(url)
    if response.status_code == 200:
        with open(file_path, 'wb') as file:
            file.write(response.content)
        print("File downloaded successfully.")
    else:
        print("Failed to download the file.")



# access_token = create_access_token()
client_id = '71d2c5ded07748889b86e68730b5780e'
file_path = "output_result.pdf"


# out_url_id = get_upload_presigned_uri(access_token, file_path)
# print(out_url_id)

# down_url = get_download_uri(access_token, out_url_id, client_id)
# print(down_url)

# exported_doc_id = export_pdf_to_docx(access_token, client_id, 'urn:aaid:AS:UE1:46778fe4-82d0-400c-829b-86d4f9ef7109')
# print(exported_doc_id)


# exported_doc_url = get_download_uri(access_token, exported_doc_urlx, client_id)
# print(exported_doc_url)


# download_file(exported_doc_url, 'gg.docx')








