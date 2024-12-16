import os
import hashlib
from PIL import Image, ImageEnhance

## 이미지 파일의 해시값 생성 ##
# 파일 내용 기반의 고유 해시값을 생성하여 중복 여부를 판별
def get_image_hash(image_path):
    with open(image_path, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()  # 파일의 바이트 내용을 해시화하여 반환

# 중복된 이미지 제거 및 새 폴더에 저장
def remove_duplicates_and_save(folder_path, output_folder):
    if not os.path.exists(folder_path):
        return
    os.makedirs(output_folder, exist_ok=True)  # 결과를 저장할 폴더 생성

    seen_hashes = set()  # 중복 여부 확인을 위한 해시값 저장소
    duplicates = []  # 중복된 파일 경로를 저장할 리스트

    # 폴더 내 모든 파일 탐색
    files = [file for file in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, file))]
    for file in files:
        file_path = os.path.join(folder_path, file)  # 각 파일의 절대 경로 생성
        img_hash = get_image_hash(file_path)  # 이미지의 해시값 생성

        if img_hash in seen_hashes:
            duplicates.append(file_path)  # 중복된 파일 목록에 추가
        else:
            seen_hashes.add(img_hash)  # 새로운 해시값을 저장
            # 중복되지 않은 파일을 새 폴더로 이동
            new_path = os.path.join(output_folder, file)
            os.rename(file_path, new_path)

    print(f"중복된 이미지 개수: {len(duplicates)}개")
    if duplicates:
        print("중복된 이미지 목록:")
        for dup in duplicates:
            print(f"  - {dup}")

## 손상된 이미지 제거 및 새 폴더에 저장 ##
def remove_corrupted_and_save(folder_path, output_folder):
    if not os.path.exists(folder_path):
        return
    os.makedirs(output_folder, exist_ok=True)  # 결과를 저장할 폴더 생성

    corrupted = []  # 손상된 파일 경로를 저장할 리스트

    # 폴더 내 모든 파일 탐색
    files = [file for file in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, file))]
    for file in files:
        file_path = os.path.join(folder_path, file)  # 각 파일의 절대 경로 생성
        try:
            with Image.open(file_path) as img:
                img.verify()  # 이미지 유효성 확인
                # 유효한 이미지인 경우 결과 폴더에 저장
                new_path = os.path.join(output_folder, file)
                os.rename(file_path, new_path)
        except (IOError, SyntaxError):  # 오류가 발생하면 손상된 파일로 간주
            corrupted.append(file_path)

    print(f"손상된 이미지 개수: {len(corrupted)}개")
    if corrupted:
        print("손상된 이미지 목록:")
        for cor in corrupted:
            print(f"  - {cor}")

## 이미지 크기 정규화 후 저장 ##
def resize_and_save(folder_path, output_folder, target_size=(224, 224)):
    if not os.path.exists(folder_path):
        return
    os.makedirs(output_folder, exist_ok=True)  # 결과를 저장할 폴더 생성

    resized = 0  # 크기가 조정된 이미지 개수
    files = [file for file in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, file))]
    for file in files:
        file_path = os.path.join(folder_path, file)  # 각 파일의 절대 경로 생성
        try:
            with Image.open(file_path) as img:
                img = img.resize(target_size)  # 이미지 크기 조정
                new_path = os.path.join(output_folder, file)
                img.save(new_path)  # 결과를 새 폴더에 저장
                resized += 1
        except IOError:  # 이미지 파일 열기에 실패한 경우 건너뜀
            continue

    print(f"{resized}개의 이미지 크기 변경 완료.")

# ## 데이터 증강 후 저장 ##
# def augment_and_save(folder_path, output_folder):
#     if not os.path.exists(folder_path):
#         return
#     os.makedirs(output_folder, exist_ok=True)  # 결과를 저장할 폴더 생성
#
#     # 데이터 증강 함수 정의
#     augmentations = {
#         "rotate_90": lambda img: img.rotate(90),  # 90도 회전
#         "rotate_180": lambda img: img.rotate(180),  # 180도 회전
#         "enhance_brightness": lambda img: ImageEnhance.Brightness(img).enhance(1.5)  # 밝기 증가
#     }
#
#     # 폴더 내 모든 파일 탐색
#     files = [file for file in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, file))]
#     for file in files:
#         file_path = os.path.join(folder_path, file)  # 각 파일의 절대 경로 생성
#         try:
#             with Image.open(file_path) as img:
#                 for aug_name, aug_fn in augmentations.items():
#                     aug_img = aug_fn(img)  # 데이터 증강 함수 적용
#                     new_file_path = os.path.join(output_folder, f"{os.path.splitext(file)[0]}_{aug_name}.png")
#                     aug_img.save(new_file_path)  # 증강된 이미지 저장
#         except IOError:  # 이미지 파일 열기에 실패한 경우 건너뜀
#             continue
#
#     print("데이터 증강 완료.")

## 전체 전처리 및 결과 저장 ##
def preprocess_and_save(folder_path, output_base_folder):
    print(f"\n'{folder_path}' 폴더 전처리 시작...")
    output_folder = os.path.join(output_base_folder, os.path.basename(folder_path))  # 결과 저장 경로

    print("중복 제거 및 저장...")
    remove_duplicates_and_save(folder_path, output_folder)

    print("손상된 파일 제거 및 저장...")
    remove_corrupted_and_save(folder_path, output_folder)

    print("이미지 크기 정규화 및 저장...")
    resize_and_save(folder_path, output_folder)

    # print("데이터 증강 및 저장...")
    # augment_and_save(folder_path, output_folder)

    print(f"'{folder_path}' 폴더 전처리 완료.\n")

if __name__ == "__main__":
    # 전처리할 폴더 경로
    folder_paths = [
        "C:/Users/yeseo/PycharmProjects/ds_for_python_connected_Capston/bedbug_correct_scholar", # 개인 폴더로 변경 필요
        "C:/Users/yeseo/PycharmProjects/ds_for_python_connected_Capston/bedbug_incorrect_scholar" # 개인 폴더로 변경 필요
    ]
    output_base_folder = "C:/Users/yeseo/PycharmProjects/ds_for_python_connected_Capston/processed_images" # 개인 폴더로 변경 필요

    # 각 폴더에 대해 전처리 실행
    for folder in folder_paths:
        preprocess_and_save(folder, output_base_folder)