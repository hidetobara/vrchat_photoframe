import gspread
from oauth2client.service_account import ServiceAccountCredentials 


class Item:
    def __init__(self, name, url, title) -> None:
        self.name = name
        self.url = url
        self.title = title

    def is_valid(self):
        return len(self.name) > 0 and len(self.url) > 0 and self.url.startswith("https://")

    def to_csv(self):
        return [self.name, self.url, self.title]

class Sheet:
    def __init__(self, key):
        scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
        credentials = ServiceAccountCredentials.from_json_keyfile_name('./private/vrchat-analyzer-ba2bcb1497e6.json', scope)
        self.gc = gspread.authorize(credentials)
        self.key = key

    def load(self, worksheet) -> dict:
        worksheet = self.gc.open_by_key(self.key).worksheet(worksheet)
        table = {}
        for row in worksheet.get_all_values():
            i = Item(row[0], row[1], row[2])
            if not i.is_valid(): continue

            table[i.name] = i
        return table
