import zipfile

if __name__ == '__main__':
    with zipfile.ZipFile('dataset.zip') as dataset_zip:
        dataset_zip.extractall()
