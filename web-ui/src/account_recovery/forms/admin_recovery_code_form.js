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

import './admin_recovery_code_form.scss';


export const AdminRecoveryCodeForm = ({ t }) => (
  <div>
    <h1>{t('account-recovery.admin-form.title')}</h1>
    <ul>
      <li>{t('account-recovery.admin-form.tip1')}</li>
      <li>{t('account-recovery.admin-form.tip2')}</li>
      <li>{t('account-recovery.admin-form.tip3')}</li>
    </ul>
    <InputField name='admin-code' label={t('account-recovery.admin-form.input-label')} />
    <SubmitButton buttonText={t('account-recovery.admin-form.button')} />
  </div>
);

AdminRecoveryCodeForm.propTypes = {
  t: React.PropTypes.func.isRequired
};

export default translate('', { wait: true })(AdminRecoveryCodeForm);
