import { shallow } from 'enzyme';
import expect from 'expect';
import React from 'react';
import SnackbarNotification from 'src/common/snackbar_notification/snackbar_notification';
import Snackbar from 'material-ui/Snackbar';
import { red500 } from 'material-ui/styles/colors';

describe('SnackbarNotification', () => {
  let snackbarNotification;

  beforeEach(() => {
    snackbarNotification = shallow(<SnackbarNotification message={'Error Message'} isError />);
  });

  it('renders snackbar with error message', () => {
    expect(snackbarNotification.find(Snackbar).props().message).toEqual('Error Message');
  });

  it('renders snackbar with open as true', () => {
    expect(snackbarNotification.find(Snackbar).props().open).toEqual(true);
  });

  it('renders snackbar with error body style', () => {
    expect(snackbarNotification.find(Snackbar).props().bodyStyle)
      .toEqual({ height: 'auto', backgroundColor: red500 });
  });

  it('renders snackbar with default auto-hide duration', () => {
    expect(snackbarNotification.find(Snackbar).props().autoHideDuration).toEqual(5000);
  });
});
