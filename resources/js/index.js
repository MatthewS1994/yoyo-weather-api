import '../scss/app.scss';

/* eslint-disable import/no-duplicates */
import 'jquery/dist/jquery';
/* eslint-enable import/no-duplicates */
import './vendor/init';
import '@popperjs/core';
import 'bootstrap/dist/js/bootstrap';
import 'bootstrap/js/dist/tooltip';
import 'jquery.cookie/jquery.cookie';
import '@lgaitan/pace-progress';
import 'semantic-ui-css/semantic.min';

// Load the favicon and the .htaccess file
/* eslint-disable import/no-unresolved, import/extensions */
import 'file-loader?name=.htaccess!../.htaccess';
/* eslint-enable import/no-unresolved, import/extensions */

/* eslint-disable import/no-duplicates */
/* eslint-disable no-unused-vars */
import $ from 'jquery';

if (process.env.NODE_ENV === 'production') {
  require('offline-plugin/runtime').install(); // eslint-disable-line global-require
}
