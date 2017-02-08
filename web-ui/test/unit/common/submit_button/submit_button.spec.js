import { shallow } from 'enzyme';
import expect from 'expect';
import React from 'react';
import SubmitButton from 'src/common/submit_button/submit_button';

describe('SubmitButton', () => {
  let submitButton;

  beforeEach(() => {
    submitButton = shallow(<SubmitButton buttonText='Add Email' />);
  });

  it('renders an input of type submit for add email', () => {
    expect(submitButton.find('input[type="submit"]').props().value).toEqual('Add Email');
  });
});
