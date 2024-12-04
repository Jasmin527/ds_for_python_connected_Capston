import os
import hashlib
from PIL import Image, ImageEnhance
from collections import defaultdict

## 이미지 해시 생성 ##
# 이미지 파일의 고유 해시값 생성하여 중복을 식별하는 함수
def get_image_hash(image_path):
    with open(image_path, "rb") as f: # binary mode로 파일 open
        return hashlib.md5(f.read()).hexdigest() #MD5 해시값 생성 및 반환

## 중복되는 이미지 제거 ##
# 같은 해시값 가진 이미지 파일 찾아 제거
def remove_duplicates(folder_path):
    seen_hashes = set() #이미 처리된 해시값 저장
    duplicates = 0 #제거된 중복 이미지 개수

    for root, _, files in os.walk(folder_path): #폴더 내 모든 파일 탐색
        for file in files:
            file_path = os.path.join(root, file) # 파일의 전체 경로 생성
            img_hash = get_image_hash(file_path) # 이미지 해시값 생성

            if img_hash in seen_hashes: # 위에서 이미 본 해시값인지 확인
                os.remove(file_path) # 중복 이미지 파일 삭제
                duplicates += 1
            else:
                seen_hashes.add(img_hash) # 새로운 해시값 저장
    print(f"중복 이미지 {duplicates}개 제거 완료.") # 중복 제거 결과 출력

## 손상된 이미지 제거 ##
# 파일 유효성 검사에 실패한 손상된 이미지 삭제
def remove_corrupted_files(folder_path):
    corrupted = 0 # 제거된 손상된 이미지 개수

    for root, _, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                with Image.open(file_path) as img:
                    img.verify()  # 파일 유효성 검사
            except (IOError, SyntaxError):
                os.remove(file_path)
                corrupted += 1
    print(f"손상된 파일 {corrupted}개 제거 완료.")

## 이미지 폴더 별 개수 카운트 ##
def count_classes(folder_path):
    counts = defaultdict(int)

    for root, _, files in os.walk(folder_path):
        for file in files:
            label = os.path.basename(root)
            counts[label] += 1
    print("클래스별 이미지 개수:")
    for label, count in counts.items():
        print(f"{label}: {count}장")

## 이미지 크기 정규화 ##
def resize_images(folder_path, target_size=(224, 224)):
    resized = 0

    for root, _, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                with Image.open(file_path) as img:
                    img = img.resize(target_size)
                    img.save(file_path)
                    resized += 1
            except IOError:
                continue
    print(f"{resized}개의 이미지 크기 변경 완료.")

## 데이터 증강 ##
def augment_data(folder_path):
    augmentations = {"rotate_90": lambda img: img.rotate(90),
                     "rotate_180": lambda img: img.rotate(180),
                     "enhance_brightness": lambda img: ImageEnhance.Brightness(img).enhance(1.5)}

    for root, _, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                with Image.open(file_path) as img:
                    for aug_name, aug_fn in augmentations.items():
                        aug_img = aug_fn(img)
                        new_file_path = os.path.join(root, f"{os.path.splitext(file)[0]}_{aug_name}.png")
                        aug_img.save(new_file_path)
            except IOError:
                continue
    print("데이터 증강 완료.")

## 메타데이터 추가 ##
def add_metadata(folder_path):
    metadata = []

    for root, _, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                with Image.open(file_path) as img:
                    metadata.append({
                        "filename": file,
                        "size": img.size,
                        "format": img.format
                    })
            except IOError:
                continue

    for data in metadata:
        print(data)
    print("메타데이터 기록 완료.")

## 이상치 제거 ##
def filter_outliers(folder_path, min_size=(50, 50)):
    removed = 0

    for root, _, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                with Image.open(file_path) as img:
                    if img.size[0] < min_size[0] or img.size[1] < min_size[1]:
                        os.remove(file_path)
                        removed += 1
            except IOError:
                continue
    print(f"이상치 {removed}개 제거 완료.")

## 전체 전처리 진행 ##
def preprocess_data(folder_path):
    print("중복 제거 시작...")
    remove_duplicates(folder_path)

    print("손상된 파일 제거 시작...")
    remove_corrupted_files(folder_path)

    print("클래스 불균형 확인...")
    count_classes(folder_path)

    print("이미지 크기 정규화...")
    resize_images(folder_path)

    print("데이터 증강...")
    augment_data(folder_path)

    print("메타데이터 추가...")
    add_metadata(folder_path)

    print("이상치 제거...")
    filter_outliers(folder_path)

## 전체 실행 ##
# 실행
if __name__ == "__main__":
    # 전처리할 폴더 경로 지정
    folder_paths = ["bedbug_correct_scholar", "bedbug_incorrect_scholar"]

    for folder in folder_paths:
        print(f"{folder} 폴더 전처리 시작...")
        preprocess_data(folder)
        print(f"{folder} 폴더 전처리 완료.\n")
