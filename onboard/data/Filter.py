from scipy.signal import butter, filtfilt

# === Smoothing ===
def filterReading(data: list[float], lookback: int) -> list[float]:
    """Smoothes raw sensor input based on historical data."""

    lookback = min(lookback, len(data) - 1)
    cutoff = 250
    fs = 5000 # sample rate (rule of thum)

    b, a = butter(5, cutoff / (0.5 * fs), btype='lowpass', analog=False)
    return filtfilt(b, a, data)