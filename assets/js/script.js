const synth = window.speechSynthesis;

const inputTxt = document.querySelector('.query-input');

const submitButton = document.getElementById('submit-btn');
const answerText = document.getElementById('answer');
const voiceSelect = document.querySelector('select');

const pitchValue = 1;
const rateValue = 1;

let voices = [];

function populateVoiceList() {
  voices = synth.getVoices().sort(function (a, b) {
    const aname = a.name.toUpperCase();
    const bname = b.name.toUpperCase();

    if (aname < bname) {
      return -1;
    } else if (aname == bname) {
      return 0;
    } else {
      return +1;
    }
  });
  const selectedIndex =
    voiceSelect.selectedIndex < 0 ? 0 : voiceSelect.selectedIndex;
  voiceSelect.innerHTML = '';

  for (let i = 0; i < voices.length; i++) {
    const option = document.createElement('option');
    option.textContent = `${voices[i].name} (${voices[i].lang})`;

    if (voices[i].default) {
      option.textContent += ' -- DEFAULT';
    }

    option.setAttribute('data-lang', voices[i].lang);
    option.setAttribute('data-name', voices[i].name);
    voiceSelect.appendChild(option);
  }
  voiceSelect.selectedIndex = selectedIndex;
}

populateVoiceList();

if (speechSynthesis.onvoiceschanged !== undefined) {
  speechSynthesis.onvoiceschanged = populateVoiceList;
}

function speak() {
  if (synth.speaking) {
    console.error('speechSynthesis.speaking');
    return;
  }

  if (inputTxt.value !== '') {
    const utterThis = new SpeechSynthesisUtterance(answerText.innerText);

    utterThis.onend = function (event) {
      console.log('SpeechSynthesisUtterance.onend');
    };

    utterThis.onerror = function (event) {
      console.error('SpeechSynthesisUtterance.onerror');
    };

    const selectedOption =
      voiceSelect.selectedOptions[0].getAttribute('data-name');

    for (let i = 0; i < voices.length; i++) {
      if (voices[i].name === selectedOption) {
        utterThis.voice = voices[i];
        break;
      }
    }
    utterThis.pitch = pitch.value;
    utterThis.rate = rate.value;
    synth.speak(utterThis);
  }
}

submitButton.onclick = function (event) {
  console.log('Speak Output Ready');
  event.preventDefault();
  setTimeout(() => {
    speak();
  }, 2000);
  return true;
};

voiceSelect.onchange = function () {
  speak();
};
