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
import { translate } from 'react-i18next';

const App = () => (
  <form className='standard' id='login_form' action='/login' method='post'>
    <input
      type='text' name='username' id='email' className='text-field'
      placeholder='username' autoFocus=''
    />
    <input
      type='password' name='password' id='password' className='text-field'
      placeholder='password' autoComplete='off'
    />
    <input type='submit' name='login' value='Login' className='button' />
  </form>
);

export default translate('', { wait: true })(App);
