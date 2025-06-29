import json
import os

# 파일 경로
normal_path = "/home/sanghyeok/openvla/outputs/summary/EVAL-libero_10-openvla-2025_05_12-00_10_41.json"
dola_path   = "/home/sanghyeok/openvla/outputs/summary/EVAL-libero_10-openvla-2025_05_14-00_21_56-dola.json"

# JSON 로드
with open(normal_path, "r") as f:
    normal_stats = json.load(f)

with open(dola_path, "r") as f:
    dola_stats = json.load(f)

# task들만 꺼내기 (만약 "tasks" 필드가 없다면 파일 전체를 사용)
normal_tasks = normal_stats.get("tasks", normal_stats)
dola_tasks   = dola_stats.get("tasks", dola_stats)

# 결과 저장 구조 (리스트로 초기화)
result = {
    "normal": [],
    "dola": [],
    "equal": []
}

# 비교
for task, n in normal_tasks.items():
    # 정상적으로 dict인지 확인
    if not isinstance(n, dict):
        continue

    s_n = n.get("successes", 0)

    d_entry = dola_tasks.get(task, {})
    s_d = d_entry.get("successes", 0) if isinstance(d_entry, dict) else 0

    if s_n > s_d:
        result["normal"].append(task)
    elif s_n < s_d:
        result["dola"].append(task)
    else:
        result["equal"].append(task)

# 출력 파일명 생성
base_name = os.path.splitext(os.path.basename(normal_path))[0]
output_path = f"/home/sanghyeok/openvla/outputs/summary/compare_{base_name}.json"

# 결과 저장
with open(output_path, "w") as f:
    json.dump(result, f, indent=4)

print(f"비교 결과를 '{output_path}'에 저장했습니다.")
