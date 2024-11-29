from PIL import Image
import os

def convert_png_to_jpg(input_path, output_path):
    """PNG 이미지를 JPG로 변환"""
    try:
        with Image.open(input_path) as img:
            rgb_img = img.convert('RGB')  # PNG는 알파 채널이 포함될 수 있음
            rgb_img.save(output_path, 'JPEG', quality=95)  # 품질 설정
            print(f"Converted: {input_path} to {output_path}")
    except Exception as e:
        print(f"Error converting {input_path}: {e}")

# PNG 파일 변환 예시
input_folder = "images/png/"
output_folder = "images/jpg/"

os.makedirs(output_folder, exist_ok=True)

for file_name in os.listdir(input_folder):
    if file_name.endswith(".png"):
        input_file = os.path.join(input_folder, file_name)
        output_file = os.path.join(output_folder, file_name.replace(".png", ".jpg"))
        convert_png_to_jpg(input_file, output_file)