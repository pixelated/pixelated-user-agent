import { shallow } from 'enzyme';
import expect from 'expect';
import React from 'react';
import InputField from 'src/common/input_field/input_field';

describe('InputField', () => {
  let inputField;

  beforeEach(() => {
    inputField = shallow(<InputField label='Email' name='email' />);
  });

  it('renders an input of type text for email', () => {
    expect(inputField.find('input[type="text"]').props().name).toEqual('email');
  });

  it('renders a label for the email', () => {
    expect(inputField.find('label').text()).toEqual('Email');
  });
});
