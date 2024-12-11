import os
import hashlib
from PIL import Image, ImageEnhance

def get_image_hash(image_path):
    with open(image_path, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()

def remove_duplicates_and_count(input_folder, output_folder):
    seen_hashes = set()
    duplicates = []

    files = [file for file in os.listdir(input_folder) if os.path.isfile(os.path.join(input_folder, file))]
    for file in files:
        input_path = os.path.join(input_folder, file)
        img_hash = get_image_hash(input_path)

        if img_hash in seen_hashes:
            duplicates.append(input_path)
        else:
            seen_hashes.add(img_hash)
            output_path = os.path.join(output_folder, file)
            os.makedirs(output_folder, exist_ok=True)
            os.replace(input_path, output_path)

    print(f"중복된 이미지 개수: {len(duplicates)}개")
    if duplicates:
        print("중복된 이미지 목록:")
        for dup in duplicates:
            print(f"  - {dup}")

def remove_corrupted_and_count(input_folder, output_folder):
    corrupted = []
    files = [file for file in os.listdir(input_folder) if os.path.isfile(os.path.join(input_folder, file))]
    for file in files:
        input_path = os.path.join(input_folder, file)
        try:
            with Image.open(input_path) as img:
                img.verify()
            output_path = os.path.join(output_folder, file)
            os.makedirs(output_folder, exist_ok=True)
            os.replace(input_path, output_path)
        except (IOError, SyntaxError):
            corrupted.append(input_path)

    print(f"손상된 이미지 개수: {len(corrupted)}개")
    if corrupted:
        print("손상된 이미지 목록:")
        for cor in corrupted:
            print(f"  - {cor}")

def count_images(folder_path):
    if not os.path.exists(folder_path):
        return

    file_count = len([file for file in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, file))])
    print(f"{folder_path} 폴더의 이미지 개수: {file_count}장")

def resize_images(input_folder, output_folder, target_size=(224, 224)):
    resized = 0
    files = [file for file in os.listdir(input_folder) if os.path.isfile(os.path.join(input_folder, file))]
    for file in files:
        input_path = os.path.join(input_folder, file)
        try:
            with Image.open(input_path) as img:
                img = img.resize(target_size)
                output_path = os.path.join(output_folder, file)
                os.makedirs(output_folder, exist_ok=True)
                img.save(output_path)
                resized += 1
        except IOError:
            continue

    print(f"{resized}개의 이미지 크기 변경 완료.")

def augment_data(input_folder, output_folder):
    augmentations = {
        "rotate_90": lambda img: img.rotate(90),
        "rotate_180": lambda img: img.rotate(180),
        "enhance_brightness": lambda img: ImageEnhance.Brightness(img).enhance(1.5)
    }

    files = [file for file in os.listdir(input_folder) if os.path.isfile(os.path.join(input_folder, file))]
    for file in files:
        input_path = os.path.join(input_folder, file)
        try:
            with Image.open(input_path) as img:
                for aug_name, aug_fn in augmentations.items():
                    aug_img = aug_fn(img)
                    new_file_name = f"{os.path.splitext(file)[0]}_{aug_name}.png"
                    output_path = os.path.join(output_folder, new_file_name)
                    os.makedirs(output_folder, exist_ok=True)
                    aug_img.save(output_path)
        except IOError:
            continue

    print("데이터 증강 완료.")

def filter_outliers(input_folder, output_folder, min_size=(50, 50)):
    removed = 0
    files = [file for file in os.listdir(input_folder) if os.path.isfile(os.path.join(input_folder, file))]
    for file in files:
        input_path = os.path.join(input_folder, file)
        try:
            with Image.open(input_path) as img:
                if img.size[0] < min_size[0] or img.size[1] < min_size[1]:
                    removed += 1
                else:
                    output_path = os.path.join(output_folder, file)
                    os.makedirs(output_folder, exist_ok=True)
                    img.save(output_path)
        except IOError:
            continue

    print(f"이상치 {removed}개 제거 완료.")

def preprocess_data(input_folder, output_folder):
    working_folder = os.path.join(output_folder, "working")

    print(f"\n'{input_folder}' 폴더 중복 제거 시작...")
    remove_duplicates_and_count(input_folder, working_folder)

    print(f"\n'{working_folder}' 폴더 손상된 파일 제거 시작...")
    remove_corrupted_and_count(working_folder, working_folder)

    print(f"\n'{working_folder}' 폴더 이미지 개수 확인...")
    count_images(working_folder)

    print(f"\n'{working_folder}' 폴더 이미지 크기 정규화 시작...")
    resize_images(working_folder, working_folder)

    print(f"\n'{working_folder}' 폴더 데이터 증강 시작...")
    augment_data(working_folder, output_folder)

    print(f"\n'{working_folder}' 폴더 이상치 제거 시작...")
    filter_outliers(working_folder, output_folder)

if __name__ == "__main__":
    input_folders = [
        "bedbug_correct_scholar",
        "bedbug_incorrect_scholar"
    ]

    output_folders = [
        "bedbug_correct",
        "bedbug_incorrect"
    ]

    for input_folder, output_folder in zip(input_folders, output_folders):
        print(f"'{input_folder}' 폴더 전처리 시작...")
        os.makedirs(output_folder, exist_ok=True)
        preprocess_data(input_folder, output_folder)
        print(f"'{input_folder}' 폴더 전처리 완료. 결과는 '{output_folder}'에 저장되었습니다.\n")