import {shallow} from 'enzyme'
import expect from 'expect'
import React from 'react'
import Page from '../../../app/js/account_recovery/page'

describe('test', () => {
  'use strict';
  it('react', () => {
    const page = shallow(<Page />);
    expect(page.find('h1').text()).toEqual('E se você esquecer sua senha?');
  });
});
