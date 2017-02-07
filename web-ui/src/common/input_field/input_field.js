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

import React from 'react'

import './input-field.scss'

const InputField = ({ label, name }) => (
  <div className='input-field-group'>
    <input type='text' name={name} className='input-field' required />
    <label className='input-field-label' htmlFor={name}>{label}</label>
  </div>
)

InputField.propTypes = {
  label: React.PropTypes.string.isRequired,
  name: React.PropTypes.string.isRequired
}

export default InputField
