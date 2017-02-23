import { shallow } from 'enzyme';
import expect from 'expect';
import React from 'react';
import { PixelatedWelcome } from 'src/login/about/pixelated_welcome';

describe('PixelatedWelcome', () => {
  let pixelatedWelcome;
  const mockTranslations = key => key;

  beforeEach(() => {
    pixelatedWelcome = shallow(<PixelatedWelcome t={mockTranslations} />);
  });

  it('renders welcome component', () => {
    expect(pixelatedWelcome.find('.pixelated-welcome').length).toEqual(1);
  });
});
