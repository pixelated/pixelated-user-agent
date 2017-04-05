import { shallow } from 'enzyme';
import expect from 'expect';
import React from 'react';
import LinkButton from 'src/common/link_button/link_button';

describe('LinkButton', () => {
  let linkButton;

  beforeEach(() => {
    linkButton = shallow(<LinkButton buttonText='Go To Link' href='/some-link' />);
  });

  it('renders link button with given button text', () => {
    expect(linkButton.find('RaisedButton').props().label).toEqual('Go To Link');
  });

  it('renders link button with given href', () => {
    expect(linkButton.find('RaisedButton').props().href).toEqual('/some-link');
  });
});
