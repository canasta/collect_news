class SearchKeyword:
    def __init__(self, keyword: str):
        self.main_keyword = keyword
        self.sub_keyword = []
        self.excluded_keyword = []

    def __str__(self):
        sub_key_str = ' '.join(self.sub_keyword)
        excluded_key_str = ' -'.join(self.sub_keyword)
        return f'{self.main_keyword} {sub_key_str} -{excluded_key_str}'

    def add_key(self, keyword: str):
        self.sub_keyword.append(keyword)

    def add_keys(self, key_list: list):
        self.sub_keyword.extend(key_list)

    def exclude_key(self, keyword: str):
        self.excluded_keyword.append(keyword)

    def exclude_keys(self, key_list: list):
        self.excluded_keyword.extend(key_list)
