import requests
import json

## Config env related
presigned_url_api = "https://portal.pedscommons.org/amanuensis/admin/upload-file"
s3_bucket = "pcdc-prod-data-release-bucket"
access_token = "YOUR_ACCESS_TOKEN"


## Config request related
# File to upload
project_id = 16
file_name = '20250115_INSTRuCT_2022-09.zip'
file_path = './outputs/' + file_name



payload = json.dumps({
  "bucket": s3_bucket,
  "key": file_name,
  "project_id": project_id
})
headers = {
  'Content-Type': 'application/json',
  'Authorization': "Bearer " + access_token
}

response = requests.request("POST", presigned_url_api, headers=headers, data=payload)
print(response.text)

# Use the pre-signed URL to upload the file from the amanuensis endpoint 
url = response.text
url = url[1:-2]
print(url)


with open(file_path, 'rb') as data:
    response = requests.put(url, data=data)

# Check if the file was uploaded successfully
if response.status_code == 200:
    print("File uploaded successfully.")
else:
    print(f"Failed to upload file. Status code: {response.status_code}")





