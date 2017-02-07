import React from 'react'
import { render } from 'react-dom'
import Page from 'js/account_recovery/page'
import a11y from 'react-a11y'

import 'font-awesome/scss/font-awesome.scss'

if(process.env.NODE_ENV === 'development') a11y(React);

render(
  <Page/>,
  document.getElementById('root')
);