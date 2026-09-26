import os
import shutil

def clear_folder(folder_path):
    """
    Remove all files from a folder.
    
    Args:
        folder_path: Path to folder to clear
    """
    
    if not os.path.exists(folder_path):
        return
    
    try:
        for file in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file)
            
            if os.path.isfile(file_path):
                os.remove(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
    
    except Exception as e:
        print(f"Error clearing folder {folder_path}: {e}")


def remove_folder(folder_path):
    """
    Completely remove a folder and all its contents.
    
    Args:
        folder_path: Path to folder to remove
    """
    
    if not os.path.exists(folder_path):
        return
    
    try:
        shutil.rmtree(folder_path)
        print(f"Removed folder: {folder_path}")
    except Exception as e:
        print(f"Error removing folder {folder_path}: {e}")


def cleanup_all():
    """
    Clean up all temporary folders used by the application.
    """
    
    folders_to_clean = ["uploads", "frames", "audio"]
    
    for folder in folders_to_clean:
        clear_folder(folder)
        print(f"Cleaned: {folder}")


def get_folder_size(folder_path):
    """
    Get the total size of a folder in MB.
    
    Args:
        folder_path: Path to folder
    
    Returns:
        float: Size in MB
    """
    
    total_size = 0
    
    try:
        for dirpath, dirnames, filenames in os.walk(folder_path):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                total_size += os.path.getsize(filepath)
    except Exception as e:
        print(f"Error calculating folder size: {e}")
    
    return round(total_size / (1024 * 1024), 2)  # Convert to MB