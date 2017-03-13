export const hasQueryParameter = (param) => {
  const decodedUri = decodeURIComponent(window.location.search.substring(1));
  return !(decodedUri.split('&').indexOf(param) < 0);
};

export default {
  hasQueryParameter
};
