# ================Import Library=================
import os
import datetime
import configparser
import threading
# ===============================================


# ===================Threading Class===================
class RecorderThreading(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        while True:
            vlc()
# =====================================================


# ===========Function: Record Media from VLC==============
def vlc():
    config_reader = configparser.ConfigParser()
    config_reader.sections()
    config_reader.read("config.ini")
    config_reader.sections()

    v_dev = str(config_reader["VLC_RECORD"]["cam_name"])                # camera name
    a_dev = str(config_reader["VLC_RECORD"]["mic_name"])                # mic name
    duration = str(config_reader["VLC_RECORD"]["record_duration"])      # time recording - will lose some seconds
    frame_rate = str(config_reader["VLC_RECORD"]["frame_rate"])         # frame rate per second
    v_code = str(config_reader["VLC_RECORD"]["video_encode"])           # video encode
    vb = str(config_reader["VLC_RECORD"]["video_bit_rate"])             # video bit-rate
    a_code = str(config_reader["VLC_RECORD"]["audio_encode"])           # audio encode
    ab = str(config_reader["VLC_RECORD"]["audio_bit_rate"])             # audio bit-rate
    file_path = str(config_reader["VLC_RECORD"]["record_folder_path"])  # saving location
    file_ext = str(config_reader["VLC_RECORD"]["file_type"])            # video type/extension

    h = str(datetime.datetime.today().hour)
    m = str(datetime.datetime.today().minute)
    s = str(datetime.datetime.today().second)
    file_name = h + "-" + m + "-" + s

    command = 'vlc --no-repeat --no-loop --qt-start-minimized ' \
              '-vvv dshow:// '  \
              ' :dshow-vdev="' + v_dev + '"' \
              ' :dshow-adev="' + a_dev + '"' \
              ' --no-qt-error-dialogs ' \
              ' --run-time=' + duration + \
              ' --sout=#transcode{vcodec=' + v_code + \
              ',acodec=' + a_code + \
              ',ab=' + ab + ',vb=' + vb + \
              ',fps=' + frame_rate + \
              '}:file{dst=' + file_path + file_name + file_ext + '}' \
              ' vlc://quit'
    os.system(command)
# ========================================================
