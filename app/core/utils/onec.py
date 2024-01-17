import os
from ftplib import FTP

HOST = os.getenv("FTP_HOST")
USER = os.getenv("FTP_HOST_USER")
PASSWORD = os.getenv("FTP_HOST_PASSWORD")


def get_ftp():
    return FTP(HOST, USER, PASSWORD)
