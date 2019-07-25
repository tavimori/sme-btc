#!/usr/bin/env python3
import subprocess





offset = 0
count = 10000

while count > 0:
    a = subprocess.run("./analyze-sme-btc2.py {}".format(offset), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    if a.returncode != 0:
        print("exec fail")
        bad_id = a.stdout.split("\n")[-1].split("\t")[0].split(" ")[1]
        bad_uid_str = a.stdout.split("\n")[-1].split("\t")[1].split(" ")[1]
        print("bad_uid: {}".format(bad_uid_str))
        with open("bad-uids-auto.txt", "a") as bad_uid_file:
            bad_uid_file.write(bad_uid_str)
            bad_uid_file.write("\n")
        count -= 1
        offset += int(bad_id) - 3
        print("offset = {}".format(offset))
        # print(a.stdout)
    else:
        print("success")
        print(a.returncode)