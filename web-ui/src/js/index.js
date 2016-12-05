import React from 'react';
import ReactDOM from 'react-dom';
import {createStore} from 'redux';
import {Map} from 'immutable';
import 'whatwg-fetch';


class PixelatedComponent extends React.Component {
  _updateStateFromStore() {
    this.setState(this.props.store.getState().toJS());
  }

  componentWillMount() {
    this.unsubscribe = this.props.store.subscribe(() => this._updateStateFromStore());
    this._updateStateFromStore();
  }

  componentWillUnmount() {
    this.unsubscribe();
  }
}


class PixelatedForm extends PixelatedComponent {
  _fetchAndDispatch(url, actionProperties) {
    const immutableActionProperties = new Map(actionProperties);
    this.props.store.dispatch(immutableActionProperties.merge({status: 'STARTED'}).toJS());
    fetch(url).then((response) => {
      return response.json();
    }).then((json) => {
      setTimeout(() => {
        this.props.store.dispatch(immutableActionProperties.merge({status: 'SUCCESS', json: json}).toJS());
      }, 3000);
    }).catch((error) => {
      console.error('something went wrong', error);
      this.props.store.dispatch(immutableActionProperties.merge({status: 'ERROR', error: error}).toJS());
    });
  }
}


class InviteCodeForm extends PixelatedForm {
  render() {
    let className = "blue-button validation-link";

    if(!this.state.inviteCodeValidation) {
      className = className + " disabled";
    }

    return (
      <form onSubmit={this._handleClick.bind(this)}>
        <div className="field-group">
          <input type="text" name="invite-code" className="invite-code" onChange={this._handleInputEmpty.bind(this)} required/>
          <label className="animated-label" htmlFor="invite-code">invite code</label>
        </div>
        <input type="submit" value="Get Started" className={className} />
      </form>
    );
  }

  _handleClick(event) {
    event.stopPropagation();
    event.preventDefault();
    this.props.store.dispatch({type: 'SUBMIT_INVITE_CODE', inviteCode: event.target['invite-code'].value});
  }

  _handleInputEmpty(event) {
    this.props.store.dispatch({type: 'VALIDATE_INVITE_CODE', inviteCode: event.target.value});
  }
}


class CreateAccountForm extends PixelatedForm {
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
    this.props.store.dispatch({type: 'SUBMIT_CREATE_ACCOUNT', username: event.target.username.value, password: event.target.password.value});
  }
}


class BackupEmailForm extends PixelatedForm {
  render() {
    return (
      <form onSubmit={this._handleClick.bind(this)}>
        <div className="field-group">
          <input type="text" name="backup-email" required/>
          <label className="animated-label" htmlFor="password">type your backup email</label>
        </div>

        <input type="submit" value="Send Email" className="blue-button validation-link" />
        <p className="link-message">
          <a href="#" className="validation-link">I didn't receive anything. Send the email again</a>
        </p>
      </form>
    );
  }

  _handleClick(event) {
    event.stopPropagation();
    event.preventDefault();
    this._fetchAndDispatch('dummy.json', {type: 'SUBMIT_BACKUP_EMAIL', backupEmail: event.target['backup-email'].value});
  }
}


class BackupEmailSentForm extends PixelatedForm {
  render() {
    return (
      <form onSubmit={this._handleClick.bind(this)}>
        {this.state.isFetching || <a href="/" className="blue-button">I received the codes. <br/>Go to my inbox</a>}
        <p className="link-message">
          <a href="#">I didn't receive anything. Send the email again</a>
        </p>
      </form>
    );
  }

  _handleClick(event) {
    event.stopPropagation();
    event.preventDefault();
  }
}


class SignUp extends PixelatedComponent {
  render() {
    return (
      <div>
        <div className="message">
          <h1>{this.state.header}</h1>
          {this.state.icon}
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
      case 'backup_email_sent': return <BackupEmailSentForm store={store} />;
      default: throw Error('TODO');
    }
  }
}


const initialState = new Map({
  isFetching: false,
  form: 'invite_code',
  header: 'Welcome',
  icon: null,
  summary: ['Do you have an invite code?', <br key='br1' />, 'Type it below'],
});


const store = createStore((state=initialState, action) => {
  switch (action.type) {
  case 'SUBMIT_INVITE_CODE':
    return state.merge({
      inviteCode: action.inviteCode,
      form: 'create_account',
      header: 'Create your account',
      summary: 'Choose your username, and be careful about your password, it must be strong and easy to remember. If you have a password manager, we strongly advise you to use one.',
    });
  case 'SUBMIT_CREATE_ACCOUNT':
    return state.merge({
      username: action.username,
      password: action.password,
      form: 'backup_email',
      header: 'In case you lose your password...',
      summary: 'Set up a backup email account. You\'ll receive an email with a code so you can recover your account in the future, other will be sent to your account administrator.',
    });
  case 'SUBMIT_BACKUP_EMAIL':
    switch (action.status) {
    case 'STARTED':
      return state.merge({
        isFetching: true,
        backupEmail: action.backupEmail,
        form: 'backup_email_sent',
        icon: <p><img key="img1" src="images/sent_email.png" className="sent-email-icon"/></p>,
        summary: 'An email was sent to the email you provided. Check your spam folder, just in case.',
      });
    case 'SUCCESS':
      return state.merge({
        isFetching: false,
      });
    case 'ERROR':
      return state.merge({
        isFetching: false,
      });
    default:
      return state;
    }
  case 'SUBMIT_BACKUP_EMAIL_SENT':
    return state.merge({});
  case 'VALIDATE_INVITE_CODE':
    return state.merge({
      inviteCodeValidation: Boolean(action.inviteCode)
    });
  default:
    return state;
  }
});


ReactDOM.render(
  <SignUp store={store}/>,
  document.getElementById('app')
);
