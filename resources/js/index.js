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

/* eslint-disable prettier/prettier */
function CallWeatherAPI() {
  const city = $('#select2-id_title-container').text();
  const cityForecast = $('#city-rendered-box');
  const days = $('#id_days').val();
  const err = $('#city-load-error');

  if (city) {
    $.ajax({
      type: "GET",
      url: `http://127.0.0.1:8000/api/locations/${city}/?days=${days}`,
      beforeSend: () => {
        cityForecast.html('<div class="ui one column stackable grid">' +
          '  <div class="column">' +
          '    <div class="ui raised segment">' +
          '      <div class="ui placeholder">' +
          '        <div class="image header">' +
          '          <div class="line"></div>' +
          '          <div class="line"></div>' +
          '        </div>' +
          '        <div class="paragraph">' +
          '          <div class="medium line"></div>' +
          '          <div class="short line"></div>' +
          '        </div>' +
          '      </div>' +
          '    </div>' +
          '  </div>' +
          '</div>');
      },
      success: (data) => {
        err.hide();
        cityForecast.html('<div />');
        let html = '';
        /* eslint-disable array-callback-return */
        data.map((forecast, index) => {
          html = `${html  }<tr>` +
            `      <td>${  index + 1  }</td>` +
            `      <td>${  forecast.maximum  }</td>` +
            `      <td>${  forecast.minimum  }</td>` +
            `      <td>${  forecast.average  }</td>` +
            `      <td>${  forecast.median  }</td>` +
            `    </tr>`
        });
        /* enable array-callback-return */
        cityForecast.html(`${'<div class="html ui top attached segment">' +
          '<table class="ui definition table">' +
          '  <thead>' +
          '    <tr>' +
          '      <th></th>' +
          '      <th>Maximum</th>' +
          '      <th>Minimum</th>' +
          '      <th>Average</th>' +
          '      <th>Median</th>' +
          '    </tr>' +
          '  </thead>' +
          '  <tbody>'}${
          html
        }  </tbody>` +
          `</table>` +
          `</div>`
        );
      },
      error: (e) => {
        cityForecast.html('<div />');
        err.text(e.responseText);
        err.show();
      },
    })
  }
}
/* enable prettier/prettier */

$(document).ready(() => {
  $(document).on('change', '#id_title,#id_days', () => {
    CallWeatherAPI();
  });
});
