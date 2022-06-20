document.addEventListener('DOMContentLoaded', function() {

  // // get reports via ajax_obj.reports_by_user_url
  var get_reports_by_user = function(event) {
    var element = event.target;
    var granddad_element = element.parentNode.parentNode;
    var granddad_id = granddad_element.getAttribute('id');
    var input_name = granddad_id.replace('-column', '');

    console.log(input_name + ' : via Ajax, get reports for ' + element.options[element.selectedIndex].value);

    var xmlhttp = false;
    if (window.XMLHttpRequest) {
        xmlhttp = new XMLHttpRequest();
    }
    else if (window.ActiveXObject) {
        xmlhttp = new ActiveXObject('Microsoft.XMLHTTP');
    }

    xmlhttp.onreadystatechange=function() {
      if (xmlhttp.readyState==4 && xmlhttp.status==200) {
         // document.getElementById("relatedPosts").innerHTML=xmlhttp.responseText;
         var responseJSON = JSON.parse(xmlhttp.responseText);

         console.log('submit : xmlhttp.responseText = ' + xmlhttp.responseText);

         var resultElement = granddad_element.querySelector(".reports");

         // // Remove existing children
         while (resultElement.firstChild) {
           resultElement.removeChild(resultElement.firstChild);
         }

         if (responseJSON.error) {

           console.log('submit : KO. error = ' + responseJSON.error);

           // // Fade in (?) the form submission alert
           resultElement.innerHTML = responseJSON.error;

         } else {

            const user = responseJSON.user;

            // // Add HTML elements based on Ajax response

            // var nameElement = document.createElement('h6');
            // nameElement.innerHTML = user.first_name + ' ' + user.last_name;

            var reportCountElement = document.createElement('span');
            reportCountElement.innerHTML = user.report_count + ' found';

            var dividerElement = document.createElement('div');
            dividerElement.classList.add('divider');

            // resultElement.appendChild(nameElement);
            resultElement.appendChild(reportCountElement);
            resultElement.appendChild(dividerElement);

            var shortMonthNames = ['Jan', 'Feb', 'Mar',
              'Apr', 'May', 'Jun',
              'Jul', 'Aug', 'Sep',
              'Oct', 'Nov', 'Dec'];

            var reports = user.reports;
            for (var i = 0; i < user.report_count; i++) {
              var report = reports[i];

              /*
              <h6>{{ uzzer.first_name }}</h6>

              {{ uzzer.report_count }} found
              <div class="divider" ></div>
              {% for report in uzzer.reports %}
                <label>
                  <input type="radio" name="self" value="{{ report.stage }}|{{ report.target }}|{{ report.id }}" />
                  <span class="slanted">{{ report.stage }}</span>&nbsp:&nbsp;<span class="blue-text">{{ report.dream_name }}</span>
                  <div class="ml-3 black-text">{{ report.dream_date|date:"DATETIME_FORMAT" }}</div>
                </label>
              {% endfor %}
              */

              var labelElement = document.createElement('label');

              var inputElement = document.createElement('input');
              inputElement.setAttribute('type', 'radio');
              inputElement.setAttribute('name', input_name);
              inputElement.setAttribute('value', report.stage + '|' + report.target + '|' + report.id);

              var spanTargetElement = document.createElement('span');
              spanTargetElement.classList.add('slanted');
              spanTargetElement.innerHTML = report.stage;

              var spanSpaceElement = document.createElement('span');
              spanSpaceElement.innerHTML = '&nbsp:&nbsp;';

              var spanReportNameElement = document.createElement('span');
              spanReportNameElement.classList.add('blue-text');
              spanReportNameElement.innerHTML = report.dream_name;

              var dateArray1 = (report.dream_date).split('T');
              var dateArray2 = (dateArray1[0]).split('-');
              var dateArray3 = (dateArray1[1]).split(':');

              var dateElement = document.createElement('div');
              dateElement.classList.add('ml-3', 'black-text');
              dateElement.innerHTML = shortMonthNames[dateArray2[1] - 1]
                + '. ' + dateArray2[2]
                + ', ' + dateArray2[0]
                // + ', ' + dateArray3[0]
                + ', ' + (dateArray3[0] > 12 ? dateArray3[0] - 12 : dateArray3[0])
                + ':' + dateArray3[1]
                + ' ' + (dateArray3[0] > 12 ? 'a.m.' : 'p.m.');

              labelElement.appendChild(inputElement);
              labelElement.appendChild(spanTargetElement);
              labelElement.appendChild(spanSpaceElement);
              labelElement.appendChild(spanReportNameElement);
              labelElement.appendChild(dateElement);

              resultElement.appendChild(labelElement);
            } // // end : for (var i = 0; i < user.report_count; i++)
          } // // end : if (responseJSON.error)
        } // // end : if (xmlhttp.readyState==4 && xmlhttp.status==200)
    } // end : xmlhttp.onreadystatechange=function()

    var base_url = ajax_obj.reports_by_user_url;
    var actual_url = base_url.replace('/0', '/' + element.options[element.selectedIndex].value);

    xmlhttp.open("GET", actual_url, true);
    xmlhttp.send();
  };

  // // ============================

  var person1_member = document.querySelector('select[name="person1_member"]');

  // // Init Materialize CSS for group select
  M.FormSelect.init(person1_member, {});

  // // Bind listener to the group select
  person1_member.addEventListener("change", get_reports_by_user);

  // // ============================

  var person2_member = document.querySelector('select[name="person2_member"]');

  // // Init Materialize CSS for group select
  M.FormSelect.init(person2_member, {});

  // // Bind listener to the group select
  person2_member.addEventListener("change", get_reports_by_user);

  // // ============================
  // // ============================
  // // ============================
  // // ============================
  // // ============================

  // // What to do when the "type" buttons are clicked
  var left_column = document.getElementById('left-column');
  var right_column = document.getElementById('right-column');
  var self_column = document.getElementById('self-column');
  var person1_column = document.getElementById('person1-column');
  var person2_column = document.getElementById('person2-column');
  var button_ids = ['self-self', 'self-person', 'person-self', 'person-person'];

  var toggleTypeButtons = function(eyed) {

      console.log('eyed = ' + eyed);

      // // Toggle active appearance on buttons
      button_ids.forEach(function (item, index) {
        var button = document.getElementById(item);

        if (item != eyed) {
          button.classList.remove('btn-active');
          button.classList.remove('blue');
          button.classList.add('black');
        } else {
          button.classList.add('btn-active');
          button.classList.add('blue');
          button.classList.remove('black');
        }
      });
  };

  document.getElementById('self-self').addEventListener(
    "click",
    // "submit",
    function(event) {
      event.preventDefault();

      // // If it is already active, abort
      if (event.target.classList.contains('btn-active')) {
        return false;
      }

      var current_id = event.target.getAttribute('id');
      toggleTypeButtons(current_id);

      // // move #self-column to #left-column
      var sc = right_column.querySelector('#self-column');
      if (sc) {
        left_column.appendChild(self_column);
      }

      self_column.classList.remove("hide");
      person1_column.classList.add("hide");

      person2_column.classList.add("hide");

      // // Manipulate some form values ...
      document.querySelector('input[name="type"]').value = 'self|self';

      return false;
    });

  document.getElementById('self-person').addEventListener(
    "click",
    // "submit",
    function(event) {
      event.preventDefault();

      // // If it is already active, abort
      if (event.target.classList.contains('btn-active')) {
        return false;
      }

      var current_id = event.target.getAttribute('id');
      toggleTypeButtons(current_id);

      var sc = right_column.querySelector('#self-column');
      if (sc) {
        left_column.appendChild(self_column);
      }

      self_column.classList.remove("hide");
      person1_column.classList.add("hide");

      person2_column.classList.remove("hide");

      // // Manipulate some form values ...
      document.querySelector('input[name="type"]').value = 'self|person';

      return false;
    });

  document.getElementById('person-self').addEventListener(
    "click",
    // "submit",
    function(event) {
      event.preventDefault();

      // // If it is already active, abort
      if (event.target.classList.contains('btn-active')) {
        return false;
      }

      var current_id = event.target.getAttribute('id');
      toggleTypeButtons(current_id);

      // // move #self-column to #right-column
      right_column.appendChild(self_column);

      person1_column.classList.remove("hide");

      self_column.classList.remove("hide");
      person2_column.classList.add("hide");

      // // Manipulate some form values ...
      document.querySelector('input[name="type"]').value = 'person|self';

      return false;
    });

    document.getElementById('person-person').addEventListener(
      "click",
      // "submit",
      function(event) {
        event.preventDefault();

        // // If it is already active, abort
        if (event.target.classList.contains('btn-active')) {
          return false;
        }

        var current_id = event.target.getAttribute('id');
        toggleTypeButtons(current_id);

        self_column.classList.add("hide");
        person1_column.classList.remove("hide");

        person2_column.classList.remove("hide");

        // // Manipulate some form values ...
        document.querySelector('input[name="type"]').value = 'person|person';

        return false;
      });


});
