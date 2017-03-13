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
import { I18nextProvider } from 'react-i18next';

import internationalization from 'src/common/i18n';
import injectTapEventPlugin from 'react-tap-event-plugin';
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';
import materialPixTheme from 'src/common/materialPixTheme';

injectTapEventPlugin();

const App = ({ i18n = internationalization, child }) => (
  <MuiThemeProvider muiTheme={materialPixTheme}>
    <I18nextProvider i18n={i18n}>
      {child}
    </I18nextProvider>
  </MuiThemeProvider>
);

App.propTypes = {
  i18n: React.PropTypes.object, // eslint-disable-line react/forbid-prop-types
  child: React.PropTypes.element.isRequired
};

App.defaultProps = {
  i18n: internationalization
};

export default App;
