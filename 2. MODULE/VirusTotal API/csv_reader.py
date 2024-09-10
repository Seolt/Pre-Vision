import csv

def read_hashes_from_csv(csv_file):
    """CSV 파일에서 해시 값을 읽어온다."""
    with open(csv_file, 'r', encoding='ISO-8859-1') as file:
        reader = csv.DictReader(file)
        hashes = [row['md5_hash'].strip() for row in reader] # CSV에서 'md5_hash' 열 읽기
    return hashes
