import json

import configure


class VectorInfo:
    noun_dict = dict()
    selected_news_vector = []
    banned_news_vector = []

    @staticmethod
    def save():
        new_vec = dict({
            'selected': VectorInfo.selected_news_vector,
            'banned': VectorInfo.banned_news_vector
        })

        with open(configure.nouns_dict_filename, 'w+') as f:
            # Save news vectors
            json.dump(VectorInfo.noun_dict, f)

        with open(configure.news_vector_filename, 'w+') as f:
            # Save news vectors
            json.dump(new_vec, f)

    @staticmethod
    def load():
        with open(configure.nouns_dict_filename, 'r') as f:
            json_dict = json.load(f)

            VectorInfo.noun_dict = dict(json_dict)

        with open(configure.news_vector_filename, 'r') as f:
            json_dict = json.load(f)

            VectorInfo.selected_news_vector = json_dict['selected']
            VectorInfo.banned_news_vector = json_dict['banned']

    @staticmethod
    def append(news_vector, news_type: str = 'selected'):
        if type(news_vector) is dict:
            VectorInfo._append(news_vector, news_type)
        elif type(news_vector) is not list:
            raise TypeError('`append_target_news` needs list() or dict().')

        for news in news_vector:
            VectorInfo._append(news, news_type)

    @staticmethod
    def _append(news_vector: dict, news_type: str = 'selected'):
        if news_type is 'selected':
            for k, v in news_vector.items():
                if k not in VectorInfo.noun_dict:
                    VectorInfo.noun_dict[k] = len(VectorInfo.noun_dict)
                VectorInfo.selected_news_vector[VectorInfo.noun_dict[k]] = v
        elif news_type is 'banned':
            for k, v in news_vector.items():
                if k not in VectorInfo.noun_dict:
                    VectorInfo.noun_dict[k] = len(VectorInfo.noun_dict)
                VectorInfo.banned_news_vector[VectorInfo.noun_dict[k]] = v
