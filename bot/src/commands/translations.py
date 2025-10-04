import i18n

class Translations:

    def __init__(self):
        i18n.set('locale', 'pl')
        i18n.set('fallback', 'en')
        i18n.set('filename_format', '{locale}.{format}')
        i18n.load_path.append('src/commands/translations')
    
    def t(self, key: str, language) -> str:
        return i18n.t(key, locale=language.lower())