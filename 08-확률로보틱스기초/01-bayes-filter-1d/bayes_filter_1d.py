#!/usr/bin/env python3
# bayes_filter_1d.py
import random
import matplotlib.pyplot as plt

NUM_CELLS = 30                        # 복도를 30칸으로 나눔(칸당 0.5m, 총 15m)
DOOR_CELLS = [3, 8, 15, 22]           # 문이 있는 칸의 인덱스
P_HIT = 0.8                           # 문 앞에서 센서가 "문"이라고 옳게 읽을 확률
P_FALSE_ALARM = 0.1                   # 문이 아닌 곳에서 센서가 "문"이라고 잘못 읽을 확률(오탐)
MOTION_PROFILE = [0.1, 0.8, 0.1]      # 명령한 1칸 이동 대비 실제 이동량(0/1/2칸)의 확률
TRUE_START = 1                        # 로봇의 실제 시작 위치(시뮬레이션 전용 — 필터는 모르는 값)
NUM_STEPS = 14
SEED = 61


def uniform_belief(num_cells):
    return [1.0 / num_cells] * num_cells


def predict(belief, motion_profile):
    new_belief = [0.0] * len(belief)
    for src, p_src in enumerate(belief):
        for offset, p_offset in enumerate(motion_profile):
            dst = src + offset
            if dst < len(belief):
                new_belief[dst] += p_src * p_offset
    return new_belief


def likelihood(measurement, num_cells, door_cells):
    hit = [P_HIT if c in door_cells else P_FALSE_ALARM for c in range(num_cells)]
    if measurement == 1:
        return hit
    return [1.0 - h for h in hit]


def correct(belief, measurement, door_cells):
    lik = likelihood(measurement, len(belief), door_cells)
    unnormalized = [b * l for b, l in zip(belief, lik)]
    total = sum(unnormalized)
    return [u / total for u in unnormalized]


def simulate_motion(true_pos, motion_profile, num_cells, rng):
    offset = rng.choices(range(len(motion_profile)), weights=motion_profile)[0]
    return min(true_pos + offset, num_cells - 1)


def simulate_measurement(true_pos, door_cells, rng):
    p_hit = P_HIT if true_pos in door_cells else P_FALSE_ALARM
    return 1 if rng.random() < p_hit else 0


def run_filter(rng):
    belief = uniform_belief(NUM_CELLS)
    true_pos = TRUE_START
    history = [belief]

    for step in range(NUM_STEPS):
        true_pos = simulate_motion(true_pos, MOTION_PROFILE, NUM_CELLS, rng)
        belief = predict(belief, MOTION_PROFILE)
        history.append(belief)

        measurement = simulate_measurement(true_pos, DOOR_CELLS, rng)
        belief = correct(belief, measurement, DOOR_CELLS)
        history.append(belief)

        best = max(range(NUM_CELLS), key=belief.__getitem__)
        label = '문' if measurement else '문아님'
        print(f'스텝 {step+1:2d} | 실제 위치 {true_pos:2d} | 관측 {label} '
              f'| 최고 확신 칸 {best:2d} ({belief[best]:.3f})')

    return history, true_pos


def plot_strip(history, true_pos, snapshot_frames):
    fig, axes = plt.subplots(1, len(snapshot_frames), figsize=(4 * len(snapshot_frames), 3), sharey=True)
    for ax, frame in zip(axes, snapshot_frames):
        belief = history[frame]
        colors = ['tab:red' if c in DOOR_CELLS else 'tab:blue' for c in range(NUM_CELLS)]
        ax.bar(range(NUM_CELLS), belief, color=colors)
        ax.axvline(true_pos, color='black', linestyle='--', linewidth=1)
        ax.set_title(f'프레임 {frame}')
        ax.set_xlabel('칸 인덱스')
    axes[0].set_ylabel('믿음 bel(x)')
    fig.suptitle('1D 베이즈 필터 — 예측(퍼짐)과 보정(좁아짐)의 반복')
    fig.tight_layout()
    fig.savefig('bayes_filter_1d_strip.png', dpi=150)
    print('그림 저장: bayes_filter_1d_strip.png')


def main():
    rng = random.Random(SEED)
    history, true_pos = run_filter(rng)
    snapshot_frames = [0, 4, 14, 20, len(history) - 1]
    plot_strip(history, true_pos, snapshot_frames)


if __name__ == '__main__':
    main()
