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
import Footer from 'src/common/footer/footer';
import Header from 'src/common/header/header';
import BackupEmail from 'src/backup_account/backup_email/backup_email';
import Confirmation from 'src/backup_account/confirmation/confirmation';
import SnackbarNotification from 'src/common/snackbar_notification/snackbar_notification';

import 'font-awesome/scss/font-awesome.scss';
import './page.scss';


export class Page extends React.Component {

  constructor(props) {
    super(props);
    this.state = { status: '' };
  }

  saveBackupEmail = (status) => {
    this.setState({ status });
  };

  mainContent = () => {
    if (this.state.status === 'success') return <Confirmation />;
    return <BackupEmail onSubmit={this.saveBackupEmail} />;
  };

  showSnackbarOnError = (t) => {
    if (this.state.status === 'error') {
      return <SnackbarNotification message={t('backup-account.error.submit-error')} isError />;
    }
    return undefined; // To satisfy eslint error - consistent-return
  };

  render() {
    const t = this.props.t;
    return (
      <DocumentTitle title={t('backup-account.page-title')}>
        <div className='page'>
          <Header />
          <section>
            {this.mainContent()}
          </section>
          {this.showSnackbarOnError(t)}
          <Footer />
        </div>
      </DocumentTitle>
    );
  }
}


Page.propTypes = {
  t: React.PropTypes.func.isRequired
};

export default translate('', { wait: true })(Page);
