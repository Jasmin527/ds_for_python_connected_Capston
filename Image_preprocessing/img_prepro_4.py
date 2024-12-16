import os
import hashlib
from PIL import Image, ImageEnhance

# 이미지 파일의 해시값을 계산하여 중복된 이미지를 감지하기 위한 함수
def get_image_hash(image_path):
    # 이미지 파일을 읽고 MD5 해시값을 반환
    with open(image_path, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()

# 중복 이미지 제거 및 중복된 이미지 개수와 목록 출력
def remove_duplicates_and_count(input_folder, output_folder):
    seen_hashes = set()  # 중복 확인을 위한 해시값 저장
    duplicates = []  # 중복된 파일 경로 저장

    # 입력 폴더의 모든 파일 목록
    files = [file for file in os.listdir(input_folder) if os.path.isfile(os.path.join(input_folder, file))]
    for file in files:
        input_path = os.path.join(input_folder, file)
        img_hash = get_image_hash(input_path)  # 이미지의 해시값 계산

        if img_hash in seen_hashes:  # 해시값이 이미 존재하면 중복으로 간주
            duplicates.append(input_path)
        else:
            seen_hashes.add(img_hash)  # 새로운 해시값 저장
            output_path = os.path.join(output_folder, file)
            os.makedirs(output_folder, exist_ok=True)  # 출력 폴더 생성
            os.replace(input_path, output_path)  # 중복이 아닌 파일 이동

    # 중복된 이미지 결과 출력
    print(f"중복된 이미지 개수: {len(duplicates)}개")
    if duplicates:
        print("중복된 이미지 목록:")
        for dup in duplicates:
            print(f"  - {dup}")

# 손상된 이미지 제거 및 손상된 이미지 개수와 목록 출력
def remove_corrupted_and_count(input_folder, output_folder):
    corrupted = []  # 손상된 파일 경로 저장
    files = [file for file in os.listdir(input_folder) if os.path.isfile(os.path.join(input_folder, file))]
    for file in files:
        input_path = os.path.join(input_folder, file)
        try:
            with Image.open(input_path) as img:
                img.verify()  # 이미지 유효성 확인
            output_path = os.path.join(output_folder, file)
            os.makedirs(output_folder, exist_ok=True)  # 출력 폴더 생성
            os.replace(input_path, output_path)  # 손상되지 않은 파일 이동
        except (IOError, SyntaxError):  # 손상된 경우 예외 처리
            corrupted.append(input_path)

    # 손상된 이미지 결과 출력
    print(f"손상된 이미지 개수: {len(corrupted)}개")
    if corrupted:
        print("손상된 이미지 목록:")
        for cor in corrupted:
            print(f"  - {cor}")

# 폴더에 포함된 이미지 파일 개수를 계산
def count_images(folder_path):
    if not os.path.exists(folder_path):
        return

    file_count = len([file for file in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, file))])
    print(f"{folder_path} 폴더의 이미지 개수: {file_count}장")

# 이미지 크기를 지정된 크기로 변경
def resize_images(input_folder, output_folder, target_size=(224, 224)):
    resized = 0  # 크기 변경된 이미지 수
    files = [file for file in os.listdir(input_folder) if os.path.isfile(os.path.join(input_folder, file))]
    for file in files:
        input_path = os.path.join(input_folder, file)
        try:
            with Image.open(input_path) as img:
                img = img.resize(target_size)  # 이미지 크기 변경
                output_path = os.path.join(output_folder, file)
                os.makedirs(output_folder, exist_ok=True)  # 출력 폴더 생성
                img.save(output_path)
                resized += 1
        except IOError:  # 오류 발생 시 건너뜀
            continue

    # 결과 출력
    print(f"{resized}개의 이미지 크기 변경 완료.")

# 데이터 증강을 통해 다양한 이미지 생성
def augment_data(input_folder, output_folder):
    augmentations = {
        "rotate_90": lambda img: img.rotate(90),  # 90도 회전
        "rotate_180": lambda img: img.rotate(180),  # 180도 회전
        "enhance_brightness": lambda img: ImageEnhance.Brightness(img).enhance(1.5)  # 밝기 향상
    }

    files = [file for file in os.listdir(input_folder) if os.path.isfile(os.path.join(input_folder, file))]
    for file in files:
        input_path = os.path.join(input_folder, file)
        try:
            with Image.open(input_path) as img:
                for aug_name, aug_fn in augmentations.items():
                    aug_img = aug_fn(img)  # 증강 수행
                    new_file_name = f"{os.path.splitext(file)[0]}_{aug_name}.png"  # 새 파일 이름
                    output_path = os.path.join(output_folder, new_file_name)
                    os.makedirs(output_folder, exist_ok=True)  # 출력 폴더 생성
                    aug_img.save(output_path)
        except IOError:  # 오류 발생 시 건너뜀
            continue

    # 결과 출력
    print("데이터 증강 완료.")

# 이미지 크기가 최소 조건을 충족하지 않는 이미지를 제거
def filter_outliers(input_folder, output_folder, min_size=(50, 50)):
    removed = 0  # 제거된 이미지 수
    files = [file for file in os.listdir(input_folder) if os.path.isfile(os.path.join(input_folder, file))]
    for file in files:
        input_path = os.path.join(input_folder, file)
        try:
            with Image.open(input_path) as img:
                # 이미지 크기가 최소 조건을 충족하지 않으면 제거
                if img.size[0] < min_size[0] or img.size[1] < min_size[1]:
                    removed += 1
                else:
                    output_path = os.path.join(output_folder, file)
                    os.makedirs(output_folder, exist_ok=True)  # 출력 폴더 생성
                    img.save(output_path)
        except IOError:  # 오류 발생 시 건너뜀
            continue

    # 결과 출력
    print(f"이상치 {removed}개 제거 완료.")

# 데이터 전처리 전체 과정
def preprocess_data(input_folder, output_folder):
    working_folder = os.path.join(output_folder, "working")  # 임시 작업 폴더

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

# 메인 실행 부분
if __name__ == "__main__":
    input_folders = [
        "bedbug_correct_scholar",  # 전처리할 첫 번째 폴더
        "bedbug_incorrect_scholar"  # 전처리할 두 번째 폴더
    ]

    output_folders = [
        "bedbug_correct",  # 첫 번째 결과 폴더
        "bedbug_incorrect"  # 두 번째 결과 폴더
    ]

    # 각 입력 폴더에 대해 전처리 수행
    for input_folder, output_folder in zip(input_folders, output_folders):
        print(f"'{input_folder}' 폴더 전처리 시작...")
        os.makedirs(output_folder, exist_ok=True)  # 출력 폴더 생성
        preprocess_data(input_folder, output_folder)
        print(f"'{input_folder}' 폴더 전처리 완료. 결과는 '{output_folder}'에 저장되었습니다.\n")