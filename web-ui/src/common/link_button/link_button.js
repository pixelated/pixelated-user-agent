/*
 * Copyright (c) 2017 ThoughtWorks, Inc.
 *
 * Pixelated is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Affero General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * Pixelated is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU Affero General Public License for more details.
 *
 * You should have received a copy of the GNU Affero General Public License
 * along with Pixelated. If not, see <http://www.gnu.org/licenses/>.
 */

import React from 'react';
import FlatButton from 'material-ui/FlatButton';

import './link_button.scss';

const labelStyle = {
  textTransform: 'none',
  color: 'inherit',
  fontSize: 'inherit',
  width: '100%',
  padding: '0'
};

const linkButtonStyle = {
  color: 'inherit',
  borderRadius: '0',
  minHeight: '36px',
  height: 'auto',
  lineHeight: '20px',
  padding: '12px 0'
};

const LinkButton = ({ buttonText, href }) => (
  <div className='link-button'>
    <FlatButton
      href={href}
      containerElement='a'
      label={buttonText}
      labelStyle={labelStyle}
      hoverColor={'#ff9c00'}
      style={linkButtonStyle}
    />
  </div>
);

LinkButton.propTypes = {
  buttonText: React.PropTypes.string.isRequired,
  href: React.PropTypes.string.isRequired
};

export default LinkButton;
