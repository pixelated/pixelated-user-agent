import {shallow} from 'enzyme'
import React from 'react'
import Page from '../../../app/js/account_recovery/page'

describe('test', () => {
  'use strict';
  it('react', () => {
    const page = shallow(<Page />);
    expect(page.find('h1').text()).toEqual('Hello world');
  });
});
