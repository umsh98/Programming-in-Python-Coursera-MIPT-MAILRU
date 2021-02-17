import os
import json
import argparse
import tempfile


def parse():
    """Parsing the arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument('--key', help='key for getting/saving values')
    parser.add_argument('--value', help='saved value')

    return parser.parse_args()


def read_data(path):
    """Reading data from the storage."""
    if not os.path.exists(storage_path):
        return {}

    with open(path, 'r') as f:
        json_data = f.read()

    if json_data:
        return json.loads(json_data)
    else:
        return {}


def write_data(path, data):
    """Writing the data to the storage."""
    with open(path, 'w') as f:
        f.write(json.dumps(data))


def put(path, key, value):
    """Putting the values with the keys into the storage."""
    data = read_data(path)
    data.setdefault(key, list())
    data[key].append(value)
    write_data(path, data)


def get(path, key):
    """Getting values by the key."""
    data = read_data(path)

    return data.get(key, [])


def storage(path):

    args = parse()

    if args.key and args.value:
        put(path, args.key, args.value)
    elif args.key:
        result = get(path, args.key)
        print(', '.join(result))
    else:
        print('Please, enter a key or a key with a value.')


if __name__ == "__main__":

    storage_path = os.path.join(tempfile.gettempdir(), 'storage.data')
    storage(storage_path)
