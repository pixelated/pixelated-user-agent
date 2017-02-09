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
import './header.scss';

export const Header = ({ t }) => (
  <header className='header-wrapper'>
    <div className='header-content'>
      <img
        className='header-logo'
        src='/startup-assets/pixelated-logo-orange.svg'
        alt='Pixelated'
      />
      <div className='header-icons'>
        <a href='/'>
          <span>{t('logout')}</span>
          <i className='fa fa-sign-out' aria-hidden='true' />
        </a>
      </div>
    </div>
  </header>
);

Header.propTypes = {
  t: React.PropTypes.func.isRequired
};

export default translate('', { wait: true })(Header);
