document.addEventListener("DOMContentLoaded", function() {

  // // share with group drop down
  var share_with_group_select = document.querySelector('select[name="share_with_group_id"]');

  // // Init Materialize CSS for the above drop down
  M.FormSelect.init(share_with_group_select, {});

  // // share with (multiple ?) user drop down
  var share_with_user_select = document.querySelector('select[name="share_with_user_id"]');

  // // Init Materialize CSS for the above drop down
  M.FormSelect.init(share_with_user_select, {});



  // // The circle, words & share buttons
  var content_selectors = document.querySelectorAll('a.content_selector');
  for (let i = 0; i < content_selectors.length; i++) {
    content_selectors[i].addEventListener("click", function(event) {
      // event.preventDefault();

      // // Reset the active cadence button
      for (let j = 0; j < content_selectors.length; j++) {
        var content_selector = content_selectors[j];
        if (content_selector.classList.contains('btn-active')) {
          content_selector.classList.remove('btn-active');
        }
      }

      // // Show the clicked button as active
      this.classList.add('btn-active');

      // event.preventDefault();

      // // Hide existing cadence detail
      var cds = document.querySelectorAll('.content');
      for (let j = 0; j < cds.length; j++) {
        var cd = cds[j];
        if (!cd.classList.contains('hide')) {
          cd.classList.add('hide');
        }
      }

      // // Reveal the detail for the clicked cadence
      var eyed = this.getAttribute('data-content-id');
      document.getElementById('content-' + eyed).classList.remove('hide');
    })
  };

  // // The members buttons & their title + report
  var member_buttons = document.querySelectorAll('.member a');
  for (let i = 0; i < member_buttons.length; i++) {
    member_buttons[i].addEventListener("click", function(event) {
      // event.preventDefault();

      // // Reset the active members button
      for (let j = 0; j < member_buttons.length; j++) {
        var member_button = member_buttons[j];
        if (member_button.classList.contains('btn-active')) {
          member_button.classList.remove('btn-active');
        }
      }

      // // Show the clicked clicked button as active
      this.classList.add('btn-active');

      // // Hide existing members detail
      var cds = document.querySelectorAll('.member-detail');
      for (let j = 0; j < cds.length; j++) {
        var cd = cds[j];
        if (!cd.classList.contains('hide')) {
          cd.classList.add('hide');
        }
      }

      // // Reveal the detail for the clicked cadence
      var eyed = this.getAttribute('data-id');
      document.getElementById('member-' + eyed).classList.remove('hide');

      console.log('eyed = ' + eyed);
    })
  };

  // // The cadence buttons' hide/show
  var cadence_links = document.querySelectorAll('.cadence a');
  for (let i = 0; i < ajax_obj.cadence_max; i++) {
    cadence_links[i].classList.remove('hide');

    if (cadence_links[i].text.toLowerCase() == ajax_obj.cadence) {
      cadence_links[i].classList.add('btn-active');
    }
  }

  // // The cadence buttons' event listener
  // var cadence_links = document.querySelectorAll('.cadence a');
  for (let i = 0; i < cadence_links.length; i++) {
    cadence_links[i].addEventListener("click", function(event) {
      event.preventDefault();

      // // Get target element
      var target = event.target || event.srcElement;

      // if (cadence_links[i].text.toLowerCase() == ajax_obj.cadence) {
      if (target.text.toLowerCase() == ajax_obj.cadence) {

        console.log('this is the current cadence ...');

        // // Disable the button for the current cadence in the report
        return false;
      }

      // // NO !!! ... as it returns the HTML elements created by Materialize CSS as well
      // console.log(this.innerHTML);

      // // Manipulate some form values ...
      // // The next one has been set when the "To find the Cadence connector ..."
      // // button was clicked earlier to reveal the cadence buttons,
      // // but let's just set it again to be *really* sure.

      var connector_form = document.getElementById('connector-form');

      connector_form.querySelector('input[name="cadence"]').value =
        (this.text).toLowerCase();
        // target.text.toLowerCase();

      // // ... then submit form
      connector_form.submit();

      return false;
    });
  }







  // // Ajax submission of share-form's "SAVE" button
  var saveShareElement = document.getElementById('save-share');
  if (saveShareElement) {
    saveShareElement.addEventListener(
      "click",
      // "submit",
      function(event) {
        event.preventDefault();

        var diz = this;

        diz.classList.toggle('disabled');

        console.log(diz.getAttribute('href'));

        // // Manipulate some form values ...
        // document.querySelector('input[name="connector_type"]').value = 'cadence';

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

             console.log('share click : xmlhttp.responseText = ' + xmlhttp.responseText);

             var results = responseJSON.message;

             if (responseJSON.status == 'error') {

               console.log('share click : KO. message = ' + responseJSON.message);

             } else {

                console.log('share click : OK. message = ' + responseJSON.message);

                results = responseJSON.status;

                /*
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
                */
            }

            document.getElementById("share-result").innerHTML = results;

            diz.classList.toggle('disabled');

          }
        };

        /*
        // // Manually field by field

        var formData = new FormData();
        formData.append("action", action);
        formData.append("nonce_field", nonce_value);
        formData.append("name", name);
        formData.append("body", body);
        */

        // // Let the browser deal with it :)
        var formData = new FormData(document.getElementById('share-form'));

        xmlhttp.open("POST", this.getAttribute('href'), true);
        // xmlhttp.setRequestHeader("Content-type", "multipart/form-data; charset=utf-8; boundary=" + Math.random().toString().substr(2));
        xmlhttp.send(formData);

        return false;
      });
  }

});
