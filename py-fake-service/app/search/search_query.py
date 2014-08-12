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
        compiled = {"tags": [], "not_tags": []}

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
                compiled["general"] = token     

            if not first_token:
                first_token = True              

        return SearchQuery(compiled)

    def __init__(self, compiled):
        self.compiled = compiled

    def test(self, mail):
        if set(self.compiled.get('tags')).intersection(mail.tags) or 'all' in self.compiled.get('tags'):
           return True

        if self.compiled.get('general'):
            search_terms = re.compile(self.compiled['general'])
            if search_terms.match(mail.body) or search_terms.match(mail.subject):
                return True

        if not self.compiled.get('tags') and not self.compiled.get('not_tags'):
            return True

        return False

    

