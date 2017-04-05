import { shallow } from 'enzyme';
import expect from 'expect';
import React from 'react';
import LinkButton from 'src/common/link_button/link_button';
import { BackupAccountStep } from './backup_account_step';

describe('BackupAccountStep', () => {
  let backupAccountStep;

  beforeEach(() => {
    const mockTranslations = key => key;
    backupAccountStep = shallow(<BackupAccountStep t={mockTranslations} />);
  });

  it('renders title for backup account step', () => {
    expect(backupAccountStep.find('h1').text()).toEqual('account-recovery.backup-account-step.title');
  });

  it('renders submit button with given href', () => {
    expect(backupAccountStep.find(LinkButton).props().href).toEqual('/backup-account');
  });

  it('renders submit button with given button text', () => {
    expect(backupAccountStep.find(LinkButton).props().buttonText)
      .toEqual('account-recovery.backup-account-step.buttonText');
  });
});
