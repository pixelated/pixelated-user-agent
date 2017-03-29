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

import './back_link.scss';

const icon = <i className='fa fa-angle-left' aria-hidden='true' />;

const button = (text, options) => (
  <button className='link' {...options}>{icon}<span>{text}</span></button>
);

const link = (text, options) => (
  <a className='link' {...options}>{icon}<span>{text}</span></a>
);

const BackLink = ({ text, ...other }) => (
  <div className='link-content'>
    { other.href ? link(text, other) : button(text, other) }
  </div>
);

BackLink.propTypes = {
  text: React.PropTypes.string.isRequired
};

export default BackLink;
