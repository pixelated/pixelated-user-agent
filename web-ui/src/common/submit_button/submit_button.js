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
import RaisedButton from 'material-ui/RaisedButton';

import './submit_button.scss';

const labelStyle = {
  textTransform: 'none',
  fontSize: '1em',
  lineHeight: '48px'
};

const buttonStyle = {
  height: '48px'
};

const SubmitButton = ({ buttonText, disabled = false }) => (
  <div className='submit-button'>
    <RaisedButton
      type='submit'
      label={buttonText}
      disabled={disabled}
      labelStyle={labelStyle}
      buttonStyle={buttonStyle}
      overlayStyle={buttonStyle}
      fullWidth
      primary
    />
  </div>
);

SubmitButton.propTypes = {
  buttonText: React.PropTypes.string.isRequired,
  disabled: React.PropTypes.bool
};

SubmitButton.defaultProps = {
  disabled: false
};

export default SubmitButton;
