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
import InputField from 'src/common/input_field/input_field';
import SubmitButton from 'src/common/submit_button/submit_button';
import AuthError from 'src/login/error/auth_error';
import GenericError from 'src/login/error/generic_error';
import Welcome from 'src/login/about/welcome';

import './page.scss';

const errorMessage = (t, authError) => {
  if (authError) return <AuthError />;
  return <div />;
};

const rightPanel = (t, error) => {
  if (error) return <GenericError />;
  return <Welcome />;
};

export const Page = ({ t, authError, error }) => (
  <div className='login'>
    <img
      className={error ? 'logo small-logo' : 'logo'}
      src='/public/images/logo-orange.svg'
      alt='Pixelated logo'
    />
    {rightPanel(t, error)}
    <form className='standard' id='login_form' action='/login' method='post' noValidate>
      {errorMessage(t, authError)}
      <InputField name='username' label={t('login.email')} autoFocus />
      <InputField type='password' name='password' label={t('login.password')} />
      <SubmitButton buttonText={t('login.submit')} />
    </form>
  </div>
);

Page.propTypes = {
  t: React.PropTypes.func.isRequired,
  authError: React.PropTypes.bool,
  error: React.PropTypes.bool
};

export default translate('', { wait: true })(Page);
