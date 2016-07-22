import argparse
import modules

parser = argparse.ArgumentParser(description='NetFork - Network protocols fuzzer.')

parser.add_argument('--type', '-t', type=str,
                    help='client or server fuzzing')
parser.add_argument('--host', '-H', type=str,
                    help='target host address or hostname')
parser.add_argument('--proto', '-p', type=str,
                    help='target protocol')
parser.add_argument('--sum', dest='accumulate', action='store_const',
                    const=sum, default=max,
                    help='sum the integers (default: find the max)')

args = parser.parse_args()

server_type = args.type
target_addr = args.host
proto = args.proto

