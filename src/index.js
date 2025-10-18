import './styles/main.css';

// Wait for DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    console.log('RecruitPro APK initialized!');
    
    // Get the start button
    const startBtn = document.getElementById('start-assessment');
    if (startBtn) {
        startBtn.addEventListener('click', function() {
            alert('Assessment functionaliteit wordt geladen...');
            // Hier zou de assessment functionaliteit starten
        });
    }
});
