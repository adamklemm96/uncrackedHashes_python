#!/usr/bin/env python3

import os,sys,pandas as pd, csv, time
os.system("clear")
path1 = sys.argv[1]
start = time.time()
filePaths = []
with os.scandir(path1) as it:
    for entry in it:
        if entry.name.endswith(".csv") and entry.is_file():
            filePaths.append(entry.path)

rows = []

toolbar_width = len(filePaths)
sys.stdout.write("[%s]" % (" " * toolbar_width))
sys.stdout.flush()
sys.stdout.write("\b" * (toolbar_width+1))
for path in filePaths:
    #progress bar
    sys.stdout.write("-")
    sys.stdout.flush()
    #reads second column
    df = pd.read_csv(path, header=None)
    rows.append(df.count())
    new_format = df.loc[df[2].isnull(), 1]
    new_format.dropna(inplace=True)
sys.stdout.write("]\n")
#count emails / lines
emails_count=[]
hash_count = []
password_count = []
for x in rows:
    emails_count.append(x[0])
    hash_count.append(x[1])
    password_count.append(x[2])

end = time.time()
print(f"""
Total rows: {sum(emails_count)}
Hashes: {sum(hash_count)}
Passwords: {sum(password_count)}
""")
print("It took ",end - start)

answer = input("Would you like to save uncracked hashes to a file?[y/n]: ")
if answer == 'y' or answer == 'Y':
    name = input("Enter the name of the file with a suffix (.txt, .csv): ")
    destination = "/home/adam/toCrack/uncracked_hashes/"
    new_format.to_csv(destination+name, mode= 'a', index=None, header=None)
    print(f"Uncracked passwords saved to ",destination)
    upload = input("Upload file to GCLOUD? [y/n]: ")
    if upload == 'y' or upload == 'Y':
        directory_name = input("Enter the destination in gs://data_breaches/: ")
        bash_command = f"gsutil -m cp {destination+name} gs://data_breaches/{directory_name}*"
        os.system(bash_command)
        os.system(f"gsutil ls gs://data_breaches/{directory_name}")

