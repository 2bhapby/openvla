import os

def log_to_summary(logs_path, summary_path):
    """
    훈련 로그를 요약 파일로 저장합니다.

    Args:
        logs_path (str): 훈련 로그 파일 경로입니다.
        summary_path (str): 저장할 요약 파일 경로입니다.
    """
    # summary_path의 디렉터리가 없으면 전부 생성
    os.makedirs(os.path.dirname(summary_path), exist_ok=True)

    with open(logs_path, 'r') as f_in, open(summary_path, 'w') as f_out:
        for line in f_in:
            # if "Episode" in line and "average get_action latency" in line:
            #     episode = line.split(" ")[1]
            #     f_out.write(f"Episode {episode}\n")
            # elif "Success:" in line:
            #     success = line.split(":")[-1].strip()
            #     f_out.write(f"Success: {success}\n")
            # elif "# episodes completed so far" in line:
            #     episodes_completed = line.split(":")[-1].strip()
            #     f_out.write(f"# episodes completed so far: {episodes_completed}\n")
            # elif "# successes" in line:
            #     successes = line.split(":")[-1].strip()
            #     f_out.write(f"# successes: {successes}\n")
            if "Task: " in line:
                f_out.write(line)
            elif "Current task success rate" in line:
                task_success_rate = line.split(":")[-1].strip()
                f_out.write(f"Current task success rate: {task_success_rate}\n")
            elif "Current total success rate" in line:
                total_success_rate = line.split(":")[-1].strip()
                f_out.write(f"Current total success rate: {total_success_rate}\n\n")
            elif "Episode" in line and "average get_action latency" in line:
                step = line.split(" ")[-2:]
                f_out.write(step[0] + " " + step[1])
            elif "# episodes completed so far" in line:
                f_out.write(line)
            elif "# successes" in line:
                f_out.write(line)
                f_out.write("\n")

            # 그 외 라인은 무시
        # 요약 맨 끝에 개행 추가
        f_out.write("\n")


# 사용 예시
path = "/home/sanghyeok/openvla/experiments/logs/EVAL-libero_goal-openvla-2025_05_10-18_11_05-dola.txt"
summary_path = f"outputs/summary/{os.path.basename(path)}"
log_to_summary(path, summary_path)
