from bs4 import BeautifulSoup
import requests
import os
import shutil


class BundleScraper:
    def __init__(self, url, extension='', output_dir='', filename=''):
        self.url = url
        self.book_list = []
        self.title = ''
        self.soup = None
        self.extension = extension
        self.output_dir = output_dir
        self.filename = filename

    def request_soup(self):
        self.soup = BeautifulSoup(requests.get(self.url).content, "html.parser")

    def parse_soup(self):
        found = self.soup.find_all("span", {"class": "front-page-art-image-text"})
        title = self.soup.find_all("h3", class_="bundle-info-heading")[0].text
        self.title = title.replace(" ", "")
        for el in found:
            self.book_list.append(el.text)

    def export_list(self):
        with open(self.title.replace(" ", "_"), 'w') as output:
            toWrite = "\n".join(self.book_list)
            output.writelines(toWrite)

    def export_directory(self):
        if self.output_dir:
            export_dir = self.output_dir
        else:
            export_dir = self.title.replace(" ", "_")

        if self.filename:
            export_file = self.filename + self.extension
        else:
            export_file = self.title.replace(" ", "_") + '_List_Of_Contents' + self.extension

        try:
            os.mkdir(export_dir)
            with open(export_file, 'w') as output:
                toWrite = "\n".join(self.book_list)
                output.writelines(toWrite)
            shutil.move(export_file, export_dir)
        except OSError:
            print("Error creating directory" + export_dir)

    def __call__(self, *args, **kwargs):
        self.request_soup()
        self.parse_soup()
        self.export_directory()


s = BundleScraper("https://www.humblebundle.com")
s()

