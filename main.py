import configparser
import time
import vlc_record
import log_writer
import upload
import db_query

# ====================Main Function====================
# Read config data
log_writer.write_log("AMS_Client Start!")
config_reader = configparser.ConfigParser()
config_reader.sections()
config_reader.read("config.ini")
config_reader.sections()
# FTP config
record_folder_path = config_reader["VLC_RECORD"]["record_folder_path"]
# Clear record folder
upload.clear_dir(record_folder_path)
# Clear streaming data
db_query.clear_streaming_media()
# Create new threads
log_writer.write_log("Create VLC record thread")
thread_1 = vlc_record.RecorderThreading()
# Start new Threads
log_writer.write_log("Start thread")
thread_1.start()
# ====================Main Loop=======================
while True:
    upload.folder_upload(record_folder_path)
    time.sleep(20)
# ====================================================
