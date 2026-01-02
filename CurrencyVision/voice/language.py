import yaml

class LanguageManager:
    def __init__(self, language_code="en"):
        with open("config/languages.yaml", encoding="utf-8") as f:
            self.languages = yaml.safe_load(f)

        if language_code not in self.languages:
            raise ValueError("Language not supported")

        self.lang = self.languages[language_code]

    def detected_text(self, value):
        return self.lang["detected"].format(value=value)

    def total_text(self, total):
        return self.lang["total"].format(total=total)
