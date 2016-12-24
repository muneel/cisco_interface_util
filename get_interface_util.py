from telnetlib import Telnet
import re
import time
import argparse
import sys


def print_output(output, interface):
    in_rate = 0
    out_rate = 0
    for item in output:
        if re.search('.*input rate*?', item):
            m = re.search(r'.*rate.(\d+).*', item)
            in_rate = float(m.group(1)) / 1000000
        elif re.search('.*output rate*?', item):
            m = re.search(r'.*rate.(\d+).*', item)
            out_rate = float(m.group(1)) / 1000000

    print "%65s, %7.2f Mbps, %7.2f Mbps" % (interface, in_rate, out_rate)


def get_interface(switch, user, password, enable_password, list):
    tel = Telnet(switch, 23, 30)
    check_con = tel.expect([r".*Password: "], 10)
    tel.write(password + '\r\n')
    tel.expect([r".*>"], 10)
    tel.write('en\r\n')
    check_con = tel.expect([r".*Password.*"], 10)
    tel.write(enable_password + '\r\n')
    check_con = tel.expect([r".*#"], 10)
    print 'Login Successful'
    print '      Interface Status                                             Input Rate, Output Rate'

    for int in list:
        cmd = 'show int ' + str(int) + ' | include line\r\n'
        time.sleep(0.5)
        tel.write(cmd)
        check_con = tel.expect([r".*#"], 10)
        interface = str(check_con[2])
        trim_output = interface.split('\r\n')
        interface = trim_output[1]
        cmd = 'show int ' + str(int) + ' | include rate\r\n'
        time.sleep(0.5)
        tel.write(cmd)
        check_con = tel.expect([r".*#"], 10)
        output = str(check_con[2])
        trim_output = output.split('\r\n')
        print_output(trim_output, interface)


def get_cli_args(args=None):
    parser = argparse.ArgumentParser(
        description='Script to get the Input/Output Rates for a given list of Interfaces from cisco switch')
    parser.add_argument('-s', '--switch',
                        type=str,
                        help='Switch IP Address',
                        required='True')
    parser.add_argument('-u', '--user',
                        type=str,
                        help='Username')
    parser.add_argument('-p', '--password',
                        type=str,
                        help='Password',
                        required=True)
    parser.add_argument('-e', '--enable_password',
                        type=str,
                        help='Enable Password',
                        required=True)
    parser.add_argument('-i', '--interfaces',
                        type=str,
                        help='Interfaces',
                        nargs='+',
                        default=',')
    parser.add_argument('-f', '--file',
                        nargs='?', type=argparse.FileType('r'),
                        help='File containing list of Interfaces',
                        default=None)

    results = parser.parse_args(args)

    if results.interfaces == ',' and results.file is None:
        print 'ERROR - interface or file needed'
        sys.exit(0)
    results.interfaces = results.interfaces[0].split(",")
    return (results.switch,
            results.user,
            results.password,
            results.enable_password,
            results.interfaces,
            results.file)

if __name__ == '__main__':
    s, u, p, e, i, f = get_cli_args(sys.argv[1:])
    if f is None:
        get_interface(s, u, p, e, i)
        pass
    else:
        list = f.readlines()
        list = map(lambda s: s.strip(), list)
        get_interface(s, u, p, e, list)
