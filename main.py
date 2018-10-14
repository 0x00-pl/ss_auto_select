import json
import sys
import py_ping


def read_server_list(gui_config_file):
    gui_config = json.load(open(gui_config_file, 'r'))
    configs = gui_config['configs']
    return [item['server'] for item in configs]


def test_server(addr):
    result = py_ping.ping(addr)
    return float(result['avg']) if result is not None else 99999


def fast_in_server_list(addr_list):
    ping_avg_addr = [(test_server(addr), addr) for addr in addr_list]
    fast_avg_addr = min(ping_avg_addr, key=(lambda x: x[0]))
    return fast_avg_addr[1]


def gen_config(gui_config_file, fast_server):
    gui_config = json.load(open(gui_config_file, 'r'))
    config = {}
    for item in gui_config['configs']:
        if item['server'] == fast_server:
            config = item
    config['localPort'] = 1080
    return config


def main(gui_config_file, config_file):
    server_list = read_server_list(gui_config_file)
    fast_server = fast_in_server_list(server_list)
    config = gen_config(gui_config_file, fast_server)
    json.dump(config, open(config_file, 'w'), indent=4)


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
