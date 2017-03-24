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
import FontIcon from 'material-ui/FontIcon';
import { grey500 } from 'material-ui/styles/colors';

const labelStyle = {
  textTransform: 'none',
  verticalAlign: 'middle'
};

const iconStyle = {
  marginRight: 0
};

const flatButtonStyle = {
  minWidth: 0,
  verticalAlign: 'top'
};

const SubmitFlatButton = ({ name, buttonText, fontIconClass }) => (
  <FlatButton
    name={name}
    type='submit'
    hoverColor='transparent'
    style={flatButtonStyle}
    labelPosition='before'
    label={buttonText}
    labelStyle={labelStyle}
    aria-label={buttonText}
    title={buttonText}
    icon={<FontIcon className={fontIconClass} color={grey500} style={iconStyle} />}
  />
);

SubmitFlatButton.propTypes = {
  name: React.PropTypes.string.isRequired,
  buttonText: React.PropTypes.string.isRequired,
  fontIconClass: React.PropTypes.string.isRequired
};

export default SubmitFlatButton;
