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
import browser from 'helpers/browser';

import SubmitFlatButton from 'src/common/flat_button/flat_button';

export class Logout extends React.Component {

  constructor(props) {
    super(props);
    this.state = { csrf_token: browser.getCookie('XSRF-TOKEN') };
  }

  render() {
    const t = this.props.t;
    return (
      <div className='logout-container'>
        <form id='logout-form' method='POST' action='logout'>
          <input type='hidden' name='csrftoken' value={this.state.csrf_token} />
          <SubmitFlatButton name="logout" buttonText={t('logout')} fontIconClass='fa fa-sign-out' />
        </form>
      </div>
    );
  }
}

Logout.propTypes = {
  t: React.PropTypes.func.isRequired
};

export default translate('', { wait: true })(Logout);
