import os
import fileinput
import sys
import re

f = 'C://Users//neel//Documents//winaflautomation//testing11.txt'
sambit = input('provide exe file path use // in place of \  ')
find = '( .*)|([^0-9a-zA-Z\n])'
replace = ''
with open(f, "r") as myfile:
    s = myfile.read()

ret = re.sub(find, replace, s)  # find and replace
# print(ret)
wr = open('C://Users//neel//Documents//winaflautomation//testing123.txt', "w+")
wr.write(ret)
wr.close()

with open('C://Users//neel//Documents//winaflautomation//testing123.txt') as infile:
    with open('C://Users//neel//Documents//winaflautomation//results11.txt', 'w') as outfile:
        rum = '00007ff75ad00000'
        hxrum = int(rum, 16)

        for line in infile:
            try:
                num = int(line, 16)
                total = num - hxrum
                print(hex(total), file = outfile)
            except ValueError:
                print(
                    "'{}' is not a number".format(line.rstrip())
                )

with open('C://Users//neel//Documents//winaflautomation//results11.txt', 'r') as f:
    lines = f.readlines()
    with open('C://Users//neel//Documents//winaflautomation//results12.txt', 'w') as f:
        line1 = ['mkdir ' + line for line in lines]
        line2 = ['&& cd ' + line for line in lines]
        for item_a, item_b in zip(line1, line2):
            y = item_a.__add__(item_b)
            f.writelines(y)
with open('C://Users//neel//Documents//winaflautomation//results12.txt', 'r') as f2:
    content = f2.read().splitlines()

    with open('C://Users//neel//Documents//winaflautomation//results12.txt', 'w') as f2:
        f2.writelines("\n".join(" ".join(two_lines) for two_lines in zip(content[::2], content[1::2])) + (
            content[-1] if len(content) % 2 != 0 else ''))
    # print(x)


def te():
    for line in fileinput.input(['C://Users//neel//Documents//winaflautomation//results11.txt'], inplace=True):
        sys.stdout.write(
            " && C://Fuzzing//DynamoRIO//bin64//drrun.exe -c C://Fuzzing//winafl-master-64//bin//Debug//winafl.dll -debug -target_module" + ' ' + sambit + ' '+ "-target_offset {lo}".format(
                lo=line))


def to():
    file_name = 'C://Users//neel//Documents//winaflautomation//results11.txt'
    cmdCommand1 = " -fuzz_iterations 10 -nargs 2 --"+ ' ' + sambit + ' '+  input('provide the image file path use // in place of \ ') + "&& cd.."

    with open(file_name, 'r') as f:
        file_lines = [' '.join([x.strip(), cmdCommand1, '\n']) for x in f.readlines()]

    with open(file_name, 'w') as f:
        # print(f.readline())
        f.writelines(file_lines)
        # print(file_lines)


te()
to()

with open('C://Users//neel//Documents//winaflautomation//results12.txt', 'r') as fh1, open(
        'C://Users//neel//Documents//winaflautomation//results11.txt', 'r') as fh2:
    for line1, line2 in zip(fh1, fh2):
        # print(line1+line2)

        with open('C://Users//neel//Documents//winaflautomation//results13.txt', 'w+') as f4:
            file_lines1 = [' '.join([x.strip(), fh2.readline(), '\n']) for x in fh1.readlines()]
            f4.writelines(file_lines1)

with open('C://Users//neel//Documents//winaflautomation//results13.txt')as f5:
    for lin in f5:
        os.system(lin)
