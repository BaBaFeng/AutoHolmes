# Create : 2016.05.25 holmes.


def appinfo(apkPath):
    # apkinfos
    import subprocess
    import re
    infos = subprocess.Popen("aapt dump badging {0}".format(apkPath), stdout=subprocess.PIPE).stdout.read()
    infos = infos.decode()

    HomeActivity = re.search("launchable-activity: name='.*?'", infos)
    PackageName = re.search("package: name='.*?'", infos)
    AppName = re.search("application-label:'.*?'", infos)
    AppVersion = re.search("versionName='.*?'", infos)
    appversionCode = re.search("versionCode='.*?'", infos)

    result = {}
    if AppName:
        result["AppName"] = AppName.group(0)[19:-1]
    else:
        result["AppName"] = ""

    if AppVersion:
        result["AppVersion"] = AppVersion.group(0)[13:-1]
    else:
        result["AppVersion"] = ""

    if appversionCode:
        result["appversionCode"] = appversionCode.group(0)[13:-1]
    else:
        result["appversionCode"] = ""

    if PackageName:
        result["PackageName"] = PackageName.group(0)[15:-1]
    else:
        result["PackageName"] = ""

    if HomeActivity:
        result["HomeActivity"] = HomeActivity.group(0)[27:-1]
    else:
        result["HomeActivity"] = ""

    # hash
    import hashlib
    md5 = hashlib.md5()
    sha1 = hashlib.sha1()
    sha256 = hashlib.sha256()

    _File = open(apkPath, "rb")
    data = _File.read()
    md5.update(data)
    sha1.update(data)
    sha256.update(_File.read())

    _File.close()
    APPMD5 = md5.hexdigest()

    _File = open(apkPath, "rb")
    _File.close()
    AppSHA1 = sha1.hexdigest()
    AppSHA256 = sha256.hexdigest()

    if APPMD5:
        result["AppMD5"] = APPMD5
    else:
        result["AppMD5"] = ""

    if AppSHA256:
        result["AppSHA256"] = AppSHA256
    else:
        result["AppSHA256"] = ""

    if AppSHA1:
        result["AppSHA1"] = AppSHA1
    else:
        result["AppSHA1"] = ""
    # cer
    import zipfile
    import os
    zipFile = zipfile.ZipFile(apkPath)
    for zipFiles in zipFile.namelist():
        if (zipFiles[-3:] == "RSA"):
            zipFile.extract(zipFiles, apkPath[:-4])
            keytools = "keytool -printcert -file %s\\%s" % (
                apkPath[:-4], zipFiles.replace("/", "\\"))
    cer = os.popen(keytools).read()
    # os.system("rd /q /s %s" % apkPath[:-4])

    if cer:
        result["cer"] = cer

    return result


if __name__ == "__main__":
    import platform
    print("Python Version: {0}".format(platform.python_version()))

    import sys
    apkpath = sys.argv[1]
    appinfos = appinfo(apkpath)

    print("Apk File Name: %s" % apkpath.split("\\")[-1])

    print("AppName: %s" % appinfos["AppName"])
    print("AppVersion: %s" % appinfos["AppVersion"])
    print("appversionCode: %s" % appinfos["appversionCode"])
    print("PackageName: %s" % appinfos["PackageName"])
    print("HomeActivity: %s" % appinfos["HomeActivity"])
    print("AppMD5: %s" % appinfos["AppMD5"])
    print("AppSHA1: %s" % appinfos["AppSHA1"])
    print("AppSHA256: %s" % appinfos["AppSHA256"])
    print("%s" % appinfos["cer"])
