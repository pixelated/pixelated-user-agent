import { shallow } from 'enzyme';
import expect from 'expect';
import React from 'react';
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
});
