import React from 'react'

import 'scss/account_recovery/page.scss'

const Page = () => (
  <div className='container'>
    <form>
      <img src='assets/images/forgot-my-password.svg' />
      <h1>E se você esquecer sua senha?</h1>
      <p>Informe outro e-mail que você usa regularmente. Esse será o seu e-mail de recuperação.</p>
      <p>Instruções serão enviadas para esse e-mail, guarde com carinho.</p>
      <div className="field-group">
        <input type="text" name="email" className="email" required/>
        <label className="animated-label" htmlFor="email">Digite seu e-mail de recuperação</label>
      </div>
      <button>Adicionar e-mail</button>
    </form>
  </div>
);

export default Page
