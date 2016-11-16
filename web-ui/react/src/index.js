import React from 'react';
import ReactDOM from 'react-dom';
import {createStore} from 'redux';
import {Map} from 'immutable';


class PixelatedComponent extends React.Component {
  _updateStateFromStore() {
    this.setState(this.props.store.getState().toJS());
  }

  componentWillMount() {
    console.debug('mounting', this);
    this.unsubscribe = this.props.store.subscribe(() => this._updateStateFromStore());
    this._updateStateFromStore();
  }

  componentWillUnmount() {
    console.debug('unmounting', this);
    this.unsubscribe()
  }
}


class InviteCodeForm extends PixelatedComponent {
  render() {
    return (
      <form onSubmit={this._handleClick.bind(this)}>
        <div className="field-group">
          <input type="text" name="invite-code" className="invite-code" required/>
          <label className="animated-label" htmlFor="invite-code">invite code</label>
        </div>
        <input type="submit" value="Get Started" className="blue-button validation-link" />
      </form>
    );
  }

  _handleClick(event) {
    event.stopPropagation();
    event.preventDefault();
    this.props.store.dispatch({type: 'SUBMIT_INVITE_CODE'});
  }
}


class CreateAccountForm extends PixelatedComponent {
  render() {
    return (
      <form onSubmit={this._handleClick.bind(this)}>
        <span className="domain-label"> @domain.com </span>
        <div className="field-group">
          <input type="text" name="username" className="username" required/>
          <label className="animated-label" htmlFor="username">username</label>
        </div>

        <div className="field-group">
          <input type="password" name="password" className="password" required/>
          <label className="animated-label" htmlFor="password">password</label>
        </div>

        <div className="field-group">
          <input type="text" name="name" className="name" required/>
          <label className="animated-label" htmlFor="name">name</label>
        </div>

        <input type="submit" value="Create my account" className="blue-button validation-link" />
      </form>
    );
  }

  _handleClick(event) {
    event.stopPropagation();
    event.preventDefault();
    this.props.store.dispatch({type: 'SUBMIT_CREATE_ACCOUNT'});
  }
}


class BackupEmailForm extends PixelatedComponent {
  render() {
    return (
      <form onSubmit={this._handleClick.bind(this)}>
        <span className="domain-label"> @domain.com </span>
        <div className="field-group">
          <input type="text" name="username" className="username" required/>
          <label className="animated-label" htmlFor="username">username</label>
        </div>

        <div className="field-group">
          <input type="password" name="password" className="password" required/>
          <label className="animated-label" htmlFor="password">password</label>
        </div>

        <input type="submit" value="Create my account" className="blue-button validation-link" />
      </form>
    );
  }

  _handleClick(event) {
    event.stopPropagation();
    event.preventDefault();
    this.props.store.dispatch({type: 'SUBMIT_CREATE_ACCOUNT'});
  }
}


class SignUp extends PixelatedComponent {
  render() {
    return (
      <div>
        <div className="message">
          <h1>{this.state.header}</h1>
          <p>{this.state.summary}</p>
        </div>
        <div className="form-container">
          {this._form()}
        </div>
      </div>
    );
  }

  _form() {
    switch(this.state.form) {
      case 'invite_code': return <InviteCodeForm store={store} />;
      case 'create_account': return <CreateAccountForm store={store} />;
      case 'backup_email': return <BackupEmailForm store={store} />;
      default: throw Exception('TODO');
    }
  }
}


const initialState = new Map({
  form: 'invite_code',
  header: 'Welcome',
  summary: ['Do you have an invite code?', <br/>, 'Type it below'],
});


const store = createStore((state=initialState, action) => {
  switch (action.type) {
  case 'SUBMIT_INVITE_CODE':
    return state.merge({
      form: 'create_account',
      header: 'Create your account',
      summary: 'Choose your username, and be careful about your password, it must be strong and easy to remember. If you have a password manager, we strongly advise you to use one.',
    });
  case 'SUBMIT_CREATE_ACCOUNT':
    return state.merge({
      form: 'backup_email',
      header: 'In case you lose your password...',
      summary: 'Set up a backup email account. You\'ll receive an email with a code so you can recover your account in the future, other will be sent to your account administrator.',
    });
  default:
    return state;
  }
});


ReactDOM.render(
  <SignUp store={store}/>,
  document.getElementById('app')
);
