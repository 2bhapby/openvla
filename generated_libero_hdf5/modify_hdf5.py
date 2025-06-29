import h5py
import os
import shutil

def restructure_hdf5_to_data_group(src_path, dst_path):
    """
    src_path: 기존 HDF5 경로 (demo_0, demo_1 ... 이 최상위에 존재)
    dst_path: 새롭게 저장할 HDF5 경로 (data/demo_0 ... 형태로 정리됨)
    """
    # 임시 디렉토리 확인 및 생성
    os.makedirs(os.path.dirname(dst_path), exist_ok=True)

    with h5py.File(src_path, 'r') as src_file, h5py.File(dst_path, 'w') as dst_file:
        data_group = dst_file.create_group("data")
        for key in src_file.keys():
            if not key.startswith("demo_"):
                print(f"[!] 무시됨: {key}")
                continue
            print(f"[+] 복사 중: {key} → data/{key}")
            src_file.copy(key, data_group)

    print(f"[✓] 저장 완료: {dst_path}")


# 예시 실행
if __name__ == "__main__":
    for file in os.listdir("/home/sanghyeok/openvla/generated_libero_hdf5/0627"):
        if file.endswith(".hdf5"):
            src_path = os.path.join("/home/sanghyeok/openvla/generated_libero_hdf5/0627", file)
            dst_path = os.path.join("/home/sanghyeok/openvla/generated_libero_hdf5/0627_modi", f"{file}")
            restructure_hdf5_to_data_group(src_path, dst_path)
