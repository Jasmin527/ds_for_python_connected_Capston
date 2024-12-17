import os
import hashlib
from PIL import Image, ImageEnhance

# 이미지 파일의 해시값을 계산하여 중복된 이미지를 감지하기 위한 함수
def get_image_hash(image_path):
    """
    이미지 파일의 해시값(MD5)을 계산하는 함수입니다.
    동일한 해시값을 가지는 이미지는 중복된 이미지로 간주합니다.
    
    Args:
        image_path (str): 이미지 파일의 경로
    
    Returns:
        str: 이미지 파일의 MD5 해시값
    """
    with open(image_path, "rb") as f:  # 이미지 파일을 바이너리 모드로 엽니다.
        return hashlib.md5(f.read()).hexdigest()  # 이미지 데이터를 읽고 MD5 해시값을 반환

# 중복 이미지 제거 및 중복된 이미지 개수와 목록 출력
def remove_duplicates_and_count(input_folder, output_folder):
    """
    중복된 이미지를 감지하여 제거하고, 중복이 아닌 이미지만 출력 폴더로 이동합니다.
    
    Args:
        input_folder (str): 입력 이미지 폴더 경로
        output_folder (str): 중복 제거 후 이미지를 저장할 폴더 경로
    """
    seen_hashes = set()  # 중복 여부를 확인하기 위해 해시값을 저장할 집합
    duplicates = []  # 중복된 이미지 파일 경로를 저장할 리스트

    # 입력 폴더의 모든 파일을 가져옵니다.
    files = [file for file in os.listdir(input_folder) if os.path.isfile(os.path.join(input_folder, file))]
    for file in files:
        input_path = os.path.join(input_folder, file)  # 각 파일의 전체 경로 생성
        img_hash = get_image_hash(input_path)  # 이미지 파일의 해시값 계산

        if img_hash in seen_hashes:  # 동일한 해시값이 이미 존재하면 중복으로 간주
            duplicates.append(input_path)
        else:
            seen_hashes.add(img_hash)  # 새로운 해시값은 집합에 추가
            output_path = os.path.join(output_folder, file)  # 중복이 아닌 파일의 출력 경로 설정
            os.makedirs(output_folder, exist_ok=True)  # 출력 폴더가 없으면 생성
            os.replace(input_path, output_path)  # 중복이 아닌 파일만 출력 폴더로 이동

    # 결과 출력
    print(f"중복된 이미지 개수: {len(duplicates)}개")
    if duplicates:
        print("중복된 이미지 목록:")
        for dup in duplicates:
            print(f"  - {dup}")

# 손상된 이미지 제거 및 손상된 이미지 개수와 목록 출력
def remove_corrupted_and_count(input_folder, output_folder):
    """
    손상된 이미지를 감지하여 제거하고, 유효한 이미지만 출력 폴더로 이동합니다.
    
    Args:
        input_folder (str): 입력 이미지 폴더 경로
        output_folder (str): 손상되지 않은 이미지를 저장할 폴더 경로
    """
    corrupted = []  # 손상된 이미지 파일 경로를 저장할 리스트
    
    # 입력 폴더의 모든 파일을 가져옵니다.
    files = [file for file in os.listdir(input_folder) if os.path.isfile(os.path.join(input_folder, file))]
    for file in files:
        input_path = os.path.join(input_folder, file)
        try:
            with Image.open(input_path) as img:  # 이미지 파일 열기
                img.verify()  # 이미지 유효성 검사 (이미지가 손상되지 않았는지 확인)
            output_path = os.path.join(output_folder, file)
            os.makedirs(output_folder, exist_ok=True)  # 출력 폴더가 없으면 생성
            os.replace(input_path, output_path)  # 유효한 파일만 이동
        except (IOError, SyntaxError):  # 이미지가 손상되었을 경우 예외 발생
            corrupted.append(input_path)

    # 결과 출력
    print(f"손상된 이미지 개수: {len(corrupted)}개")
    if corrupted:
        print("손상된 이미지 목록:")
        for cor in corrupted:
            print(f"  - {cor}")

# 폴더에 포함된 이미지 파일 개수를 계산
def count_images(folder_path):
    """
    지정된 폴더에 있는 이미지 파일 개수를 계산합니다.
    
    Args:
        folder_path (str): 이미지 폴더 경로
    """
    if not os.path.exists(folder_path):
        return

    # 파일 개수를 세고 출력
    file_count = len([file for file in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, file))])
    print(f"{folder_path} 폴더의 이미지 개수: {file_count}장")

# 이미지 크기를 지정된 크기로 변경
def resize_images(input_folder, output_folder, target_size=(224, 224)):
    """
    모든 이미지 파일의 크기를 지정된 크기로 변경합니다.
    
    Args:
        input_folder (str): 입력 이미지 폴더 경로
        output_folder (str): 크기 변경 후 이미지를 저장할 폴더 경로
        target_size (tuple): 변경할 이미지 크기 (width, height)
    """
    resized = 0  # 크기가 변경된 이미지 개수

    files = [file for file in os.listdir(input_folder) if os.path.isfile(os.path.join(input_folder, file))]
    for file in files:
        input_path = os.path.join(input_folder, file)
        try:
            with Image.open(input_path) as img:
                img = img.resize(target_size)  # 이미지 크기 변경
                output_path = os.path.join(output_folder, file)
                os.makedirs(output_folder, exist_ok=True)  # 출력 폴더 생성
                img.save(output_path)  # 변경된 이미지 저장
                resized += 1
        except IOError:  # 이미지 처리 중 오류 발생 시 건너뜀
            continue

    print(f"{resized}개의 이미지 크기 변경 완료.")

# 데이터 증강을 통해 다양한 이미지 생성
def augment_data(input_folder, output_folder):
    """
    데이터 증강을 수행하여 새로운 이미지 파일을 생성합니다.
    적용되는 증강 기법:
        - 90도 회전
        - 180도 회전
        - 밝기 향상

    Args:
        input_folder (str): 입력 이미지 폴더 경로
        output_folder (str): 증강된 이미지를 저장할 폴더 경로
    """
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
                    aug_img = aug_fn(img)  # 증강 기법 적용
                    new_file_name = f"{os.path.splitext(file)[0]}_{aug_name}.png"  # 새 파일명 생성
                    output_path = os.path.join(output_folder, new_file_name)
                    os.makedirs(output_folder, exist_ok=True)  # 출력 폴더 생성
                    aug_img.save(output_path)  # 증강된 이미지 저장
        except IOError:  # 이미지 처리 중 오류 발생 시 건너뜀
            continue

    print("데이터 증강 완료.")

# 이미지 크기가 최소 조건을 충족하지 않는 이미지를 제거
def filter_outliers(input_folder, output_folder, min_size=(50, 50)):
    """
    이미지 크기가 최소 조건보다 작은 이미지를 제거합니다.
    
    Args:
        input_folder (str): 입력 이미지 폴더 경로
        output_folder (str): 유효한 이미지를 저장할 폴더 경로
        min_size (tuple): 최소 허용 이미지 크기 (width, height)
    """
    removed = 0  # 제거된 이미지 개수

    files = [file for file in os.listdir(input_folder) if os.path.isfile(os.path.join(input_folder, file))]
    for file in files:
        input_path = os.path.join(input_folder, file)
        try:
            with Image.open(input_path) as img:
                if img.size[0] < min_size[0] or img.size[1] < min_size[1]:  # 최소 조건 검사
                    removed += 1
                else:
                    output_path = os.path.join(output_folder, file)
                    os.makedirs(output_folder, exist_ok=True)
                    img.save(output_path)  # 유효한 이미지 저장
        except IOError:  # 오류 발생 시 건너뜀
            continue

    print(f"이상치 {removed}개 제거 완료.")

# 데이터 전처리 전체 과정
def preprocess_data(input_folder, output_folder):
    """
    이미지 데이터 전처리 전체 파이프라인을 실행합니다.
    
    Args:
        input_folder (str): 입력 이미지 폴더 경로
        output_folder (str): 전처리된 이미지를 저장할 폴더 경로
    """
    working_folder = os.path.join(output_folder, "working")  # 중간 작업 폴더 설정

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
