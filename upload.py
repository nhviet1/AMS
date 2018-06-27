# ================Import Library=================
import ftplib
import os
import db_query
import configparser
# ===============================================


# ===========Function: Clear old file in record folder==============
# Arguments:    [1]
# Arguments: [Folder Path]
def clear_dir(record_folder_path):
    list_file = os.listdir(record_folder_path)
    for f in list_file:
        os.remove(record_folder_path + "\\" + f)
# ==================================================================


# ===========Function: Upload File to Server using FTP==============
# Arguments:    [1]          [2]
# Arguments: [File Path] [File Name]
def single_file_upload(folder_path, file_name):
    # Read config data
    config_reader = configparser.ConfigParser()
    config_reader.sections()
    config_reader.read("config.ini")
    config_reader.sections()
    # FTP config
    ftp_server_name = config_reader["FTP"]["server_name"]
    ftp_port = config_reader["FTP"]["port"]
    ftp_user_name = config_reader["FTP"]["user_name"]
    ftp_password = config_reader["FTP"]["password"]

    file_full_path = folder_path + "\\" + file_name
    if os.path.isfile(file_full_path):
        # write_log("Start upload file: " + file_full_path)
        session = ftplib.FTP()
        session.connect(ftp_server_name, int(ftp_port))
        session.login(ftp_user_name, ftp_password)
        # session = ftplib.FTP(ftp_server_name, ftp_user_name, ftp_password, "2233")
        # session.connect("localhost", "2233")
        file = open(file_full_path, 'rb')  # file to send
        session.storbinary('STOR ' + file_name, file)  # send the file
        file.close()  # close file and FTP
        session.quit()

    # Insert media's info into "MEDIA_TEMP"
    file_size = str(os.path.getsize(folder_path + "\\" + file_name))
    db_query.media_temp_insert("cam1", file_size, file_name, "")
# ==================================================================


# ===========Function: Upload all file in folder to FTP Server==============
# Arguments:      [1]
# Arguments: [Folder Path]
def folder_upload(folder_path):
    list_file = os.listdir(folder_path)
    list_file = sorted(list_file, key=lambda x: os.path.getctime(folder_path + "\\" + x))
    if len(list_file) > 1:
        for i in range(0, len(list_file)-2):
            os.remove(folder_path + "\\" + list_file[i])
        for i in range(len(list_file) - 2, len(list_file) - 1):
            # print('File name: ' + list_file[i])
            # FTP upload
            single_file_upload(folder_path, list_file[i])
            # Remove file after uploaded
            os.remove(folder_path + "\\" + list_file[i])
# =========================================================================







