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
import getMuiTheme from 'material-ui/styles/getMuiTheme';

const mediumLightGrey = '#999999';
const darkBlue = '#178ca6';

const materialPixTheme = getMuiTheme({
  fontFamily: 'Open Sans, sans-serif',
  palette: {
    disabledColor: mediumLightGrey,
    primary1Color: darkBlue,
    borderColor: darkBlue
  }
});

export default materialPixTheme;
