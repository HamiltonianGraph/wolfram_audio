# Soundspace: Wolfram CA Sonification

Inspired by the work of [Stephen Wolfram](https://www.wolframscience.com/nks/) and the video ["Emergent Complexity"](https://youtu.be/0HqUYpGQIfs?si=iO7CaGzHBo_VxWSZ) by [Emergent Garden](https://www.youtube.com/@EmergentGarden), this repo explores the auditory patterns hidden within Wolfram's Elementary Cellular Automata. This Python script generates audio by mapping the density of cellular automata generations to sound frequencies, creating unique sonic textures for each of the 256 rules.

## How It Works
The script simulates a 1D cellular automaton (like Rule 30 or Rule 110) over time. For each generation (row), it calculates the "density" of active cells. This density is then mapped to a frequency pitch, which is synthesized as a sine wave segment. Concatenating these segments creates a rhythmic, evolving soundscape.

## Dependencies
- Python 3
- `numpy`
- `scipy`

Install via pip:
```bash
pip install numpy scipy
```

## Usage
Run the script to generate WAV files for all 256 rules in the `wolfram_wavs/` directory:

```bash
python soundspace.py
```

## Code Overview

### `wolfram_ca(rule_num, width, steps)`
Simulates the Elementary Cellular Automaton.
- `rule_num`: The Wolfram rule number (0-255).
- `width`: Width of the grid (number of cells).
- `steps`: Number of time steps (generations) to simulate.
Returns a 2D numpy array of the automaton's history.

### `ca_to_freqs(rows, fmin, fmax)`
Converts the CA grid into a sequence of frequencies.
- Calculates the active cell density for each row.
- Maps this density to a frequency between `fmin` and `fmax`.

### `sine_segment(freq, dur, sr, amp)`
Synthesizes a single sine wave tone with a smooth attack and release envelope to prevent clicking artifacts.

### `render_sequence(freqs, seg_dur, sr, amp)`
Stitches together the sine segments for the entire sequence of frequencies into a single audio buffer.

### `save_wav(filename, audio, sr)`
Writes the generated audio buffer to a standard WAV file.

### `generate_all_rules(output_dir, ...)`
The main driver function that iterates through rules 1 to 255, generates the audio for each, and saves them to the specified output directory.

---
*Experiment with different `fmin`, `fmax`, or `seg_dur` values in the code to discover new sounds!*
