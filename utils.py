def read_dict(file):
    with open(file) as f:
        text = f.read().upper().split('\n')
        f.close()
        return text
