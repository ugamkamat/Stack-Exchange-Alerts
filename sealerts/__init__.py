# standard library
import time

# 3rd party modules
import requests
from bs4 import BeautifulSoup
from win10toast import ToastNotifier

def isnew(array_new, array_old):
    new = False if array_new == array_old else True
    for i in range(len(array_new)):
        if array_new[i] == array_old[0]:
            break
    return new, i

class alertnotify:
    def __init__(self, rss_link, file_name_with_path):
        self.rss_link = rss_link
        self.file_name_with_path = file_name_with_path
        self.title_r = []
        self.link_r = []
        self.summary_r = []

    def get_current_data(self):
        page = requests.get(self.rss_link)
        soup = BeautifulSoup(page.content, 'html.parser')
        title_all = soup.find_all('title')
        link_all = soup.find_all('link')
        summary_all = soup.find_all('summary')

        title, link, summary = [],[],[]
        for elements in title_all:
            title.append(elements.get_text())
        
        for elements in link_all:
            link.append(elements.get('href'))

        for elements in summary_all:
            summary_list = elements.get_text().split()
            summary_list[0] = summary_list[0][3:]
            count = 0
            for summ in summary_list:
                if summ.endswith('</p>'):
                    break
                count += 1
            try:
                summary_list[count] = summary_list[count][:-4]
                summary.append(' '.join(summary_list[:(count+1)]))
            except IndexError:
                continue
        return title[1:], link[2:], summary

    def initialize_data_file(self):
        title = alertnotify.get_current_data(self)[0]
        with open(self.file_name_with_path, 'w') as f:
            for i in range(len(title)):
                f.write(title[i] + '\n')
            f.close()

    def update_data_file(self):
        title_new, link_new, summary_new = alertnotify.get_current_data(self)
        
        with open(self.file_name_with_path, 'r') as f:
            data = f.readlines()
            f.close()
        
        title_old = []
        for i in range(len(data)):
            title_old.append(data[i].split('\t')[0].rstrip())

        if isnew(title_new, title_old)[0]:
            with open(self.file_name_with_path, 'w') as f:
                for i in range(len(title_new)):
                    f.write(title_new[i] + '\n')
                f.close()
        
            for i in range(isnew(title_new, title_old)[1]):
                self.title_r.append(title_new[i])
                self.link_r.append(link_new[i])
                self.summary_r.append(summary_new[i])

    def send_notification(self):
        alertnotify.update_data_file(self)
        for i in range(len(self.title_r)):
            ToastNotifier().show_toast(self.title_r[i], self.summary_r[i], icon_path=None, duration=10, threaded=True)
            # Wait for threaded notification to finish
            while ToastNotifier().notification_active():
                time.sleep(0.1)

def main(rss_link, file_name_with_path):
    while True:
        alerts = alertnotify(rss_link, file_name_with_path)
        try:
            alerts.send_notification()
        
        except FileNotFoundError:
            alerts.initialize_data_file()
        
        time.sleep(300)