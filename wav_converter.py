import librosa
import numpy as np

def analyze_wav_frequencies(input_file, output_file):
    """
    Extract frequencies from WAV file and write them to a text file.
    
    Args:
        input_file (str): Path to input WAV file
        output_file (str): Path to output text file
    """
    # Load the audio file
    y, sr = librosa.load(input_file)
    
    # Extract frequencies using librosa
    frequencies = librosa.piptrack(y=y, sr=sr)[0]  # Only get frequencies, ignore magnitudes
    
    # Get timestamps
    times = librosa.times_like(frequencies)
    
    # Write frequencies to file
    with open(output_file, 'w') as f:
        
        for t, freq_frame in zip(times, frequencies.T):
            # Get the main frequency for this frame (excluding zeros)
            main_freq = np.max(freq_frame[freq_frame > 0]) if any(freq_frame > 0) else 0
            if main_freq > 0:  # Only write if we detected a frequency
                f.write(f"{t:.3f} | {main_freq:.1f}\n")

# Example usage
if __name__ == "__main__":
    input_file = "moog.wav"
    output_file = "frequencies.txt"
    analyze_wav_frequencies(input_file, output_file)