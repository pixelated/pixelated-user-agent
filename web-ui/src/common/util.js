import browser from 'helpers/browser';

export const hasQueryParameter = (param) => {
  const decodedUri = decodeURIComponent(window.location.search.substring(1));
  return !(decodedUri.split('&').indexOf(param) < 0);
};

export const submitForm = (event, url, body = {}) => {
  event.preventDefault();

  return fetch(url, {
    credentials: 'same-origin',
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      csrftoken: [browser.getCookie('XSRF-TOKEN')],
      ...body
    })
  });
};

export default {
  hasQueryParameter,
  submitForm
};
