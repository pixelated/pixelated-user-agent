import { shallow } from 'enzyme';
import expect from 'expect';
import React from 'react';
import { Header } from 'src/common/header/header';
import Logout from 'src/common/logout/logout';

describe('Header', () => {
  let header;

  beforeEach(() => {
    header = shallow(<Header />);
  });

  it('renders the header containing the logout button', () => {
    expect(header.find('header').find(Logout)).toExist();
  });

  it('renders the header pixelated logo', () => {
    expect(header.find('header').find('img').props().alt).toEqual('Pixelated');
  });
});
