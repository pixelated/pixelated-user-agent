import { shallow } from 'enzyme';
import expect from 'expect';
import React from 'react';
import { BackupAccountStep } from './backup_account_step';
import SubmitButton from 'src/common/submit_button/submit_button';

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
    expect(backupAccountStep.find(SubmitButton).props().href).toEqual('/backup-account');
  });

  it('renders submit button with given container element', () => {
    expect(backupAccountStep.find(SubmitButton).props().containerElement).toEqual('a');
  });

  it('renders submit button with given button text', () => {
    expect(backupAccountStep.find(SubmitButton).props().buttonText)
      .toEqual('account-recovery.backup-account-step.buttonText');
  });
});
