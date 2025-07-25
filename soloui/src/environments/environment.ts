export const environment = {
  production: false,
  apiUrl:
    window.location.port === '4200'
      ? 'http://localhost:8000/api'
      : 'http://localhost:8060/api'
};
