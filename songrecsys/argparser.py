from argparse import ArgumentParser

def parse_args():
    parser = ArgumentParser(description='Song recommendation system')
    parser.add_argument('--id', type=str, help='Spotify app client ')
    parser.add_argument('--secret', type=str, help=)