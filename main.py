import os
import shutil
import tempfile
import zipfile
from datetime import UTC, datetime

import boto3
import polars as pl
from botocore import UNSIGNED
from botocore.client import Config

from config import (
    PARQUERT_DIR,
    RAW_DATA_DIR,
    S3_BUCKET_NAME,
    S3_REGION_NAME,
    SCHEMAS,
    SUMMARY_FILES,
)

s3_client = boto3.client(
    "s3", region_name=S3_REGION_NAME, config=Config(signature_version=UNSIGNED)
)


def list_files_by_type(directory, file_type):
    """
    List full paths of all files with a specific extension in a given directory.

    Args:
        directory (str): The directory path to search
        file_type (str): File extension to search for (e.g. 'txt', 'pdf', 'csv')

    Returns:
        list: List of full paths to files with the specified extension
    """
    try:
        # Ensure file_type starts with a period
        extension = f".{file_type.lower().strip('.')}"

        matching_files = []
        for file in os.listdir(directory):
            if file.lower().endswith(extension):
                matching_files.append(os.path.join(directory, file))
        return matching_files
    except Exception as e:
        print(f"Error accessing directory: {str(e)}")
        return []


def save_in_parquet(input_path, schema, output_path):
    """
    Read a text file as CSV with specified columns and save as parquet.
    All columns are treated as strings.

    Args:
        input_path (str): Path to the input text file
        schema (dict): The SchemaDict
        output_path (str): Path where parquet file should be saved

    Returns:
        bool: True if conversion successful, False otherwise
    """
    try:
        # Read CSV file with specified columns
        df = pl.read_csv(
            source=input_path,
            schema=schema,
            has_header=False,
            separator="|",
            quote_char=None,
            truncate_ragged_lines=True,
        )

        # Save as parquet
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        df.write_parquet(output_path)
        return True

    except Exception as e:
        print(f"Error converting file: {str(e)}")
        return False


def get_s3_last_modified(bucket_name, object_key):
    """
    Get S3 object's LastModified timestamp
    """
    response = s3_client.head_object(Bucket=bucket_name, Key=object_key)
    return response["LastModified"]


def is_local_file_outdated(local_path, s3_last_modified):
    """
    Check if local file is older than S3 version or doesn't exist
    """
    if not os.path.exists(local_path):
        return True
    # Convert local timestamp to UTC timezone-aware datetime
    local_mtime = datetime.fromtimestamp(os.path.getmtime(local_path), tz=UTC)
    # Add a small buffer (1 second) to handle precision differences
    return (s3_last_modified - local_mtime).total_seconds() > 1


def download_s3_file(bucket, key, path):
    """
    Download a file from S3 bucket if it doesn't exist locally or is outdated
    """
    try:
        # Get S3 last modified time
        s3_last_modified = get_s3_last_modified(bucket, key)

        # Check if file needs updating
        if not is_local_file_outdated(path, s3_last_modified):
            print(f"Skipping {key} - local file is up to date")
            return True

        print(f"Downloading {key} to {path}")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        s3_client.download_file(bucket, key, path)

        # Update local file timestamp to match S3
        os.utime(path, (s3_last_modified.timestamp(), s3_last_modified.timestamp()))
        return True

    except Exception as e:
        print(f"Error downloading file: {e}")
        if os.path.exists(path):
            os.remove(path)
        return False


def extract_zip(zip_path: str, extract_dir: str) -> None:
    """
    Extract a ZIP file to the specified directory.
    Handles single-folder zips by moving contents to root of extract directory.

    Args:
        zip_path (str): Path to the ZIP file
        extract_dir (str): Directory to extract files to

    Raises:
        zipfile.BadZipFile: If the file is not a valid ZIP file
        ValueError: If malicious paths are detected in the ZIP
    """
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        # Check for malicious paths
        for zip_info in zip_ref.filelist:
            if os.path.isabs(zip_info.filename) or ".." in zip_info.filename:
                raise ValueError(f"Malicious path detected in ZIP: {zip_info.filename}")

        # Extract all files
        zip_ref.extractall(extract_dir)

    # Handle single-folder case
    contents = os.listdir(extract_dir)
    if len(contents) == 1 and os.path.isdir(os.path.join(extract_dir, contents[0])):
        root_folder = os.path.join(extract_dir, contents[0])
        # Move contents up one level
        for item in os.listdir(root_folder):
            shutil.move(
                os.path.join(root_folder, item), os.path.join(extract_dir, item)
            )
        # Remove the now-empty folder
        os.rmdir(root_folder)


def parse_statements_and_summary():
    for summary_file in SUMMARY_FILES:
        bucket = S3_BUCKET_NAME
        key = summary_file["key"]
        path = os.path.join(RAW_DATA_DIR, key)
        category = summary_file["category"]
        year = summary_file["year"]

        download_s3_file(bucket=bucket, key=key, path=path)

        try:
            temp_dir = tempfile.mkdtemp()
            extract_zip(path, temp_dir)
            txt_files = list_files_by_type(temp_dir, "txt")

            # Convert and save in Parquet
            schema = SCHEMAS[category]
            parquet_file = f"{PARQUERT_DIR}/{category}_{year}.parquet"
            save_in_parquet(txt_files[0], schema, parquet_file)
            print(f"Successfully save {parquet_file}")
        except Exception as e:
            print(f"Error parsing: {str(e)}")
            raise
        finally:
            shutil.rmtree(temp_dir)


def main():
    parse_statements_and_summary()


if __name__ == "__main__":
    main()
