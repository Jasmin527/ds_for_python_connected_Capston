import os
import hashlib
from PIL import Image, ImageEnhance

## 이미지 파일의 해시값 생성 ##
# 파일 내용 기반의 고유 해시값을 생성하여 중복 여부를 판별
def get_image_hash(image_path):
    with open(image_path, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()

## 중복된 이미지 제거 및 중복 개수 확인 ##
def remove_duplicates_and_count(folder_path):
    if not os.path.exists(folder_path):  # 경로가 존재하지 않으면 경고 없이 종료
        return

    seen_hashes = set()  # 중복 확인을 위한 해시값 저장소
    duplicates = []  # 중복 파일 저장소

    # 해당 폴더 내 모든 파일 탐색
    files = [file for file in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, file))]
    for file in files:
        file_path = os.path.join(folder_path, file)  # 파일 경로 생성
        img_hash = get_image_hash(file_path)  # 이미지 해시값 생성

        if img_hash in seen_hashes:
            duplicates.append(file_path)  # 중복된 파일 추가
            os.remove(file_path)  # 파일 삭제
        else:
            seen_hashes.add(img_hash)  # 새로운 해시값 저장

    # 결과 출력
    print(f"중복된 이미지 개수: {len(duplicates)}개")
    if duplicates:
        print("중복된 이미지 목록:")
        for dup in duplicates:
            print(f"  - {dup}")

## 손상된 이미지 제거 및 손상 개수 확인 ##
def remove_corrupted_and_count(folder_path):
    if not os.path.exists(folder_path):  # 경로가 존재하지 않으면 경고 없이 종료
        return

    corrupted = []  # 손상된 파일 저장소

    # 해당 폴더 내 모든 파일 탐색
    files = [file for file in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, file))]
    for file in files:
        file_path = os.path.join(folder_path, file)  # 파일 경로 생성
        try:
            with Image.open(file_path) as img:
                img.verify()  # 이미지 파일 유효성 검증
        except (IOError, SyntaxError):  # 오류 발생 시 손상된 파일로 간주
            corrupted.append(file_path)  # 손상된 파일 추가
            os.remove(file_path)  # 파일 삭제

    # 결과 출력
    print(f"손상된 이미지 개수: {len(corrupted)}개")
    if corrupted:
        print("손상된 이미지 목록:")
        for cor in corrupted:
            print(f"  - {cor}")

## 각 폴더의 이미지 개수 카운트 ##
def count_images(folder_path):
    if not os.path.exists(folder_path):  # 경로가 존재하지 않으면 경고 없이 종료
        return

    # 폴더 내 파일 개수 세기
    file_count = len([file for file in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, file))])

    # 결과 출력
    print(f"{folder_path} 폴더의 이미지 개수: {file_count}장")

## 모든 이미지 크기를 특정 크기로 정규화 ##
def resize_images(folder_path, target_size=(224, 224)):
    if not os.path.exists(folder_path):  # 경로가 존재하지 않으면 경고 없이 종료
        return

    resized = 0  # 크기 조정된 이미지 개수

    # 해당 폴더 내 모든 파일 탐색
    files = [file for file in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, file))]
    for file in files:
        file_path = os.path.join(folder_path, file)  # 파일 경로 생성
        try:
            with Image.open(file_path) as img:
                img = img.resize(target_size)  # 이미지 크기 조정
                img.save(file_path)  # 변경된 이미지 저장
                resized += 1
        except IOError:
            continue  # 이미지 파일 열기에 실패한 경우 건너뜀

    # 결과 출력
    print(f"{resized}개의 이미지 크기 변경 완료.")

## 데이터 증강(이미지 변환) ##
def augment_data(folder_path):
    if not os.path.exists(folder_path):  # 경로가 존재하지 않으면 경고 없이 종료
        return

    # 데이터 증강 함수들 정의
    augmentations = {
        "rotate_90": lambda img: img.rotate(90),  # 90도 회전
        "rotate_180": lambda img: img.rotate(180),  # 180도 회전
        "enhance_brightness": lambda img: ImageEnhance.Brightness(img).enhance(1.5)  # 밝기 증가
    }

    # 해당 폴더 내 모든 파일 탐색
    files = [file for file in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, file))]
    for file in files:
        file_path = os.path.join(folder_path, file)  # 파일 경로 생성
        try:
            with Image.open(file_path) as img:
                for aug_name, aug_fn in augmentations.items():
                    aug_img = aug_fn(img)  # 데이터 증강 적용
                    new_file_path = os.path.join(
                        folder_path, f"{os.path.splitext(file)[0]}_{aug_name}.png"
                    )
                    aug_img.save(new_file_path)  # 증강된 이미지 저장
        except IOError:
            continue  # 이미지 파일 열기에 실패한 경우 건너뜀

    # 결과 출력
    print("데이터 증강 완료.")

## 이상치 이미지 제거 ##
def filter_outliers(folder_path, min_size=(50, 50)):
    if not os.path.exists(folder_path):  # 경로가 존재하지 않으면 경고 없이 종료
        return

    removed = 0  # 제거된 이미지 개수

    # 해당 폴더 내 모든 파일 탐색
    files = [file for file in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, file))]
    for file in files:
        file_path = os.path.join(folder_path, file)  # 파일 경로 생성
        try:
            with Image.open(file_path) as img:
                # 최소 크기 조건을 만족하지 않는 경우 제거
                if img.size[0] < min_size[0] or img.size[1] < min_size[1]:
                    os.remove(file_path)
                    removed += 1
        except IOError:
            continue  # 이미지 파일 열기에 실패한 경우 건너뜀

    # 결과 출력
    print(f"이상치 {removed}개 제거 완료.")

## 전체 전처리 진행 ##
def preprocess_data(folder_path):
    print(f"\n'{folder_path}' 폴더 중복 제거 시작...")
    remove_duplicates_and_count(folder_path)

    print(f"\n'{folder_path}' 폴더 손상된 파일 제거 시작...")
    remove_corrupted_and_count(folder_path)

    print(f"\n'{folder_path}' 폴더 이미지 개수 확인...")
    count_images(folder_path)

    print(f"\n'{folder_path}' 폴더 이미지 크기 정규화 시작...")
    resize_images(folder_path)

    print(f"\n'{folder_path}' 폴더 데이터 증강 시작...")
    augment_data(folder_path)

    print(f"\n'{folder_path}' 폴더 이상치 제거 시작...")
    filter_outliers(folder_path)

## 메인 실행 ##
if __name__ == "__main__":
    # 절대 경로로 전처리할 폴더 경로 지정
    folder_paths = [
        "C:/Users/yeseo/PycharmProjects/ds_for_python_connected_Capston/bedbug_correct_scholar", #개인 경로로 변경 필요
        "C:/Users/yeseo/PycharmProjects/ds_for_python_connected_Capston/bedbug_incorrect_scholar" #개인 경로로 변경 필요
    ]

    # 각 폴더에 대해 전처리 실행
    for folder in folder_paths:
        print(f"'{folder}' 폴더 전처리 시작...")
        preprocess_data(folder)
        print(f"'{folder}' 폴더 전처리 완료.\n")