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

import './pixelated-welcome.scss';

export const PixelatedWelcome = ({ t }) => (
  <div className='pixelated-welcome'>
    <img className='welcome-logo' src='/public/images/welcome.svg' alt={t('login.welcome-image-alt')} />
    <div>
      <h3>{t('login.welcome-message')}</h3>
    </div>
  </div>
);

PixelatedWelcome.propTypes = {
  t: React.PropTypes.func.isRequired
};

export default translate('', { wait: true })(PixelatedWelcome);
