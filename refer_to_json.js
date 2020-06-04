/* A script to parse a linux refer style database to Javascript object.
* 
* final structure should be an (array of an) array of objects
* e.g. [{'Authors': ['Author1', 'Author2']},
*       {'Date': 2020},
*       {'Pages': 1-10},
*       {'Issue': 1},
*       {'Volume': 1},
*       {'Journal': 'Journal1'}
*       {'Title': 'Title1'}]
*/


(function(exports) {

exports.parse = function(l){
  // l = line
  // put global function variables here
  // this will store final output
  var refer = [];
  
  //var lines = l.split(/\r?\n/)
  
  // https://stackoverflow.com/questions/37558344/split-array-at-the-element-which-matches-regex
  // split the input into array of arrays
  function split(array, pattern) {
    return array.reduce(function(result, element, index) {
      if (pattern.test(element) && index) {
        result.push([element]);
      } else {
        result[result.length - 1].push(element);
      }
      return result;
    }, [[]]);
  }
  // save nested array as lines
              // split on a blank
  var lines = split(l.split(/\r?\n/), /^\s*$/)
                    // filter on arrays > 1
                    .filter(d => d.length > 1)
                    // get rid of pesky blanks within each array
                    .map(d => d.filter(d => d !== ""));
  
  function array_to_refer(l){
      var entry = [];
      // array for authors
      entry.authors = [];
       for (var i=0; i<l.length; i++) {
          var line = l[i];
        // series of if/elses
          if(line.startsWith('%A')){
              entry.authors.push(line.replace('%A ', ''));
             }
          if(line.startsWith('%D')){
              entry.date = +line.replace('%D ', '');
             }
          if(line.startsWith('%P')){
              entry.pages = line.replace('%P ', '');
             }
          if(line.startsWith('%N')){
              entry.issue = line.replace('%N ', '');
             }
          if(line.startsWith('%V')){
              entry.volume = line.replace('%V ', '');
             }
          if(line.startsWith('%J')){
              entry.journal = line.replace('%J ', '');
             }
          if(line.startsWith('%T')){
              entry.title = line.replace('%T ', '');
             }
           if(line === ""){
             break;
           }
       }
    return entry;
  }

  for (var i=0; i<lines.length; i++) {
    refer.push(array_to_refer(lines[i]));
  }
  // end loop
  return refer;
})(
    // exports will be set in any commonjs platform; use it if it's available
    typeof exports !== "undefined" ?
    exports :
    // otherwise construct a name space.  outside the anonymous function,
    // "this" will always be "window" in a browser, even in strict mode.
    // thanks Jason Davies. https://github.com/jasondavies/newick.js/blob/master/src/newick.js
    this.Refer = {}
);