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
        sanitized_query = re.sub(r"['\"]", "", query.encode('utf8'))
        scanner = StringScanner(sanitized_query)
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

        return compiled
