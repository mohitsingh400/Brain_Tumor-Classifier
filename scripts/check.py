import zipfile

with zipfile.ZipFile("archive.zip", "r") as z:
    for name in z.namelist()[:50]:  
        print(name)
