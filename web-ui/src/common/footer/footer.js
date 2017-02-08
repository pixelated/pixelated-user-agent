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
import './footer.scss';

export const Footer = ({ t }) => (
  <footer className='footer-wrapper'>
    <div className='footer-content'>
      <img className='footer-image' src='/assets/images/lab.svg' alt='' />
      <div>
        {t('footer-text')}
        <a className='footer-link' href='mailto:team@pixelated-project.org'>
          {' team@pixelated-project.org'}
        </a>
      </div>
    </div>
  </footer>
);

Footer.propTypes = {
  t: React.PropTypes.func.isRequired
};

export default translate('', { wait: true })(Footer);
