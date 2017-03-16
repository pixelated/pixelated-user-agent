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

import 'isomorphic-fetch';
import React from 'react';
import { translate } from 'react-i18next';
import SubmitButton from 'src/common/submit_button/submit_button';
import InputField from 'src/common/input_field/input_field';
import validator from 'validator';
import browser from 'helpers/browser';

import './backup_email.scss';

export class BackupEmail extends React.Component {

  constructor(props) {
    super(props);
    this.state = { error: '', submitButtonDisabled: true };
  }

  validateEmail = (event) => {
    const validEmail = validator.isEmail(event.target.value);
    const emptyEmail = validator.isEmpty(event.target.value);
    const t = this.props.t;
    this.setState({
      error: !emptyEmail && !validEmail ? t('backup-account.backup-email.error.invalid-email') : '',
      submitButtonDisabled: !validEmail || emptyEmail
    });
  }

  submitHandler = (event) => {
    event.preventDefault();

    fetch('/backup-account', {
      credentials: 'same-origin',
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        csrftoken: [browser.getCookie('XSRF-TOKEN')]
      })
    }).then(() => this.props.onSubmit('success'));
  }

  render() {
    const t = this.props.t;
    return (
      <div className='container backup-email-container'>
        <img
          className='backup-account-image'
          src='/public/images/forgot-my-password.svg'
          alt={t('backup-account.backup-email.image-description')}
        />
        <form onSubmit={this.submitHandler}>
          <h1>{t('backup-account.backup-email.title')}</h1>
          <p>{t('backup-account.backup-email.paragraph1')}</p>
          <p>{t('backup-account.backup-email.paragraph2')}</p>
          <InputField name='email' label={t('backup-account.backup-email.input-label')} errorText={this.state.error} onChange={this.validateEmail} />
          <SubmitButton buttonText={t('backup-account.backup-email.button')} disabled={this.state.submitButtonDisabled} />
          <div className='link-content'>
            <a href='/' className='link'>
              <i className='fa fa-angle-left' aria-hidden='true' />
              <span>{t('back-to-inbox')}</span>
            </a>
          </div>
        </form>
      </div>
    );
  }
}


BackupEmail.propTypes = {
  t: React.PropTypes.func.isRequired,
  onSubmit: React.PropTypes.func.isRequired
};

export default translate('', { wait: true })(BackupEmail);
