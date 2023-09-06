import os
import requests
import zipfile
import io
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QMessageBox, QPushButton


class Downloader(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('R3nzSkin Downloader')
        self.resize(400, 200)
        self.btn_download = QPushButton('请选择英雄联盟文件夹下的Game文件夹', self)
        self.btn_download.setGeometry(80, 80, 300, 30)
        self.btn_download.clicked.connect(self.download)

        self.show()

    def download(self):
        # Get the download URL
        url = "https://api.github.com/repos/R3nzTheCodeGOD/R3nzSkin/releases/latest"
        response = requests.get(url)
        release = response.json()
        download_url = release["assets"][0]["browser_download_url"]
        download_url = download_url.replace("https://", "https://ghproxy.com/")

        # Open file dialog to select download location
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.DirectoryOnly)
        if dialog.exec_():
            directory = dialog.selectedFiles()[0]
            try:
                # Download the zip file
                zip_response = requests.get(download_url)
                zip_file = io.BytesIO(zip_response.content)

                # Extract the contents of the zip file
                with zipfile.ZipFile(zip_file, 'r') as zip_ref:
                    zip_ref.extractall(directory)
                os.remove(os.path.join(directory, 'R3nzSkin_Injector.exe'))
                # Rename R3nzSkin.dll to hid.dll and copy to Game folder
                original_file = os.path.join(directory, 'R3nzSkin.dll')
                if(os.path.exists(os.path.join(directory, 'hid.dll'))):
                    os.remove(os.path.join(directory, 'hid.dll'))
                new_file = os.path.join(directory, 'hid.dll')
                os.rename(original_file, new_file)

                QMessageBox.information(self, '成功', '下载和安装完成！')
            except Exception as e:
                QMessageBox.critical(self, '错误', f'下载和安装失败：{str(e)}')
        else:
            QMessageBox.warning(self, '警告', '未选择下载位置！')


if __name__ == '__main__':
    app = QApplication([])
    window = Downloader()
    app.exec_()
