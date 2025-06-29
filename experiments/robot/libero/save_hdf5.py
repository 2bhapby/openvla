# save_hdf5.py

import os
import numpy as np
import h5py

def save_regenerate_format_hdf5(
    save_dir,
    task_name,
    episode_idx,
    actions,
    states,
    robot_states,
    gripper_states,
    joint_states,
    ee_states,
    agentview_images,
    eye_in_hand_images,
):
    os.makedirs(save_dir, exist_ok=True)
    hdf5_path = os.path.join(save_dir, f"{task_name}_demo.hdf5")

    # 새 HDF5 파일 또는 기존 파일 열기
    if os.path.exists(hdf5_path):
        file = h5py.File(hdf5_path, "a")
    else:
        file = h5py.File(hdf5_path, "w")

    if "data" not in file:
        root = file.create_group("data")
    else:
        root = file["data"]

    ep_name = f"demo_{episode_idx}"
    if ep_name in root:
        print(f"❗️ {ep_name} already exists. Overwriting.")
        del root[ep_name]

    ep_group = root.create_group(ep_name)

    # Done, Reward
    dones = np.zeros(len(actions), dtype=np.uint8)
    dones[-1] = 1
    rewards = np.zeros(len(actions), dtype=np.uint8)
    rewards[-1] = 1

    # obs group
    obs_group = ep_group.create_group("obs")
    obs_group.create_dataset("gripper_states", data=np.stack(gripper_states))
    obs_group.create_dataset("joint_states", data=np.stack(joint_states))
    obs_group.create_dataset("ee_states", data=np.stack(ee_states))
    obs_group.create_dataset("ee_pos", data=np.stack(ee_states)[:, :3])
    obs_group.create_dataset("ee_ori", data=np.stack(ee_states)[:, 3:])
    obs_group.create_dataset("agentview_rgb", data=np.stack(agentview_images))
    obs_group.create_dataset("eye_in_hand_rgb", data=np.stack(eye_in_hand_images))

    # 기본 데이터
    ep_group.create_dataset("actions", data=np.stack(actions))
    ep_group.create_dataset("states", data=np.stack(states))
    ep_group.create_dataset("robot_states", data=np.stack(robot_states))
    ep_group.create_dataset("rewards", data=rewards)
    ep_group.create_dataset("dones", data=dones)

    file.close()
    print(f"✅ Saved: {hdf5_path} / {ep_name}")

def save_regenerate_format_hdf5_grouped(
    save_dir,
    task_name,
    episode_idx,
    actions,
    states,
    robot_states,
    gripper_states,
    joint_states,
    ee_states,
    agentview_images,
    eye_in_hand_images,
):
    """
    Save rollout into a single HDF5 file per task with groups named demo_0, demo_1, etc.
    """
    os.makedirs(save_dir, exist_ok=True)
    file_path = os.path.join(save_dir, f"{task_name}.hdf5")
    demo_name = f"demo_{episode_idx}"

    with h5py.File(file_path, "a") as f:
        demo_group = f.create_group(demo_name)

        demo_group.create_dataset("actions", data=np.array(actions), compression="gzip")
        demo_group.create_dataset("states", data=np.array(states), compression="gzip")
        demo_group.create_dataset("robot_states", data=np.array(robot_states), compression="gzip")
        demo_group.create_dataset("rewards", data=np.ones((len(actions),), dtype=np.uint8))
        demo_group.create_dataset("dones", data=np.zeros((len(actions),), dtype=np.uint8))
        demo_group["dones"][-1] = 1  # 마지막 step은 done 처리

        obs_group = demo_group.create_group("obs")
        obs_group.create_dataset("gripper_states", data=np.array(gripper_states), compression="gzip")
        obs_group.create_dataset("joint_states", data=np.array(joint_states), compression="gzip")
        obs_group.create_dataset("ee_states", data=np.array(ee_states), compression="gzip")
        obs_group.create_dataset("agentview_rgb", data=np.array(agentview_images), compression="gzip")
        obs_group.create_dataset("eye_in_hand_rgb", data=np.array(eye_in_hand_images), compression="gzip")

    print(f"[✓] 저장 완료: {file_path} > {demo_name}")
