import sys
import os
import time
import schedule        
import shutil
import hashlib
import zipfile

def Create_ZIP(folder):
    timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")

    zip_name = folder + "_" + timestamp + ".zip"

    # open the zip file
    zobj = zipfile.ZipFile(zip_name,'w',zipfile.ZIP_DEFLATED)

    for root,dirs,files in os.walk(folder):
        for file in files:
            full_path = os.path.join(root,file)
            relative = os.path.relpath(full_path,folder)

            zobj.write(full_path,relative)

    zobj.close()

    return zip_name


def Calculate_hash(path):
    hobj = hashlib.md5()

    fobj = open(path,"rb")

    while True:
        data = fobj.read(1024)
        if not data:
            break
        else:
            hobj.update(data)
    
    fobj.close()

    return hobj.hexdigest()

def BackupFiles(Source,Destination):
    copied_files = []

    print("Creating the Backup folder for the backup process")

    os.makedirs(Destination,exist_ok=True)

    for root,dirs,files in os.walk(Source):
        for file in files:
            src_path = os.path.join(root,file)

            relative = os.path.relpath(src_path,Source)
            dest_path = os.path.join(Destination,relative)

            os.makedirs(os.path.dirname(dest_path),exist_ok=True)

            # copy the files if its new
            if ((not os.path.exists(dest_path)) or (Calculate_hash(src_path) != Calculate_hash(dest_path))):
                shutil.copy2(src_path,dest_path)
                copied_files.append(relative)
            
            

    return copied_files


def MarvellousDataShieldStart(Source = "Data"):
    Border = "-"*50

    BackName = "MarvellousBackup"

    print(Border)
    print("Backup Process started succesfully at :",time.ctime())
    print(Border)

    files = BackupFiles(Source,BackName)

    zip_file = Create_ZIP(BackName)

    print(Border)
    print("Backup completed succesfully")
    print("Files copied : ",len(files))
    print("Zip file gets created : ",zip_file)
    print(Border)

def main():
    Border = "-"*50
    print(Border)
    print("-------Marvellous Data Shield System--------")
    print(Border)

    if(len(sys.argv) == 2):
        if(sys.argv[1] == "--h"or sys.argv[1] == "--H"):
            print("1 : Takes Auto Backup at given time")
            print("2 : Backup only new and updated files")
            print("3 : Create an archive of the backup prediocally")
        
        elif(sys.argv[1] == "--u" or sys.argv[1] == "--U"):
            print("Use the automation script as :")
            print("ScriptName.py TimeInterval Source Directory")
            print("TimeInterval : Time in Minutes for periodic Scheduling")
            print("SourceDirectory : Name of directory to be backed up")

        else:
            print("Unable to proceed there is no such option")
            print("please use --h,--u for more Details")
    
    # python Demo.py 5 Data
    elif(len(sys.argv) == 3):
        print("Inside projects Logic")
        print("Time Interval :",sys.argv[1])
        print("Directory Name :",sys.argv[2])
        
        # Apply the Scheduler
        schedule.every(int(sys.argv[1])).minutes.do(MarvellousDataShieldStart,sys.argv[2])

        print(Border)
        print("Data Shield System Started Succesfully")
        print("Time Interval in minutes : ",sys.argv[1])
        print("Press Ctrl + C to Stop the Execution")
        print(Border)

        # Wait Till abort
        while True:
            schedule.run_pending()
            time.sleep(1)

    else:
        print("Invalid number of commandline Arguments")
        print("Unable to proceed there is no such option")
        print("please use --h,--u for more Details")

    print(Border)
    print("----------Thank you for using our script----------")
    print(Border)

if __name__ == "__main__":
    main()