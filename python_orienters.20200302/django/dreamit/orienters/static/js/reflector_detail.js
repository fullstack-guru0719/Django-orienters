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
      var cdis = document.querySelectorAll('.cadence-detail-' + eyed)
      for (let j = 0; j < cdis.length; j++) {
        var cdi = cdis[j];
        if (cdi.classList.contains('hide')) {
          cdi.classList.remove('hide');
        }
      }

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








  var init_tooltip = function(){
  	// // distance from the cursor
		xOffset = 15;
		yOffset = 20;

    var over_to, out_to;
    var cells = document.querySelectorAll('img.tooltip');

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
        var xxx = this.getAttribute('data-x');
        var yyy = this.getAttribute('data-y');
        // var txt = g_l_o_b_a_l.tooltip_descriptions[xxx * 1][yyy * 1];
        var txt = g_l_o_b_a_l.tooltip_descriptions[(xxx * 1) - 1][(yyy * 1) - 1];

        var tooltip_element = document.createElement('div');
        tooltip_element.setAttribute('id', 'tooltip');
        tooltip_element.style['top'] = (event.pageY - yOffset) + 'px';
        tooltip_element.style['left'] = (event.pageX + xOffset) + 'px';
        // tooltip_element.innerHTML = 'DOWN/X :' + xxx + '<br/>RIGHT/Y :' + yyy + '<br/>' + txt;
        tooltip_element.innerHTML = txt;

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
