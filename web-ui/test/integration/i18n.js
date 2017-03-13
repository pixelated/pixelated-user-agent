import i18n from 'i18next';
import translations from '../../app/locales/en_US/translation.json';

i18n
  .init({
    lng: 'en',
    resources: {
      en: {
        translation: translations
      }
    }
  });

export default i18n;
