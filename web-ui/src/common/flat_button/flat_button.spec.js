import { shallow } from 'enzyme';
import expect from 'expect';
import React from 'react';
import FlatButton from 'src/common/flat_button/flat_button';

describe('FlatButton', () => {
  let flatButton;

  beforeEach(() => {
    flatButton = shallow(<FlatButton name='logout' buttonText='Logout' fontIconClass='fa fa-sign-out' />);
  });

  it('renders a FlatButton of type submit with name logout', () => {
    expect(flatButton.find('FlatButton').props().name).toEqual('logout');
  });

  it('renders a FlatButton of type submit with text logout', () => {
    expect(flatButton.find('FlatButton').props().label).toEqual('Logout');
  });

  it('renders a FlatButton of type submit with title logout', () => {
    expect(flatButton.find('FlatButton').props().title).toEqual('Logout');
  });

  it('renders a FlatButton of type submit with aria-label logout', () => {
    expect(flatButton.find('FlatButton').props()['aria-label']).toEqual('Logout');
  });

  it('renders a FlatButton with given fontIcon class', () => {
    expect(flatButton.find('FlatButton').props().icon.props.className).toEqual('fa fa-sign-out');
  });
});
