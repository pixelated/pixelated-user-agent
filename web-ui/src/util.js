export const hasQueryParameter = (param) => {
  const decodedUri = decodeURIComponent(window.location.search.substring(1)).split('&');
  return decodedUri.includes(param);
};

export default {
  hasQueryParameter
};
