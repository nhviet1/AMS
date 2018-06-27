import configparser
import MySQLdb
import log_writer


# ==========Function: Connect to database=============
# Arguments:            [1]
# Arguments:    [FTP Folder Path]
# GET DATABASE CONNECTION
def get_conn():
    config = configparser.ConfigParser()
    config.sections()
    config.read("config.ini")
    config.sections()

    host = str(config["AMS_SERVER"]["server_name"])
    user = str(config["AMS_SERVER"]["user_name"])
    password = str(config["AMS_SERVER"]["password"])
    db = str(config["AMS_SERVER"]["db_name"])

    db = MySQLdb.connect(host=host, user=user, passwd=password, db=db)
    return db
# ====================================================


# ===========Function: Update media's info into "MEDIA_TEMP" table==============
# Arguments:      [1]           [2]          [3]          [4]
# Arguments: [Camera Name]  [File Size]  [From Name]  [To Name]
def media_temp_insert(cam_name, file_size, original_name, to_name):
    query = "INSERT INTO `media_temp`( `camName`, `fileSize`, `fromName`, `toName`) " \
            "VALUES ('" + str(cam_name) + "','" + str(file_size) + "','" \
            + str(original_name) + "','" + str(to_name) + "')"

    # Connect database
    db = get_conn()

    # Create a Cursor object to execute queries.
    cur = db.cursor()

    # Insert into database
    try:
        # log_writer.write_log("Insert media temp into database.")
        cur.execute(query)
        db.commit()
    except:
        log_writer.write_log("Insert error!")
        db.rollback()

    # Close connection
    db.close()
# ==================================================================


# ===========Function: Clear "MEDIA_TEMP" table==============
# Arguments:
# Arguments:
def clear_media_temp():
    query = "TRUNCATE TABLE media_temp"
    # Connect database
    db = get_conn()

    # Create a Cursor object to execute queries.
    cur = db.cursor()

    # Insert into database
    try:
        cur.execute(query)
        db.commit()
    except:
        db.rollback()

    # Close connection
    db.close()
# ===========================================================


# ===========Function: Clear streaming media==============
# Arguments:
# Arguments:
def clear_streaming_media():
    query = "SELECT `fromName` FROM `media_temp` WHERE 1"
    db = get_conn()
    cur = db.cursor()
    cur.execute(query)
    rows = cur.fetchall()
    for row in rows:
        print(row[0])
        media_delete_query = "DELETE FROM `media` WHERE `originalFilename` = \"" + row[0] + "\""
        try:
            cur.execute(media_delete_query)
            db.commit()
        except:
            db.rollback()

        media_temp_delete_query = "DELETE FROM `media_temp` WHERE `fromName` = \"" + row[0] + "\""
        try:
            cur.execute(media_temp_delete_query)
            db.commit()
        except:
            db.rollback()
    db.close()
# ========================================================


