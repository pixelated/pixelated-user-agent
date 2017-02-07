import React from 'react'
import { translate } from 'react-i18next'

import './page.scss'

export const Page = ({ t }) => (
  <div className='container'>
    <img src='assets/images/forgot-my-password.svg' alt={t('backup-account.image-description')}/>
    <form>
      <h1>{t('backup-account.title')}</h1>
      <p>{t('backup-account.paragraph1')}</p>
      <p>{t('backup-account.paragraph2')}</p>
      <div className="field-group">
        <input type="text" name="email" className="email" required/>
        <label className="animated-label" htmlFor="email">{t('backup-account.input-label')}</label>
      </div>
      <button>{t('backup-account.button')}</button>
      <div>
        <a href="/">
          <i className="fa fa-angle-left" aria-hidden="true"></i>
          <span>{t('back-to-inbox')}</span>
        </a>
      </div>
    </form>
  </div>
)

export default translate('', { wait: true })(Page)
