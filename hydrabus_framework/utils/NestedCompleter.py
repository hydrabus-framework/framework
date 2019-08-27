from prompt_toolkit.completion import Completion, Completer


__author__ = "Jordan Ovrè <ghecko78@gmail.com>"


class NestedCompleter(Completer):

    def __init__(self, words_dic=None, meta_dict=None, ignore_case=True, match_middle=True):
        if meta_dict is None:
            meta_dict = {}
        if words_dic is None:
            words_dic = {}
        self.ignore_case = ignore_case
        self.match_middle = match_middle
        self.words_dic = words_dic
        self.meta_dict = meta_dict
        pass

    def get_completions(self, document, complete_event):
        text_before_cursor = document.text_before_cursor
        if self.ignore_case:
            text_before_cursor = text_before_cursor.lower()

        text_before_cursor = str(text_before_cursor)
        text_arr = text_before_cursor.split(' ')
        last_words = text_arr[-1]
        words = self.__get_current_words(text_arr[:-1])

        def word_matches(word):
            """ True when the word before the cursor matches. """
            if self.ignore_case:
                word = word.lower()

            if self.match_middle:
                return last_words in word
            else:
                return word.startswith(last_words)

        for a in words:
            if word_matches(a):
                display_meta = self.meta_dict.get(a, '')
                yield Completion(a, -len(last_words), display_meta=display_meta)

    def __get_current_words(self, text_arr):
        current_dic = self.words_dic
        for tmp in text_arr:
            if tmp == ' ' or tmp == '':
                continue
            try:
                if tmp in current_dic.keys():
                    current_dic = current_dic[tmp]
                else:
                    return []
            except:
                return []
        return list(current_dic)
