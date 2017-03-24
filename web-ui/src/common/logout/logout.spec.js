import { shallow } from 'enzyme';
import expect from 'expect';
import React from 'react';
import { Logout } from 'src/common/logout/logout';

describe('Logout', () => {
  let logout;

  beforeEach(() => {
    const mockTranslations = key => key;
    logout = shallow(<Logout t={mockTranslations} fontIconClass='fa fa-sign-out' />);
  });

  it('renders the logout container', () => {
    expect(logout.find('div.logout-container')).toExist();
  });

  describe('logout form', () => {
    let logoutForm;

    beforeEach(() => {
      logoutForm = logout.find('form#logout-form');
    });

    it('renders logout form', () => {
      expect(logoutForm).toExist();
    });

    it('renders logout form with POST method', () => {
      expect(logoutForm.props().method).toEqual('POST');
    });

    it('renders logout form with action as logout', () => {
      expect(logoutForm.props().action).toEqual('logout');
    });

    it('renders csrf hidden input', () => {
      expect(logoutForm.find('input[name="csrftoken"]')).toExist();
    });

    it('renders SubmitFlatButton for logout', () => {
      expect(logoutForm.find('SubmitFlatButton').props().buttonText).toEqual('logout');
    });

    it('renders SubmitFlatButton for logout with fontIcon', () => {
      expect(logoutForm.find('SubmitFlatButton').props().fontIconClass).toEqual('fa fa-sign-out');
    });
  });
});
