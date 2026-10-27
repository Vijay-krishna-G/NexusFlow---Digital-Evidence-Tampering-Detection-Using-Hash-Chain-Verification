import hashlib

def calculate_hash(file_path):
    sha = hashlib.sha256()
    with open(file_path, 'rb') as f:
        while chunk := f.read(4096):
            sha.update(chunk)
    return sha.hexdigest()


def verify_chain(evidence_files):
    previous_hash = None
    for file in evidence_files.order_by('uploaded_at'):
        current_hash = calculate_hash(file.file.path)
        if file.hash_value != current_hash or file.previous_hash != previous_hash:
            return False, file.file.name
        previous_hash = file.hash_value
    return True, None