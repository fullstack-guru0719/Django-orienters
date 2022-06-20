document.addEventListener("DOMContentLoaded", function() {
  var selected_words = [];

  // // The continue button disappears after its clicked
  document.getElementById('continue').addEventListener("click", function(event) {
    event.preventDefault();

    document.getElementById('choose-words').classList.remove('hide');

    var diz = this;
    setTimeout(function() {
      diz.parentNode.removeChild(diz);
    }, 2000);
  });

  // // Bind listener on words
  var unordered_words = document.querySelectorAll('input[name="unordered_words[]"]');
  for (let i = 0; i < unordered_words.length; i++) {
      unordered_words[i].addEventListener("click", function(event) {
        // event.preventDefault();

        // console.log('this.value = ' + this.value);

        var _indexOf =
          // selected_words.indexOf(this.value);
          selected_words.findIndex(x => x.id === this.value);

        if (_indexOf !== -1) {
          // // remove if inside
          selected_words.splice(_indexOf, 1);
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
          selected_words.push({'id':this.value, 'text':
            // this.nextSibling.innerHTML});
            this.parentNode.querySelector('span').innerHTML});
        } else {
          // // remove if inside
          // selected_words.slice(_indexOf, 1);
        }

        if (selected_words.length == 12) {
          // // Show the reorder element
          var reorder_words = document.getElementById('reorder-words');
          reorder_words.classList.remove('hide');

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

      });
  }

  // // Listen for form submission
  document.getElementById("identifier-form").addEventListener("submit", function(e){
    // e.preventDefault();

    // // put word ids into hidden input as a comma delimited string
    var ids = [];
    for (let j = 0; j < selected_words.length; j++) {
      var selected_word = selected_words[j];
      ids.push(selected_word.id);
    }
    document.querySelector("input[name='words']").value = ids.join(",");

    return true;
  });
});
