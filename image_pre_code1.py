import os
import hashlib
from PIL import Image, ImageEnhance
from collections import defaultdict


def get_image_hash(image_path):
    """이미지 파일의 해시 생성."""
    with open(image_path, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()


def remove_duplicates(folder_path):
    """중복 이미지 제거."""
    seen_hashes = set()
    duplicates = 0

    for root, _, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            img_hash = get_image_hash(file_path)

            if img_hash in seen_hashes:
                os.remove(file_path)
                duplicates += 1
            else:
                seen_hashes.add(img_hash)
    print(f"중복 이미지 {duplicates}개 제거 완료.")


def remove_corrupted_files(folder_path):
    """손상된 이미지 제거."""
    corrupted = 0

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


def count_classes(folder_path):
    """클래스별 데이터 개수 확인."""
    counts = defaultdict(int)

    for root, _, files in os.walk(folder_path):
        for file in files:
            label = os.path.basename(root)
            counts[label] += 1
    print("클래스별 이미지 개수:")
    for label, count in counts.items():
        print(f"{label}: {count}장")


def resize_images(folder_path, target_size=(224, 224)):
    """이미지 크기 정규화."""
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


def augment_data(folder_path):
    """데이터 증강."""
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


def add_metadata(folder_path):
    """메타데이터 추가."""
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


def filter_outliers(folder_path, min_size=(50, 50)):
    """이상치 제거."""
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


def preprocess_data(folder_path):
    """전체 전처리 워크플로."""
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


# 실행
if __name__ == "__main__":
    # 전처리할 폴더 경로 지정
    folder_paths = ["bedbug_correct_scholar", "bedbug_incorrect_scholar"]

    for folder in folder_paths:
        print(f"{folder} 폴더 전처리 시작...")
        preprocess_data(folder)
        print(f"{folder} 폴더 전처리 완료.\n")