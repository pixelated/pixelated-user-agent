import React from 'react'
import { render } from 'react-dom'
import a11y from 'react-a11y'
import { I18nextProvider } from 'react-i18next'

import Page from 'js/account_recovery/page'
import i18n from 'js/account_recovery/i18n'

import 'font-awesome/scss/font-awesome.scss'

if(process.env.NODE_ENV === 'development') a11y(React);

render(
  <I18nextProvider i18n={ i18n }>
    <Page/>
  </I18nextProvider>,
  document.getElementById('root')
);
