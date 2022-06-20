document.addEventListener("DOMContentLoaded", function() {

  // // share with group drop down
  var share_with_group_select = document.querySelector('select[name="share_with_group_id"]');

  // // Init Materialize CSS for the above drop down
  M.FormSelect.init(share_with_group_select, {});

  // // share with (multiple ?) user drop down
  var share_with_user_select = document.querySelector('select[name="share_with_user_id"]');

  // // Init Materialize CSS for the above drop down
  M.FormSelect.init(share_with_user_select, {});






  /*
  // // checkbox to activate user select boxes
  var entity_type_user = document.getElementById('entity_type_user');
  entity_type_user.addEventListener("change", function(event) {

    // console.log('entity_type_user ' + this.checked);

    if (this.checked) {
      var selectElement = document.getElementById('share_with_user_id');
      var otherSelectElement = document.getElementById('share_with_group_id');

      // // activate the user drop down
      selectElement.removeAttribute('disabled');

      // var instance = M.FormSelect.getInstance(selectElement);
      // instance.destroy();
      M.FormSelect.init(selectElement, {});

      // // deactivate the group drop down
      otherSelectElement.setAttribute('disabled', 'disabled');
      M.FormSelect.init(otherSelectElement, {});
    }
  });

  // // checkbox to activate group select boxes
  var entity_type_group = document.getElementById('entity_type_group');
  entity_type_group.addEventListener("change", function(event) {

    // console.log('entity_type_group ' + this.checked);

    if (this.checked) {
      var selectElement = document.getElementById('share_with_group_id');
      var otherSelectElement = document.getElementById('share_with_user_id');

      // // activate the group drop down
      selectElement.removeAttribute('disabled');

      // var instance = M.FormSelect.getInstance(selectElement);
      // instance.destroy();
      M.FormSelect.init(selectElement, {});

      // // deactivate the user drop down
      otherSelectElement.setAttribute('disabled', 'disabled');
      M.FormSelect.init(otherSelectElement, {});
    }
  });
  */





  // // The circle, words & share buttons
  var content_selectors = document.querySelectorAll('a.content_selector');
  for (let i = 0; i < content_selectors.length; i++) {
    content_selectors[i].addEventListener("click", function(event) {
      event.preventDefault();

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








  // // The cadence buttons & their report + questions
  var cadence_buttons = document.querySelectorAll('.cadence a');
  for (let i = 0; i < cadence_buttons.length; i++) {
    cadence_buttons[i].addEventListener("click", function(event) {
      // event.preventDefault();

      // // Reset the active cadence button
      for (let j = 0; j < cadence_buttons.length; j++) {
        var cadence_button = cadence_buttons[j];
        if (cadence_button.classList.contains('btn-active')) {
          cadence_button.classList.remove('btn-active');
        }
      }

      // // Show the clicked clicked button as active
      this.classList.add('btn-active');

      // // Hide existing cadence detail
      var cds = document.querySelectorAll('.cadence-detail');
      for (let j = 0; j < cds.length; j++) {
        var cd = cds[j];
        if (!cd.classList.contains('hide')) {
          cd.classList.add('hide');
        }
      }

      // // Reveal the detail for the clicked cadence
      var eyed = this.getAttribute('data-id');
      document.getElementById('detail-' + eyed).classList.remove('hide');
    })
  };









  // // The 'display answer form' buttons
  var answer_buttons = document.querySelectorAll('a.show-answer-form');
  for (let i = 0; i < answer_buttons.length; i++) {
    answer_buttons[i].addEventListener("click", function(event) {

      event.preventDefault();

      // // Display hidden answer buttons
      var hidden_answer_buttons = document.querySelectorAll('a.show-answer-form.hide');
      for (let j = 0; j < hidden_answer_buttons.length; j++) {
        hidden_answer_buttons[j].classList.remove('hide');
      }

      // // Display hidden answer paragraphs
      var hidden_existing_answers = document.querySelectorAll('p.answer.hide');
      for (let j = 0; j < hidden_existing_answers.length; j++) {
        hidden_existing_answers[j].classList.remove('hide');
      }

      // // Get the existing answer for this clikced button.
      // // Do this *before* the DOM rearranges.
      // var existingAnswerElement = this.previousSibling;
      var existingAnswerElement = this.previousElementSibling;
      var existingAnswer = '';
      if (existingAnswerElement.classList.contains('answer')) {
        existingAnswer = existingAnswerElement.innerHTML;
        // // trim the text
        existingAnswer = existingAnswer.trim();
      }

      // console.log(existingAnswer);

      // // Get the answer form
      var c_a_f = document.getElementById('content-answer-form');
      if (c_a_f) {
        // // Relocate form before the clicked ANSWER button
        var parent = this.parentNode;
        parent.insertBefore(c_a_f, this);

        // // Set form values
        var a_f = document.getElementById('answer-form');
        var cadence = a_f.querySelector('input[name="cadence"]');
        if (cadence) {
          cadence.setAttribute('value', this.getAttribute('data-cadence'));
        }
        var iindex = a_f.querySelector('input[name="iindex"]');
        if (iindex) {
          iindex.setAttribute('value', this.getAttribute('data-iindex'));
        }

        // // Set the value for the existing answer textarea even if
        // // there is no existing answer so as to clear any existing
        // // value in said textarea
        var textareaElement = a_f.querySelector('textarea[name="text"]');
        if (textareaElement) {
          textareaElement.value = existingAnswer;
        }

        // // Hide the existing answer
        existingAnswerElement.classList.add('hide');

        // // Hide the clicked ANSWER button (?)
        this.classList.add('hide');

        // // Show the form
        c_a_f.classList.remove('hide');
      }

    })
  };



  // // Ajax submission of answer-form's "SAVE" button
  var saveAnswerElement = document.getElementById('save-answer');
  if (saveAnswerElement) {
    saveAnswerElement.addEventListener(
      "click",
      // "submit",
      function(event) {
        event.preventDefault();

        var diz = this;

        // // Disable submit button while waiting for Ajax
        diz.classList.toggle('disabled');

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

                // // Post submission, update ui
                var postOkSubmission = function() {
                  var c_a_f = document.getElementById('content-answer-form');
                  if (c_a_f) {
                    // // Get the answer as typed in the textarea
                    var a_f = document.getElementById('answer-form');
                    var textareaElement = a_f.querySelector('textarea[name="text"]');

                    // // Update the existing answer (?)
                    var existingAnswerElement = c_a_f.previousElementSibling;
                    existingAnswerElement.innerHTML = textareaElement.value;

                    // // Hide this form
                    c_a_f.classList.add('hide');

                    // // Show the answer button
                    c_a_f.nextSibling.classList.remove('hide');

                    // // Show the existing answer button
                    c_a_f.previousElementSibling.classList.remove('hide');
                  }
                }
                setTimeout(postOkSubmission, 2000);
            }

            // // You can't really see this if the submission was ok, but nvm ...
            document.getElementById("answer-result").innerHTML = results;

            // // Enable submit button after everything's done
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
        var formData = new FormData(document.getElementById('answer-form'));

        xmlhttp.open("POST", this.getAttribute('href'), true);
        // xmlhttp.setRequestHeader("Content-type", "multipart/form-data; charset=utf-8; boundary=" + Math.random().toString().substr(2));
        xmlhttp.send(formData);

        return false;
    })
  };










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








  // // Ajax submission of the "send-to-my-email" button
  document.getElementById('send-to-my-email').addEventListener("click", function(event) {
    event.preventDefault();

    var href = this.getAttribute('href');

    console.log(href);

    var xmlhttp = false;
    if (window.XMLHttpRequest) {
        xmlhttp = new XMLHttpRequest();
    }
    else if (window.ActiveXObject) {
        xmlhttp = new ActiveXObject('Microsoft.XMLHTTP');
    }

    // // Store a reference to the target element
    var diz = this;

    xmlhttp.onreadystatechange=function() {
      if (xmlhttp.readyState==4 && xmlhttp.status==200) {
         // document.getElementById("relatedPosts").innerHTML=xmlhttp.responseText;
         var responseJSON = JSON.parse(xmlhttp.responseText);

         console.log('xmlhttp.responseText = ' + xmlhttp.responseText);

         // var resultElement = document.getElementById('contact-result');

         if (responseJSON.status == 'ok') {

           alert('Done');

           /*
           // // Fade in the form submission alert
           resultElement.innerHTML = responseJSON.error;
           resultElement.classList.add("has-error", "fade-in");
           */

         } else {

            alert(responseJSON.message);

            /*
            // // Fade in the form submission alert
            resultElement.classList.remove("fade-in"); // just in case :)
            // // Wait a bit so the OK message fade in properly
            setTimeout(function(){
              resultElement.classList.remove("has-error"); // just in case :)
              resultElement.innerHTML = 'Thank you';
              resultElement.classList.add("fade-in");
            }, 1000);


            // // Disable the submit button
            diz.setAttribute("disabled", "disabled");

            // // Wait a bit before enabling it
            setTimeout(function(){
              diz.removeAttribute("disabled");
            }, 2000);
            */
          }
        }
    } // end : xmlhttp.onreadystatechange

    xmlhttp.open("GET", href);
    xmlhttp.send();

    return false;
  });














  var init_tooltip = function(){
  	// // distance from the cursor
		xOffset = 15;
		yOffset = 20;

    var over_to, out_to;
    var cells = document.querySelectorAll(
      // 'img.tooltip'
      'area'
    );

    for (let i = 0; i < cells.length; i++) {
      cells[i].addEventListener("mouseover", function(event) {

        // console.log('mouseover');

        // // Avoid memory leak I guess ?
        clearTimeout(out_to);

        // // Remove residue from previous hovers
        var tooltip_element = document.getElementById('tooltip');
        if (tooltip_element) {
          tooltip_element.remove();
        }

        var diz = this;
        // this.removeAttribute('title');
        // var alt = this.getAttribute('alt').toLowerCase();
        var alt = this.getAttribute('alt');
        var txtNodes = document.getElementById('tooltip-content-' + alt).childNodes;

    		// console.log('alt = ' + alt);
    		// console.log('txt = ' + txt);

        var tooltip_element = document.createElement('div');
        tooltip_element.setAttribute('id', 'tooltip');
        tooltip_element.style['top'] = (event.pageY - yOffset) + 'px';
        tooltip_element.style['left'] = (event.pageX + xOffset) + 'px';

        // tooltip_element.innerHTML = txt;
        for (var w = 0; w < txtNodes.length; w++) {
          tooltip_element.appendChild(txtNodes[w].cloneNode(true));
        }

        document.querySelector('body').appendChild(tooltip_element);

        over_to = setTimeout(() => {
          tooltip_element.style['opacity'] = 1;
        }, 250);
        // tooltip_element.classList.add('fade-in');
      });
      cells[i].addEventListener("mouseout", function(event) {

        // console.log('mouseout');

        // // Avoid memory leak I guess ?
        clearTimeout(over_to);

        var tooltip_element = document.getElementById('tooltip');

        out_to = setTimeout(() => {
          tooltip_element.remove();
        }, 100);
      });
      cells[i].addEventListener("mousemove", function(event) {

        // console.log('mousemove');

        var tooltip_element = document.getElementById('tooltip');
        tooltip_element.style['top'] = (event.pageY + yOffset) + 'px';
        tooltip_element.style['left'] = (event.pageX + xOffset) + 'px';
      });
    }

  };

	init_tooltip();

});
