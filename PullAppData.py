# Create : 2016.05.26 holmes.

import os
import sys
import platform
import subprocess
import re


def PullAppData(apkpath):
    # apkinfos
    infos = subprocess.Popen("aapt dump badging {0}".format(
        apkpath), stdout=subprocess.PIPE).stdout.read()
    infos = infos.decode()

    PackageName = re.search("package: name='.*?'", infos)
    AppName = re.search("application-label:'.*?'", infos)

    result = {}
    if AppName:
        result["AppName"] = AppName.group(0)[19:-1]
    else:
        result["AppName"] = ""

    if PackageName:
        result["PackageName"] = PackageName.group(0)[15:-1]
    else:
        result["PackageName"] = ""

    adb_run_as_root = "adb root"
    os.system(adb_run_as_root)
    adb_pull = "adb pull /data/data/{0} {1}{0}_AppData".format(
        result["PackageName"], apkpath.replace(apkpath.split("\\")[-1], ""))
    adb_pull_infos = subprocess.Popen(
        adb_pull, stdout=subprocess.PIPE).stdout.read()
    adb_pull_infos = adb_pull_infos.decode()

if __name__ == '__main__':
    print("Python Version: {0}".format(platform.python_version()))
    apkpath = sys.argv[1]

    PullAppData(apkpath)
