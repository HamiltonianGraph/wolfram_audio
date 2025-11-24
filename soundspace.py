import os
import numpy as np
from scipy.io.wavfile import write


def sine_segment(freq, dur, sr=44100, amp=0.12):
    t = np.linspace(0, dur, int(sr*dur), endpoint=False)
    # smooth attack/release to avoid clicks
    env = np.ones_like(t)
    a = int(0.01 * sr)  # 10 ms attack
    r = int(0.01 * sr)  # 10 ms release
    if a > 0:
        env[:a] = np.linspace(0, 1, a)
    if r > 0:
        env[-r:] = np.linspace(1, 0, r)
    return amp * env * np.sin(2*np.pi*freq*t)


def render_sequence(freqs, seg_dur=0.05, sr=44100, amp=0.12):
    audio = np.concatenate([sine_segment(f, seg_dur, sr, amp) for f in freqs])
    # safety headroom
    audio = np.clip(audio, -0.9, 0.9)
    return audio


def save_wav(filename, audio, sr=44100):
    write(filename, sr, (audio * 32767).astype(np.int16))


def wolfram_ca(rule_num, width=128, steps=600):
    rule = np.array([(rule_num >> i) & 1 for i in range(8)], dtype=np.uint8)
    state = np.zeros(width, dtype=np.uint8)
    state[width//2] = 1
    rows = [state.copy()]
    for _ in range(steps-1):
        left  = np.roll(state, 1)
        right = np.roll(state, -1)
        neighborhood = (left << 2) | (state << 1) | right
        state = rule[neighborhood]
        rows.append(state.copy())
    return np.array(rows)


def ca_to_freqs(rows, fmin=220, fmax=880):
    width = rows.shape[1]
    counts = rows.sum(axis=1)
    x = counts / width  # 0..1 density
    freqs = fmin + x * (fmax - fmin)
    return freqs


def generate_all_rules(output_dir="wolfram_wavs", sr=44100, seg_dur=0.05, duration=30):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    steps = int(duration / seg_dur)
    
    print(f"Generating rules 1-255 into '{output_dir}'...")
    
    for rule_num in range(1, 256):
        # Generate CA
        rows = wolfram_ca(rule_num=rule_num, width=128, steps=steps)
        # Convert to frequencies
        freqs = ca_to_freqs(rows, fmin=180, fmax=1200)
        # Render audio
        audio = render_sequence(freqs, seg_dur=seg_dur, sr=sr, amp=0.10)
        
        filename = os.path.join(output_dir, f"ca_rule{rule_num}.wav")
        save_wav(filename, audio, sr=sr)
        if rule_num % 10 == 0:
            print(f"Generated rule {rule_num}")

if __name__ == "__main__":
    generate_all_rules()
