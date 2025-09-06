import os, shutil

EXTENSION_MAP = {
    'PDFs':      ['.pdf'],
    'Images':    ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff'],
    'Videos':    ['.mp4', '.mov', '.avi', '.mkv', '.flv', '.wmv'],
    'Documents': ['.doc', '.docx', '.txt', '.xls', '.xlsx', '.ppt', '.pptx', '.odt'],
    'Zipped':    ['.zip', '.rar', '.7z', '.tar', '.gz'],
}

def get_folder(ext):
    for folder, exts in EXTENSION_MAP.items():
        if ext.lower() in exts:
            return folder
    return 'Others'

def organize_files(folder):
    files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
    moved = 0
    for name in files:
        ext = os.path.splitext(name)[1]
        dest = os.path.join(folder, get_folder(ext))
        os.makedirs(dest, exist_ok=True)
        shutil.move(os.path.join(folder, name), os.path.join(dest, name))
        moved += 1
    return moved, len(files)
