document.addEventListener("DOMContentLoaded", function() {
  var selected_words = [];

  var slugify = function(string) {
    return string
      .toString()
      .trim()
      .toLowerCase()
      .replace(/\s+/g, "-")
      .replace(/[^\w\-]+/g, "")
      .replace(/\-\-+/g, "-")
      .replace(/^-+/, "")
      .replace(/-+$/, "");
  }

  // // Display all instance of this word as clicked
  var toggleWordElement = function(className) {
    var wordSpansElement = document.getElementById('word-spans');
    var relevantElements = wordSpansElement.querySelectorAll('.' + className);
    // for (var relevantElement in relevantElements) {
    for (let k = 0; k < relevantElements.length; k++) {
      relevantElements[k].classList.toggle('clicked');
    }
  }

  // // Update the relevant hidden fields upon changes to .input_data_raw
  var input_data_raws = document.querySelectorAll('.input_data_raw');
  for (let i = 0; i < input_data_raws.length; i++) {
      input_data_raws[i].addEventListener("change", function(event) {
        var input_data = document.querySelector("input[name='input_data']");
        input_data.value = this.value;

        // console.log('input_data is now:');
        // console.log(input_data.value);
      });
  }

  // // The continue button disappears after it is clicked
  document.getElementById('continue').addEventListener("click", function(event) {
    event.preventDefault();

    var has_error = false;
    var existingErrorElement = null;

    // // Ensure title is filled
    var answer = document.querySelector('textarea[name="input_data"]');
    existingErrorElement = answer.parentNode.querySelector('span.red-text');
    if (answer && answer.value == '') {
      has_error = true;

      // // Show the error element if not visible already
      if (!existingErrorElement) {
        var errorElement = document.createElement('span');
        errorElement.classList.add('red-text');
        var textNode = document.createTextNode('Please fill in your answer');
        errorElement.appendChild(textNode);
        answer.parentNode.appendChild(errorElement);
      }
    } else {
      // // Remove error element if it is visible
      if (existingErrorElement) {
        answer.parentNode.removeChild(existingErrorElement);
      }
    }

    if (has_error) {return false;}

    var diz = this;
    setTimeout(function() {
      diz.parentNode.removeChild(diz);
    }, 2000);



    // // Clean then split words into spans
    var sans_white_space = (answer.value).replace(/^\s+|\s+$|\s+(?=\s)/g, '');
    var cleaned_input_data_1 = sans_white_space.replace(/[`~!@#$%^&*()_|+\-=?;:'",.+<>\{\}\[\]\\\/]/gi, '');
    var words = cleaned_input_data_1.split(" ");
    // // Remove empty or falsy elements
    var words_filtered = words.filter(function(el) { return el; });

    var wordSpansElement = document.getElementById('word-spans');

    for (var i = 0; i < words_filtered.length; i++) {
      var spanElement = document.createElement('span');

      // // Add a class such that if this word is clicked (not hovered),
      // // similar words get highlighted too.
      // // First, we create a safe version of this word.
      var safeWord = slugify(words_filtered[i]);

      console.log(words_filtered[i] + ' : ' + safeWord);

      // // Then use that as the class name
      spanElement.classList.add(safeWord);

      // // The text within each span
      var textNode = document.createTextNode(words_filtered[i]);
      spanElement.appendChild(textNode);

      // // Assign click listener to the word spans
      spanElement.addEventListener("click", spanElementListener);

      wordSpansElement.appendChild(spanElement);
    }

    // // Hide the textarea and show the word span elements
    document.getElementById('input-data-1').classList.add('hide');
    wordSpansElement.classList.remove('hide');

    var diz = this;
    setTimeout(function() {
      // // Remove self
      // diz.parentNode.removeChild(diz);

      // // Hide self
      diz.classList.add('hide');
    }, 2000);
  });

  // // TODO : Debug me
  // // TODO : Debug me
  // // TODO : Debug me
  // // TODO : Debug me
  // // TODO : Debug me
  // // Bind listener on word spans
  var spanElementListener = function(event) {
      // event.preventDefault();

      var diz = event.target;
      var className = diz.classList[0];

      var _indexOf =
        // selected_words.indexOf(this.value);
        selected_words.findIndex(x => x.id === className);

      if (_indexOf !== -1) {
        // // remove if inside
        selected_words.splice(_indexOf, 1);

        // // Display all instance of this word as unclicked
        toggleWordElement(className);
      }

      // console.table(selected_words);

      // // Clicking on not yet added words when we've reached the limit will not do anything
      if (selected_words.length == 12 && _indexOf === -1) {
        // // Don't check the checkbox
        event.preventDefault();

        return;
      }

      if (_indexOf === -1) {
        // // add if not inside
        selected_words.push({'id':className, 'text': diz.innerHTML});

        // // Display all instance of this word as clicked
        toggleWordElement(className);
      } else {
        // // remove if inside
        // selected_words.slice(_indexOf, 1);
      }

      // // Takes up a lot of screen space
      // console.table(selected_words);

      // if (selected_words.length == 12) {
      if (selected_words.length == 2) {
        // // Show the reorder element
        var reorder_words = document.getElementById('reorder-words');
        reorder_words.classList.remove('hide');

        console.log('spanElementListener : did the reorder table appear ?');

        // // init row sorting
        // tableDragger(reorder_words, { mode: "row" });
        var actual_reorder_words = reorder_words.querySelector('div');
        new Sortable(actual_reorder_words, {
            animation: 150,
            ghostClass: 'deep-orange',
          	// Changed sorting within list
          	onUpdate: function (/**Event*/evt) {
              var itemEl = evt.item;  // dragged HTMLElement
          		evt.to;    // target list
          		evt.from;  // previous list
          		evt.oldIndex;  // element's old index within old parent
          		evt.newIndex;  // element's new index within new parent
          		evt.oldDraggableIndex; // element's old index within old parent, only counting draggable elements
          		evt.newDraggableIndex; // element's new index within new parent, only counting draggable elements
          		evt.clone // the clone element
          		evt.pullMode;  // when item is in another sortable: `"clone"` if cloning, `true` if moving

              // // Update selected_words
              // // Not exactly efficient, but CPU is cheap these days :P
              selected_words = [];
              // var children = evt.from.children;
              var children = actual_reorder_words.children;
              for (var i = 0; i < children.length; i++) {
                var row = children[i];
                selected_words.push({
                  'id':row.getAttribute('data-id'),
                  'text':row.innerHTML
                });
              }
              // console.table(selected_words);
            },
        })
      }

      // // if the drag and drop element is visible, we update that too
      var reorder_words = document.getElementById('reorder-words');
      if (!reorder_words.classList.contains('hide')) {
        // // the list is actually a div deep, so get that element
        var actual_reorder_word = reorder_words.querySelector('div');
        // // Remove all children
        while (actual_reorder_word.firstChild) {
          actual_reorder_word.removeChild(actual_reorder_word.firstChild);
        }
        // // Add new ones
        for (let j = 0; j < selected_words.length; j++) {
          var selected_word = selected_words[j];
          var div_element = document.createElement("div");
          div_element.classList.add('collection-item');
          div_element.setAttribute('data-id', selected_word.id);
          div_element.innerHTML = selected_word.text;
          actual_reorder_word.appendChild(div_element);
        }
      }

  }


  // // Listen for form submission
  document.getElementById("echo-form").addEventListener("submit", function(e){
    // e.preventDefault();

    // // put word ids into hidden input as a comma delimited string
    var ids = [];
    for (let j = 0; j < selected_words.length; j++) {
      var selected_word = selected_words[j];
      ids.push(selected_word.id);
    }
    document.querySelector("input[name='input_keywords']").value = ids.join("|");
    document.querySelector("input[name='input_count']").value = ids.length;

    return true;
  });
});
