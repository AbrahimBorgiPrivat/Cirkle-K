import os
import requests
import zipfile
from tqdm import tqdm
from utils.env import DATAFORDELER_USER, DATAFORDELER_PASSWORD
from utils.path_config import FILES_DIR

def get_api(LatestTotalForEntity: str,
            register: str = "DAR",
            type: str = "current"):
    params = {
        "Register": register,
        "LatestTotalForEntity": LatestTotalForEntity,
        "type": type,
        "format": 'JSON',
        "username": DATAFORDELER_USER,
        "password": DATAFORDELER_PASSWORD,
    }
    return requests.get(f"https://api.datafordeler.dk/FileDownloads/GetFile",
                 params=params, 
                 stream=True)

def download_and_unzip(LatestTotalForEntity: str,
                       register: str,
                       type: str, 
                       save_directory: str):
    try:
        os.makedirs(save_directory, exist_ok=True)
        zip_filename = f"{register}_{LatestTotalForEntity}_{type}"
        zip_path = os.path.join(save_directory, zip_filename)
        response = get_api(LatestTotalForEntity=LatestTotalForEntity,
                           register=register,
                           type=type)
        response.raise_for_status()
        with open(zip_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(save_directory)
            extracted_files = zip_ref.namelist()
        os.remove(zip_path)
        renamed_json_files = []
        json_index = 1
        for extracted_file in extracted_files:
            extracted_path = os.path.join(save_directory, extracted_file)
            if extracted_file.endswith(".json"):
                new_json_filename = f"{register}_{LatestTotalForEntity}_{json_index}.json"
                new_json_path = os.path.join(save_directory, new_json_filename)
                if os.path.exists(new_json_path):
                    os.remove(new_json_path)
                os.rename(extracted_path, new_json_path)
                renamed_json_files.append(new_json_path)
                json_index += 1
        if renamed_json_files:
            return renamed_json_files  
    except requests.exceptions.RequestException as e:
        print(f"Download error: {e}")
    except zipfile.BadZipFile:
        print("Error: The downloaded file is not a valid ZIP file.")
    except Exception as e:
        print(f"Unexpected error: {e}")
    return None

def download_files(output_dir: str):
    file_dict = [ {'LatestTotalForEntity': 'Husnummer', 'register': 'DAR', 'type': 'current'},
                  {'LatestTotalForEntity': 'Adresse', 'register': 'DAR', 'type': 'current'},
                  {'LatestTotalForEntity': 'Adressepunkt', 'register': 'DAR', 'type': 'current'},
                  {'LatestTotalForEntity': 'NavngivenVej', 'register': 'DAR', 'type': 'current'},
                  {'LatestTotalForEntity': 'Postnummer', 'register': 'DAR', 'type': 'current'},
                  {'LatestTotalForEntity': 'Kommuneinddeling', 'register': 'DAGI', 'type': 'current'},
                  {'LatestTotalForEntity': 'Landsdel', 'register': 'DAGI', 'type': 'current'},
                  {'LatestTotalForEntity': 'Postnummerinddeling', 'register': 'DAGI', 'type': 'current'},
                  {'LatestTotalForEntity': 'Regionsinddeling', 'register': 'DAGI', 'type': 'current'},
                  {'LatestTotalForEntity': 'Storkreds', 'register': 'DAGI', 'type': 'current'},
                ]
    Number_of_tables = len(file_dict)
    for filename in tqdm(file_dict):
        download_and_unzip(LatestTotalForEntity=filename['LatestTotalForEntity'],
                            register=filename['register'],
                            type=filename['type'],
                            save_directory=os.path.join(output_dir, "json"))    
    return Number_of_tables

def main(output_dir: str = FILES_DIR):
    return download_files(output_dir)

if __name__ == "__main__":
    main()
 