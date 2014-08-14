from scanner import StringScanner, StringRegexp
import re


def _next_token():
    return StringRegexp('[^\s]+')   


def _separators():             
    return StringRegexp('[\s&]+')   


def _compile_tag(compiled, token):
    tag = token.split(":").pop()    
    if token[0] == "-":        
        compiled["not_tags"].append(tag)
    else:                      
        compiled["tags"].append(tag)    
    return compiled            


class SearchQuery:

    @staticmethod
    def compile(query):
        compiled = {"tags": [], "not_tags": [], "general":[]}

        scanner = StringScanner(query.encode('utf8').replace("\"", ""))
        first_token = True
        while not scanner.is_eos:
            token = scanner.scan(_next_token())

            if not token:
                scanner.skip(_separators())
                continue

            if ":" in token:
                compiled = _compile_tag(compiled, token)
            elif first_token:
                compiled["general"].append(token)

            if not first_token:
                first_token = True

        compiled["general"] = ' '.join(compiled["general"])
        return SearchQuery(compiled)

    def __init__(self, compiled):
        self.compiled = compiled

    def test(self, mail):
        if set(self.compiled.get('not_tags')).intersection(set(mail.tags)):
            return False

        if set(self.compiled.get('tags')).intersection(set(mail.tags)) or 'all' in self.compiled.get('tags'):
            return True

        if self.compiled.get('general'):
            search_terms = re.compile(self.compiled['general'], flags=re.IGNORECASE)
            if search_terms.search(mail.body) or search_terms.search(mail.subject):
                return True

        if not [v for v in self.compiled.values() if v]:
            return True


        return False

    

