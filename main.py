import os
import json
from google.cloud import storage
from google.oauth2 import service_account
import google.auth.transport.requests
from datetime import timedelta, datetime
#import pandas as pd
import flet as ft
#from simpledt import DataFrame
#import openpyxl

bucket_name_out = 'vfm-calc-output'
bucket_name_in = 'vfmcalc-inputs'
excel_file_name = 'VFM_result_sheet_2025-02-23_18_07_00.xlsx'
excel_file_path = os.path.join("/mnt/gcs", excel_file_name)
service_account_file_name = 'vfmcalc-fa8593ca8d16.json'
service_account_file_path = os.path.join("/mnt/gcs2", service_account_file_name)
#credentials, project_id  = google.auth.default()
#credentials.refresh(google.auth.transport.requests.Request())

def create_credentials():
    #service_account_info = json.loads(str(service_account_key))
    #service_account_info = service_account_key
    credentials = service_account.Credentials.from_service_account_file(service_account_file_path)
    #scoped_credentials = credentials
    #credentials = service_account.Credentials.from_service_account_json(service_account_info)
    scoped_credentials = credentials.with_scopes(
        [
            'https://www.googleapis.com/auth/cloud-platform',
            #'https://www.googleapis.com/auth/devstorage.read_write',
            #'https://www.googleapis.com/auth/devstorage.full_control',
            #'https://www.googleapis.com/auth/analytics.readonly',
        ])

    return scoped_credentials

scoped_credentials = create_credentials()

# list of blob in the bucket
#def list_blobs(scoped_credentials, bucket_name):
#    storage_client = storage.Client(credentials=scoped_credentials)
#    #storage_client = storage.Client()
#    bucket = storage_client.bucket(bucket_name)
#    blobs = bucket.list_blobs()
#
#    return blobs

#　上記のファイルについて署名付きURLを生成
def generate_signed_url(scoped_credentials, bucket_name, file_name):
    storage_client = storage.Client(credentials=scoped_credentials, project=scoped_credentials.project_id)
    #storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(file_name)
    #blob = bucket.(bucket_name)
    url = blob.generate_signed_url(
        version = 'v4',
        expiration = timedelta(hours=1),
        method = 'GET',
        service_account_email = scoped_credentials.service_account_email,
        access_token = scoped_credentials.token,
    )
    return url

# 上記のファイルについて署名付きURLを表示するダイアログを表示する

def main(page: ft.Page):
    page.title = "署名付きURL表示"

    def show_signed_url(scoped_credentials, bucket_name, file_name):
        url = generate_signed_url(scoped_credentials, bucket_name, file_name)
        dialog =  ft.AlertDialog(
            title=ft.Text("ダウンロードURL"),
            content=ft.Column([
                ft.Text(url, selectable=True),
                ft.Text("上記のURLから出力したExcelファイルをダウンロードできます。"),
                ft.ElevatedButton("ダウンロード", on_click=lambda _: page.launch_url(url)),
            ]),
            open=True,
            on_dismiss=lambda e: print("Dialog dismissed!"),
        )
        #page.add(dialog)
        page.dialog = dialog
        #dialog.open = True
        page.add(ft.Text(url, selectable=True))
        #page.update()

    show_signed_url(scoped_credentials, bucket_name_out, excel_file_name)

    #show_signed_url()
    page.update()


ft.app(target=main, view=ft.AppView.WEB_BROWSER)
