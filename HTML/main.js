document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('subscribeForm');
    const emailInput = document.querySelector('input[name="email"]');
    const feedback = document.getElementById('feedback-message');
    const button = form.querySelector('button[type="submit"]');

    if (!form) {
        console.error('Form not found!');
        return;
    }

    function setFeedback(message, colorClass) {
        feedback.textContent = message;
        feedback.className = 'text-xs mt-2 ' + colorClass;
    }

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        console.log('Form submitted');
        
        const email = emailInput.value.trim();
        console.log('Email:', email);
        
        // Email validation using regex
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(email)) {
            setFeedback('Please enter a valid email address', 'feedback-cyan');
            return;
        }

        button.disabled = true;
        setFeedback('Subscribing...', 'feedback-cyan');
        // TODO: Replace with your deployed subscribe endpoint:
        const endpoint = "https://your-deployed-backend-url/api/subscribe";
        

        try {
            const response = await fetch(endpoint, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ email })
            });

            console.log('Response received:', response.status);
            if (response.ok) {
                setFeedback('Thanks for subscribing! A confirmation email has been sent. If it’s in Spam, mark it as "Not Junk" so you don’t miss future emails.', 'feedback-cyan');
                emailInput.value = '';
            } else {
                const data = await response.json();
                setFeedback(data.error || 'Failed to subscribe. Please try again.', 'text-red-500');
            }
        } catch (error) {
            console.error('Error:', error);
            setFeedback('Failed to connect to the server. Please try again later.', 'text-red-500');
        } finally {
            button.disabled = false;
        }
    });

    // Reset feedback to default when user starts typing
    emailInput.addEventListener('input', () => {
        setFeedback('You can unsubscribe at any time.', 'text-gray-400');
    });
});
