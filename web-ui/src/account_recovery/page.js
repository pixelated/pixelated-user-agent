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
import DocumentTitle from 'react-document-title';
import Header from 'src/common/header/header';
import AdminRecoveryCodeForm from 'src/account_recovery/forms/admin_recovery_code_form';
import Footer from 'src/common/footer/footer';

import 'font-awesome/scss/font-awesome.scss';
import './page.scss';


export const Page = ({ t }) => (
  <DocumentTitle title={t('account-recovery.page-title')}>
    <div className='page'>
      <Header />
      <section>
        <div className='container'>
          <AdminRecoveryCodeForm />
        </div>
      </section>
      <Footer />
    </div>
  </DocumentTitle>
);

Page.propTypes = {
  t: React.PropTypes.func.isRequired
};

export default translate('', { wait: true })(Page);
