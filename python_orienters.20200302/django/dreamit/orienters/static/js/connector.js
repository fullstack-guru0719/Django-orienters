document.addEventListener('DOMContentLoaded', function() {

  var userCheckboxListener = function(event) {
    var id = this.value;
    var select_name = 'user-' + id;
    var selectElement = document.querySelector('select[name="' + select_name + '"]');

    if (selectElement) {
      var parentNode = selectElement.parentNode;
      var inputNode = parentNode.querySelector('input');
      if (inputNode) {
        if (this.checked) {

          console.log('checked. enabling select');

          selectElement.removeAttribute('disabled');
          // inputNode.removeAttribute('disabled');

          // // materialize must destroy then init to 're-enable'. Kinda stupid ...
          var instance = M.FormSelect.getInstance(selectElement);
          instance.destroy();
          M.FormSelect.init(selectElement, {});

        } else {

          console.log('not checked. disabling select');

          selectElement.setAttribute('disabled', 'disabled');
          inputNode.setAttribute('disabled', 'disabled');
        }
      }
    }

    // // Display the submit buttons if at least one checkbox gets checked
    var users = document.querySelectorAll('input[name="users[]"]:checked');

    console.log('number of checked users = ' + users.length);

    var submit_buttons = document.getElementById('submit-buttons');
    if (users.length > 0) {
      if (submit_buttons.classList.contains('hide')) {
        submit_buttons.classList.remove('hide');
      }
    } else {
      if (!submit_buttons.classList.contains('hide')) {
        submit_buttons.classList.add('hide');
      }
    }

  };





  var group_select = document.querySelector('select[name="group_id"]');

  // // Init Materialize CSS for group select
  M.FormSelect.init(group_select, {});

  // // Bind listener to the group select
  group_select.addEventListener("change", function(event) {
    var element = event.target;

    console.log('via Ajax, get users & reports for group id ' + element.options[element.selectedIndex].value);

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

         var resultMetaElement = document.getElementById('group-result-meta');
         var resultElement = document.getElementById('group-result');

         if (responseJSON.error) {

           console.log('submit : KO. error = ' + responseJSON.error);

           // // Fade in (?) the form submission alert
           resultMetaElement.innerHTML = responseJSON.error;

         } else {

            const users = responseJSON.users;

            console.log('submit : OK. users.length = ' + users.length);

            resultMetaElement.innerHTML = users.length + ' users found';

            // // Add HTML elements based on Ajax response
            for (var i = 0; i < users.length; i++) {
              var user = users[i];
              var rowElement = document.createElement('div');
              rowElement.classList.add('row');





              var optionElements = [];

              const identifier_reports = user.identifier_reports;
              for (var j = 0; j < identifier_reports.length; j++) {
                var identifier_report = identifier_reports[j];

                /*
                var rrowElement = document.createElement('div');
                rrowElement.classList.add('row');
                rrowElement.innerHTML = '[' + identifier_report.target + '|' +  identifier_report.stage + '|' + identifier_report.id + '] ' + identifier_report.dream_name;

                rowElement.appendChild(rrowElement);
                */

                var optionElement = document.createElement('option');
                optionElement.setAttribute('value', identifier_report.target + '|' +  identifier_report.stage + '|' + identifier_report.id);
                optionElement.innerHTML = identifier_report.dream_name;

                optionElements.push(optionElement);
              }

              const illuminator_reports = user.illuminator_reports;
              for (var j = 0; j < illuminator_reports.length; j++) {
                var illuminator_report = illuminator_reports[j];

                /*
                var rrowElement = document.createElement('div');
                rrowElement.classList.add('row');
                rrowElement.innerHTML = '[' + illuminator_report.target + '|' +  illuminator_report.stage + '|' + illuminator_report.id + '] ' + illuminator_report.dream_name;

                rowElement.appendChild(rrowElement);
                */

                var optionElement = document.createElement('option');
                optionElement.setAttribute('value', illuminator_report.target + '|' +  illuminator_report.stage + '|' + illuminator_report.id);
                optionElement.innerHTML = illuminator_report.dream_name;

                optionElements.push(optionElement);
              }





              if (optionElements.length > 0) {
                /*
                <label>
                  <input type="checkbox" name="unordered_words[]" value="{{ word.pk }}" />
                  <span>{{ word.word }}</span>
                </label>
                */

                var labelElement = document.createElement('label');

                var checkboxElement = document.createElement('input');
                checkboxElement.setAttribute('type', 'checkbox');
                checkboxElement.setAttribute('name', 'users[]');
                checkboxElement.setAttribute('value', user.id);
                checkboxElement.addEventListener("change", userCheckboxListener);

                var spanElement = document.createElement('span');
                spanElement.innerHTML = user.first_name + ' ' + user.last_name;

                labelElement.appendChild(checkboxElement);
                labelElement.appendChild(spanElement);

                // <div class="input-field col s12">
                var columnOneElement = document.createElement('div');
                columnOneElement.classList.add('input-field', 'col', 's4');
                columnOneElement.appendChild(labelElement);


                var selectElement = document.createElement('select');
                selectElement.setAttribute('name', 'user-' + user.id);
                selectElement.setAttribute('disabled', 'disabled');
                selectElement.classList.add('user-report');

                for (var k = 0; k < optionElements.length; k++) {
                  selectElement.appendChild(optionElements[k]);
                }




                var columnTwoElement = document.createElement('div');
                columnTwoElement.classList.add('input-field', 'col', 's8');
                columnTwoElement.appendChild(selectElement);

                rowElement.appendChild(columnOneElement);
                rowElement.appendChild(columnTwoElement);

                resultElement.appendChild(rowElement);

                // // Make sure the select has been added to the DOM
                M.FormSelect.init(selectElement, {});
              } else {
                var labelElement = document.createElement('label');

                // // create a disabled checkbox
                var checkboxElement = document.createElement('input');
                checkboxElement.setAttribute('name', 'users-no-report[]');
                checkboxElement.setAttribute('type', 'checkbox');
                checkboxElement.setAttribute('disabled', 'disabled');

                var spanElement = document.createElement('span');
                spanElement.innerHTML = user.first_name + ' ' + user.last_name;

                labelElement.appendChild(checkboxElement);
                labelElement.appendChild(spanElement);




                // <div class="input-field col s12">
                var columnOneElement = document.createElement('div');
                columnOneElement.classList.add('input-field', 'col', 's4');
                columnOneElement.appendChild(labelElement);

                var spanElement = document.createElement('span');
                spanElement.innerHTML = '(No report available)';

                var columnTwoElement = document.createElement('div');
                columnTwoElement.classList.add('input-field', 'col', 's8', 'pt-1');
                columnTwoElement.appendChild(spanElement);

                rowElement.appendChild(columnOneElement);
                rowElement.appendChild(columnTwoElement);

                resultElement.appendChild(rowElement);
              } // // end : if (optionElements.length > 0)
            } // // end : for (var i = 0; i < users.length; i++)

          } // // end : if (responseJSON.error)
        } // // end : if (xmlhttp.readyState==4 && xmlhttp.status==200)
    } // end : xmlhttp.onreadystatechange=function()

    var base_url = ajax_obj.reports_by_group_url;
    var actual_url = base_url.replace('/0', '/' + element.options[element.selectedIndex].value);

    xmlhttp.open("GET", actual_url, true);
    xmlhttp.send();
  });




  /*
  var constructSubmitData = function(event) {
      // // Get the selected report(s)
      // // See ~/Documents/python_orienters/docs/connector-drop-down-trail.png

      var selected_reports = [];

      // // Get the checked users
      var userCheckboxes = document.querySelectorAll('input[name="users[]"]');
      userCheckboxes.forEach(function(userCheckbox){

        if (userCheckbox.checked) {
          var id = userCheckbox.value;

          console.log(id + ' is checked');

          var select_name = 'user-' + id;
          var selectElement = document.querySelector('select[name="' + select_name + '"]');

          if (selectElement) {
            // // Get the selected option from the fancy materialize elements
            var parentNode = selectElement.parentNode;
            var selectedSpan = parentNode.querySelector('ul li.selected span');
            if (selectedSpan) {
              var spanText = selectedSpan.innerHTML;

              // // Get the option with said text
              for (const opt of selectElement.querySelectorAll('option')) {
                if (opt.textContent.includes(spanText)) {
                  selected_reports.push(opt.value);
                }
              }
            }

          }
        } else {
          console.log(userCheckbox.value + ' is *NOT* checked');
        }

      });

      console.table(selected_reports);

      return selected_reports;
  };
  */

  // // START : Set hidden form inputs when the relevant submit button gets clicked
  document.getElementById('connector-group-submit').addEventListener(
    "click",
    // "submit",
    function(event) {
      event.preventDefault();

      // // Manipulate some form values ...
      document.querySelector('input[name="connector_type"]').value = 'group';

      // var selected_reports = constructSubmitData(event);
      // document.querySelector('input[name="selected_reports[]"]').value = selected_reports;

      // // ... then submit form
      document.getElementById('connector-form').submit();

      return false;
    });

  document.getElementById('connector-cadence-submit').addEventListener(
    "click",
    // "submit",
    function(event) {
      event.preventDefault();

      // // Manipulate some form values ...
      document.querySelector('input[name="connector_type"]').value = 'cadence';

      // var selected_reports = constructSubmitData(event);
      // document.querySelector('input[name="selected_reports[]"]').value = selected_reports;

      // // ... then submit form
      // document.getElementById('connector-form').submit();
      // // Actually, no.
      // // The user has to click on 'Assert', 'Produce', 'Think' etc before
      // // we save to server. See the code near the bottom.

      // // Get cadence_max from the server.
      // // Then based on that, display the cadence buttons.
      // // Search for 'showEnergies' in www/wp-content/plugins/dreamit-core/js/common.js

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

           console.log('cadence click : xmlhttp.responseText = ' + xmlhttp.responseText);

           if (responseJSON.error) {

             console.log('cadence click : KO. error = ' + responseJSON.error);

           } else {

              const cadence_max = responseJSON.cadence_max;

              console.log('cadence click : OK. cadence_max = ' + cadence_max);

              document.querySelector('input[name="cadence_max"]').value = cadence_max;

              // // Show relevant cadence buttons
              var cadence_links = document.querySelectorAll('.cadence a');
              // // Hide all cadence links
              for (let i = 0; i < cadence_links.length; i++) {
                if (!cadence_links[i].classList.contains('hide')) {
                  cadence_links[i].classList.add('hide');
                }
              }
              // // Show relevant cadence links
              for (let i = 0; i < cadence_max; i++) {
                cadence_links[i].classList.remove('hide');
              }

          }
        }
      };

      /*
      // // Manually field by field

      var formData = new FormData();
      formData.append("action", action);
      formData.append("nonce_field", nonce_value);
      formData.append("email", email);
      formData.append("name", name);
      formData.append("body", body);
      */

      // // Let the browser deal with it :)
      var formData = new FormData(document.getElementById('connector-form'));

      xmlhttp.open("POST", ajax_obj.calculate_cadence_max_url,true);
      // xmlhttp.setRequestHeader("Content-type", "multipart/form-data; charset=utf-8; boundary=" + Math.random().toString().substr(2));
      xmlhttp.send(formData);

      return false;
    });
  // // END : Set hidden form inputs when the relevant submit button gets clicked






  var cadence_links = document.querySelectorAll('.cadence a');
  for (let i = 0; i < cadence_links.length; i++) {
    cadence_links[i].addEventListener("click", function(event) {
      event.preventDefault();

      // // NO !!! ... as it returns the HTML elements created by Materialize CSS as well
      // console.log(this.innerHTML);
      // console.log(this.text);

      // // Manipulate some form values ...
      // // The next one has been set when the "To find the Cadence connector ..."
      // // button was clicked earlier to reveal the cadence buttons,
      // // but let's just set it again to be *really* sure.
      document.querySelector('input[name="connector_type"]').value = 'cadence';

      document.querySelector('input[name="cadence"]').value = (this.text).toLowerCase();

      console.log("connector_type  = " + document.querySelector('input[name="connector_type"]').value);
      console.log("cadence  = " + document.querySelector('input[name="cadence"]').value);

      // // ... then submit form
      document.getElementById('connector-form').submit();

      return false;
    });
  }

});
