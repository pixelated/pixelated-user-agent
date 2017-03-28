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
import Snackbar from 'material-ui/Snackbar';
import { red500, blue500 } from 'material-ui/styles/colors';

const notificationStyle = () => ({
  top: 0,
  bottom: 'auto',
  left: (window.innerWidth - 288) / 2,
  transform: 'translate3d(0, 0px, 0)'
});

const contentStyle = {
  textAlign: 'center'
};

const getStyleByType = (isError) => {
  if (isError) {
    return { backgroundColor: red500 };
  }
  return { backgroundColor: blue500 };
};

const SnackbarNotification = ({ message, isError = false, autoHideDuration = 5000 }) => (
  <Snackbar
    open
    bodyStyle={getStyleByType(isError)}
    message={message}
    autoHideDuration={autoHideDuration}
    contentStyle={contentStyle}
    style={notificationStyle()}
  />
);

SnackbarNotification.propTypes = {
  message: React.PropTypes.string.isRequired,
  isError: React.PropTypes.bool,
  autoHideDuration: React.PropTypes.number
};

SnackbarNotification.defaultProps = {
  isError: false,
  autoHideDuration: 5000
};

export default SnackbarNotification;
