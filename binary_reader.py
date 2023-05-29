import config

def read_file(path: str) -> str:
    """Fast way to read file with diffs that may contain binary data.
    Skips binary data in efficient way if it occurs"""
    with open(path, 'rb') as f:
        binary_data = f.read()
    data = []
    step = config.DEFAULT_STEP
    for pos in range(0, len(binary_data), step):
        chunk = binary_data[pos:pos+step]
        try:
            data.append(chunk.decode())
            step = config.DEFAULT_STEP
        except UnicodeDecodeError:
            if step < config.MAX_STEP:
                step *= 2
    return "".join(data)