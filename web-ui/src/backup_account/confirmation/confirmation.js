/*
 * Copyright (c) 2017 ThoughtWorks, Inc.
 *
 * Pixelated is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Affero General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * Pixelated is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU Affero General Public License for more details.
 *
 * You should have received a copy of the GNU Affero General Public License
 * along with Pixelated. If not, see <http://www.gnu.org/licenses/>.
 */

import React from 'react';
import { translate } from 'react-i18next';
import SubmitButton from 'src/common/submit_button/submit_button';
import BackLink from 'src/common/back_link/back_link';

import './confirmation.scss';

export const Confirmation = ({ t }) => (
  <div className='container confirmation-container'>
    <h1>{t('backup-account.confirmation.title1')} <br /> {t('backup-account.confirmation.title2')}</h1>
    <p>{t('backup-account.confirmation.paragraph')}</p>
    <img src='/public/images/sent-mail.svg' alt='Sent mail' />
    <form action='/'>
      <SubmitButton buttonText={t('backup-account.confirmation.button')} type='submit' />
    </form>
    <BackLink
      href='/backup-account'
      text={t('backup-account.confirmation.retry-button')}
    />
  </div>
);

Confirmation.propTypes = {
  t: React.PropTypes.func.isRequired
};

export default translate('', { wait: true })(Confirmation);
