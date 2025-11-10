// यह जावास्क्रिप्ट कोड मोबाइल मेनू के लिए है

// उन HTML एलिमेंट्स को चुनें जिनकी हमें ज़रूरत है
const menuToggle = document.querySelector('.menu-toggle');
const navLinks = document.querySelector('nav ul');

// जब कोई 'menu-toggle' (hamburger icon) पर क्लिक करे
menuToggle.addEventListener('click', () => {
    // 'nav ul' (मेनू) पर 'active' नाम की CSS क्लास को लगाओ या हटाओ
    navLinks.classList.toggle('active');
    
    // आइकॉन को ☰ से X में और X से ☰ में बदलो
    if (menuToggle.innerHTML === '☰') {
        menuToggle.innerHTML = '✕'; // यह 'X' है
    } else {
        menuToggle.innerHTML = '☰';
    }
});