import os

UPLOAD_FOLDER = 'data_files'

def clear_uploads_directory():
    # Check if the directory exists
    if os.path.exists(UPLOAD_FOLDER):
        # Iterate over all files in the directory
        for filename in os.listdir(UPLOAD_FOLDER):
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            try:
                # Remove the file
                os.remove(file_path)
                print(f"Deleted file: {file_path}")
            except Exception as e:
                print(f"Failed to delete {file_path}. Reason: {e}")
    else:
        # If the directory does not exist, create it
        os.makedirs(UPLOAD_FOLDER)
        print(f"Created directory: {UPLOAD_FOLDER}")
