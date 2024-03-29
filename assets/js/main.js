var isClose = true;

// Setting the stopwords
const stopwords = [
  'of',
  'the',
  'a',
  'an',
  'any',
  'is',
  'can',
  'who',
  'what',
  'why',
  'whom',
];

var editor =
  'sorts\n' +
  '#location = {college_of_business_administration, the_republic, the_holly, indiana_village, international_cultural_center, holden_hall, student_union_building, university_library, student_recreation_center, student_wellness_center}.\n' +
  '#route_number = {41, 42, 48}.\n' +
  '#bus_map = {college_of_business_administration___the_republic___the_holly___indiana_village___international_cultural_center, college_of_business_administration___holden_hall___student_union_building___university_library___student_recreation_center___student_wellness_center, college_of_business_administration___student_wellness_center___student_recreation_center___university_library___student_union_building___holden_hall}.\n' +
  'predicates\n' +
  'route(#route_number, #location).\n' +
  'same_route(#location, #location).\n' +
  'neighbouring_route(#location, #location).\n' +
  'previous_route(#location, #location).\n' +
  'next_route(#location, #location).\n' +
  'center_point_route(#location, #route_number).\n' +
  'starting_route(#location, #route_number).\n' +
  'ending_route(#location, #route_number).\n' +
  'fastest_route(#route_number, #location).\n' +
  'bus_route(#bus_map, #route_number).\n' +
  'rules\n' +
  'route(48, college_of_business_administration).\n' +
  'route(48, the_republic).\n' +
  'route(48, the_holly).\n' +
  'route(48, indiana_village).\n' +
  'route(48, international_cultural_center).\n' +
  'route(42, college_of_business_administration).\n' +
  'route(42, holden_hall).\n' +
  'route(42, student_union_building).\n' +
  'route(42, university_library).\n' +
  'route(42, student_recreation_center).\n' +
  'route(42, student_wellness_center).\n' +
  'route(41, college_of_business_administration).\n' +
  'route(41, student_wellness_center).\n' +
  'route(41, student_recreation_center).\n' +
  'route(41, university_library).\n' +
  'route(41, student_union_building).\n' +
  'route(41, holden_hall).\n' +
  'center_point_route(college_of_business_administration, 41).\n' +
  'center_point_route(college_of_business_administration, 42).\n' +
  'center_point_route(college_of_business_administration, 48).\n' +
  'starting_route(college_of_business_administration, 41).\n' +
  'starting_route(college_of_business_administration, 42).\n' +
  'starting_route(college_of_business_administration, 48).\n' +
  'ending_route(holden_hall, 41).\n' +
  'ending_route(student_wellness_center, 42).\n' +
  'ending_route(international_cultural_center, 48).\n' +
  'next_route(college_of_business_administration, international_cultural_center).\n' +
  'next_route(international_cultural_center, indiana_village).\n' +
  'next_route(indiana_village, the_holly).\n' +
  'next_route(the_holly, the_republic).\n' +
  'next_route(the_republic, college_of_business_administration).\n' +
  'next_route(college_of_business_administration, student_wellness_center).\n' +
  'next_route(student_wellness_center, student_recreation_center).\n' +
  'next_route(student_recreation_center, university_library).\n' +
  'next_route(university_library, student_union_building).\n' +
  'next_route(student_union_building, holden_hall).\n' +
  'next_route(holden_hall, college_of_business_administration).\n' +
  'next_route(college_of_business_administration, holden_hall).\n' +
  'next_route(holden_hall, student_union_building).\n' +
  'next_route(student_union_building, university_library).\n' +
  'next_route(university_library, student_recreation_center).\n' +
  'next_route(student_recreation_center, student_wellness_center).\n' +
  'next_route(student_wellness_center, college_of_business_administration).\n' +
  'previous_route(college_of_business_administration, the_republic).\n' +
  'previous_route(the_republic, the_holly).\n' +
  'previous_route(the_holly, indiana_village).\n' +
  'previous_route(indiana_village, international_cultural_center).\n' +
  'previous_route(international_cultural_center, college_of_business_administration).\n' +
  'previous_route(college_of_business_administration, holden_hall).\n' +
  'previous_route(holden_hall, student_union_building).\n' +
  'previous_route(student_union_building, university_library).\n' +
  'previous_route(university_library, student_recreation_center).\n' +
  'previous_route(student_recreation_center, student_wellness_center).\n' +
  'previous_route(student_wellness_center, college_of_business_administration).\n' +
  'previous_route(college_of_business_administration, student_wellness_center).\n' +
  'previous_route(student_wellness_center, student_recreation_center).\n' +
  'previous_route(student_recreation_center, university_library).\n' +
  'previous_route(university_library, student_union_building).\n' +
  'previous_route(student_union_building, holden_hall).\n' +
  'previous_route(holden_hall, college_of_business_administration).\n' +
  'bus_route(college_of_business_administration___student_wellness_center___student_recreation_center___university_library___student_union_building___holden_hall, 41).\n' +
  'bus_route(college_of_business_administration___holden_hall___student_union_building___university_library___student_recreation_center___student_wellness_center, 42).\n' +
  'bus_route(college_of_business_administration___the_republic___the_holly___indiana_village___international_cultural_center, 48).\n' +
  'fastest_route(48, the_republic).\n' +
  'fastest_route(48, the_holly).\n' +
  'fastest_route(48, indiana_village).\n' +
  'fastest_route(48, international_cultural_center).\n' +
  'fastest_route(42, holden_hall).\n' +
  'fastest_route(42, student_union_building).\n' +
  'fastest_route(42, university_library).\n' +
  'fastest_route(41, university_library).\n' +
  'fastest_route(41, student_recreation_center).\n' +
  'fastest_route(48, student_wellness_center).\n' +
  '-same_route(X,Y) :- not same_route(X,Y).\n' +
  'same_route(X,Y) :- route(Z, X), route(Z, Y), X != Y.\n' +
  'next_route(X,Y) :- next_route(X, Y).\n' +
  '-next_route(X,Y) :- not next_route(X, Y).\n' +
  'neighbouring_route(X, Y) :- next_route(X, Y).\n' +
  'neighbouring_route(X, Y) :- previous_route(X, Y).\n' +
  '-neighbouring_route(X, Y) :- not next_route(X, Y), not previous_route(X, Y).';

// Spliting Sorts and Predicates
var contstring = editor.split('sorts\n')[1].split('predicates\n');

// Spliting Sorts value
var sortstring = contstring[0].split('.');

// Sorts Last Value
sortstring.splice(-1, 1);
var sorts = {};
sortstring = sortstring
  .map((d) => d.replace(/\n/g, '').trim())
  .forEach((d) => {
    var par = d.split('=');
    sorts[par[0].replace(/#/, '').trim()] = par[1]
      .replace(/{|}/g, '')
      .split(',')
      .map((w) => w.trim());
  });

// Spliting Predicates Value
var predicates = {};
contstring = contstring[1].split('rules\n');
sortstring = contstring[0].split('.');
sortstring.splice(-1, 1);

// Mapping each predicates and knowledge/rules
sortstring.forEach((d) => {
  var part = d.replace(/\n/g, '').trim().split('(');
  var func = part[0];
  predicates[func] = {};
  var par = part[1].split(',').map((e) => e.replace(/#|\)/g, '').trim());
  var par1 = sorts[par[0]].slice();
  par1.push('X');
  par.splice(0, 1);
  par1.forEach((e) => {
    var strinh = (e == 'X' ? '' : e + ' ') + func;
    predicates[func][strinh] = func + '(' + e + ')';
    par.forEach((par2) => {
      var temp = sorts[par2].slice();
      temp.push('X');
      temp.forEach((t) => {
        var strinh =
          (e == 'X' ? '' : e + ' ') + func + (t == 'X' ? '' : ' ' + t);
        // if (strinh != fubnc)
        predicates[func][strinh] = func + '(' + e + ',' + t + ')';
      });
    });
  });
});

// This rules generates all the knowledge and rules that has the relation and
// append it in all_predicates
var all_predicates = [];
for (var key1 in predicates) {
  if (predicates.hasOwnProperty(key1)) {
    for (var key2 in predicates[key1]) {
      if (predicates[key1].hasOwnProperty(key2)) all_predicates.push(key2);
    }
  }
}

all_predicates.push('speak spanish'); // extra terms
a = FuzzySet(all_predicates);
console.log(all_predicates);

// Speech recognition API
const SpeechRecognition =
  window.SpeechRecognition || window.webkitSpeechRecognition;
const recognition = new SpeechRecognition();
recognition.lang = 'en-US';

// Get DOM elements
const answerDiv = document.querySelector('#answer');
const voiceBtn = document.getElementById('voice-input-btn');
const textInput = document.getElementById('text-input');
const submitBtn = document.getElementById('submit-btn');
const answerBox = document.getElementById('answer-box');

// After user inputs the query and clicks submit button
submitBtn.addEventListener('click', () => {
  const question = textInput.value;
  if (question.trim() === '') {
    answerBox.innerHTML = 'Please ask a question.';
    return;
  }
  // Trims the given sentence by space ' '
  var trim_script = question.split(' ');
  // Removing the stop words from the trim script
  trim_script = trim_script.filter((f) => !stopwords.includes(f));
  console.log('TRIM JOIN', trim_script.join(' '));
  //Compute the similarity and get value with score more than 0.5
  var queryQues = a.get(trim_script.join(','), null, 0.5);
  console.log('QUERY:', queryQues);
  getAnswer(queryQues);
});

// Handle speech recognition input
recognition.onresult = (event) => {
  const resultIndex = event.resultIndex;
  const transcript = event.results[resultIndex][0].transcript;
  textInput.value = transcript;

  // Trims the given sentence by space ' '
  var trim_script = transcript.split(' ');

  // Removing the stop words from the trim script
  trim_script = trim_script.filter((f) => !stopwords.includes(f));

  //Compute the similarity and get value with score more than 0.5
  var queryQues = a.get(trim_script.join(' '), null, 0.5);
  getAnswer(queryQues);
};

// Handle click on voice input button
function startSpeechRecognition() {
  recognition.start();
}
voiceBtn.addEventListener('click', startSpeechRecognition);

function getAnswer(question) {
  if (question != null) {
    // First two element of array as a main key
    var mainkey = question[0][1].replace('speak ', '');
    // Creating array for main keys
    var answerarr = mainkey.split(' ');
    console.log('AnswerARR Key', answerarr);
    var key1 = '';
    answerarr.forEach((d) => {
      key1 = predicates[d] != undefined ? d : key1;
    });
    //var key1 = answerarr.length>2? answerarr[1]:answerarr[0];
    var key2 = mainkey;

    var data = {
      action: 'getQuery',
      query: predicates[key1][key2],
      editor: editor,
    };
    console.log('ASP Query ');
    console.log(predicates[key1][key2]);

    // AJAX CALL
    $.ajax({
      url: 'https://cors-anywhere.herokuapp.com/http://wave.ttu.edu/ajax.php',
      type: 'POST',
      headers: {
        'X-Requested-With': 'XMLHttpRequest',
      },
      data: {
        action: 'getQuery',
        query: predicates[key1][key2],
        editor: editor,
      },

      // AJAX Success Reponse
      success: function (response) {
        // console.log(response);
        const answer = response || 'Sorry, I could not find an answer.';
        const parser = new DOMParser();
        const doc = parser.parseFromString(answer, 'text/html');
        let sparc_query = doc.querySelector('span');
        let sparc_answer = doc.querySelector('p');
        let splittedString = sparc_query.innerHTML.split('(');
        let relation_name = splittedString[0];
        let objectsArray = splittedString[1];

        let objectsArrayNew = objectsArray.split(',');
        var firstAnswer;
        let firstVariable = objectsArrayNew[0];
        let secondVariable = objectsArrayNew[1].split(')')[0];

        // ANSWER
        let sparcNew = sparc_answer.innerHTML.split('=');
        if (sparcNew.indexOf(' X ') > -1) {
          firstAnswer = sparcNew[1]?.replace('X', '');
          firstAnswer = firstAnswer?.replaceAll('_', ' ');
          firstAnswer = firstAnswer.replaceAll('<br>', '');
        } else {
          firstAnswer = sparcNew[0];
        }
        let secondAnswer = sparcNew[2];
        secondAnswer = secondAnswer?.replaceAll('<br>', '');
        if (secondAnswer) {
          answerDiv.innerHTML =
            'The ' +
            relation_name?.replace('_', ' ') +
            ' of ' +
            secondVariable?.replaceAll('_', ' ') +
            ' is </br>' +
            firstAnswer?.replaceAll('_', ' ') +
            ' and ' +
            secondAnswer?.replaceAll('_', ' ');
          $('.answer-container').show();
        } else if (firstVariable != 'X') {
          answerDiv.innerHTML =
            firstAnswer?.replace('<br>\n<br>', '').toUpperCase() +
            ', ' +
            firstVariable?.replaceAll('_', ' ') +
            ' and ' +
            secondVariable?.replaceAll('_', ' ') +
            ' are the ' +
            relation_name?.replaceAll('_', ' ');
          $('.answer-container').show();
        } else {
          answerDiv.innerHTML =
            'The ' +
            relation_name?.replaceAll('_', ' ') +
            ' of ' +
            secondVariable?.replaceAll('_', ' ') +
            ' is ' +
            firstAnswer?.replaceAll('_', ' ');
          $('.answer-container').show();
        }
      },
      error: function (xhr, status, error) {
        console.log('error: ' + error);
      },
    });
  }
}
