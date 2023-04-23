# Texas Tech Citibus Route Finder

```diff
 Objective: The main objective of this application is to find the route of the bus inside university premises and student housings.
```

Welcome to our Citi Bus Route Finder Application based on Answer Set Prolog (ASP). This innovative application is designed to help students at Texas Tech University find the best and most efficient bus routes to their desired destinations inside this vast campus. With ASP, our application can help find the most optimal route based on the user’s inputs, including the bus stops and preferred routes.

It is perfect for students who rely on public transportation to get to the campus or to the housing apartment, whether for commuting or leisure. When it comes to reaching the classes on time without wandering in this massive area of the campus, our application is an excellent source of guidance. With just a query, users can get detailed and reliable route information both in speech and text format.

ASP is a powerful language that enables our application to solve complex routing problems with ease. It allows us to represent routing problems as logical statements and find solutions that satisfy all constraints. This means that our application can handle even the most complex routing problems, providing students with a solution that is both accurate and efficient.

## **Problem Description:**
“Texas Tech University is one of the biggest universities in the US geographically,” based on this statement we can assume how difficult it will be for the new students to commute inside the campus. Additionally, there are many buses that operate on many routes both inside and outside the campus. This adds up more burden to the new students to select the bus and the route to reach their classes on time. Moreover, the duration between classes is short and student must rush toward their classes. The students also have to face difficulties in choosing the bus route that takes them to their respective student housing apartments which are located outside of the campus.

## **Questions**
The sample questions that can be asked to the intelligent agents are as follows:

- What is the starting route of #route number(e.g 41)?
- What is the ending route of #route number(e.g 41)?
- What is the route of #location name e.g (holden hall)?
- Route of #location name e.g (holden hall)?
- What is the previous route of #location name e.g (international cultural center)?
- What is the next route of #location name e.g (international cultural center)?
- What is the bus route for #location list? e.g (the holly)?
- Is the #location name e.g(college of business administration) on the same route as #location name e.g(holden hall)?
- Is the #location name e.g(the holly) on the next route of #location name e.g(holden hall)?
- What is the neighbouring route for the #location name e.g(the holly)?
- Is the #location name e.g(the republic) neighbouring route of the #location name e.g(the holly)?
- What is the fastest route of #location name (e.g the holly)?

## **Libraries Used**
### Bootstrap 5.2.3 for Styling webpage
   - Carousel Slider, Navbar, Mobile Reponsive

### Font Awesome 4.7.0 for icons
   - Arrow and Microphone Icon

### JQuery 3.4.1 for Event Handling, Animation and AJAX
   - addEventListener() - on clicking submit button, microphone icon
   - getAnswer() - Translating the questions into ASP query and AJAX Call for sending ASP Query to ASP Solver and getting response
   - DOMParser() - manipulating the elements from HTML documents used to parse ASP solver response human readable language

### FuzzySet for computing similarities to the closest ASP query

   - get() - trying to match the string to the closest ASP query with threshold 0.5.

### SpeechSynthesisVoice for translating the text to voice output

  - speak() - to generate the voice output after generating the answer in the webpage

### SpeechRecognition for translating the voice speech to text

  - start() - gets the voice input from microphone and transfers it to the text in the input

### SPARC Solver for getting the response of ASP Query

  - Online SPARC Solver is (http://wave.ttu.edu/ajax.php).
  - Requesting temporary access to the server via https://cors-anywhere.herokuapp.com/corsdemo and clicking on the “request temporary access to the demo server.” button
  - Passing the ASP query to the solver by getAnswer() in main.js
  - Getting response from the Online SPARC Solver (http://wave.ttu.edu/ajax.php) in ASP response format.

**The Citibus Route Finder** is a project to create an intelligent agent web based application for the course CS-5368 - Intelligent System created using HTML, CSS and JavaScript. The backend of the app is created using SPARC programming language and hosted on GitHub.
<br />
<br />
<img width='100%' src='https://github.com/thesumitshrestha/thesumitshrestha.github.io/blob/master/assets/images/readme/RouteFinderOutput.png' />
