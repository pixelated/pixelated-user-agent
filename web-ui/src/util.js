export const hasQueryParameter = param => (
  decodeURIComponent(window.location.search.substring(1)).includes(param)
);

export default {
  hasQueryParameter
};
