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

import { submitForm } from 'src/common/util';
import InputField from 'src/common/input_field/input_field';
import SubmitButton from 'src/common/submit_button/submit_button';
import BackLink from 'src/common/back_link/back_link';

import './new_password_form.scss';

export class NewPasswordForm extends React.Component {
  submitHandler = (event) => {
    submitForm(event, '/account-recovery', {
      userCode: this.props.userCode,
      password: this.state.password,
      confirmation: this.state.confirmation
    });
  }

  handlePasswordChange = (event) => {
    this.setState({ password: event.target.value });
  }

  handlePasswordConfirmationChange = (event) => {
    this.setState({ confirmation: event.target.value });
  }

  render() {
    const { t, previous } = this.props;
    return (
      <form className='account-recovery-form new-password' onSubmit={this.submitHandler}>
        <img
          className='account-recovery-progress'
          src='/public/images/account-recovery/step_3.svg'
          alt={t('account-recovery.new-password-form.image-description')}
        />
        <h1>{t('account-recovery.new-password-form.title')}</h1>
        <InputField
          type='password' name='new-password'
          label={t('account-recovery.new-password-form.input-label1')}
          onChange={this.handlePasswordChange}
        />
        <InputField
          type='password' name='confirm-password'
          label={t('account-recovery.new-password-form.input-label2')}
          onChange={this.handlePasswordConfirmationChange}
        />
        <SubmitButton buttonText={t('account-recovery.button-next')} />
        <BackLink text={t('account-recovery.back')} onClick={previous} />
      </form>
    );
  }
}

NewPasswordForm.propTypes = {
  t: React.PropTypes.func.isRequired,
  previous: React.PropTypes.func.isRequired,
  userCode: React.PropTypes.string.isRequired
};

export default translate('', { wait: true })(NewPasswordForm);