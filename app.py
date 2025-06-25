import os
from flask import Flask, render_template, request

app = Flask(__name__)
app.config['SECRET_KEY'] = 'a_very_secure_secret_for_the_nish_solutions'

@app.route('/', methods=['GET', 'POST'])
def mitigation_tool():
    if request.method == 'POST':
        risk_description = request.form.get('risk_description', 'No description provided.')
        industry = request.form.get('industry', 'Not Specified')
        company_size = request.form.get('company_size', 'Not Specified')
        
        # In a real app, you would have your AI logic here.
        # This is a placeholder response.
        result_text = (
            f"**Risk Identified:**\n{risk_description}\n\n"
            f"**Industry Context:** {industry}\n"
            f"**Company Size:** {company_size}\n\n"
            "-----------------------------------\n\n"
            "**Recommended Mitigation Strategies:**\n\n"
            "**1. Technical Controls:**\n"
            "   - **Access Management:** Implement a Role-Based Access Control (RBAC) model to enforce the principle of least privilege.\n"
            "   - **Encryption:** Ensure all sensitive data is encrypted, both at rest and in transit, using industry-standard AES-256 encryption.\n"
            "   - **Endpoint Security:** Deploy advanced endpoint detection and response (EDR) solutions on all company devices.\n\n"
            "**2. Administrative Controls:**\n"
            "   - **Security Policies:** Develop and enforce a comprehensive information security policy. This should be reviewed and updated annually.\n"
            "   - **Employee Training:** Conduct mandatory, regular security awareness training for all employees, focusing on phishing, social engineering, and data handling.\n"
            "   - **Incident Response Plan:** Establish and regularly test a formal incident response plan to ensure a swift and effective reaction to any security breaches.\n\n"
            "**3. Physical Controls:**\n"
            "   - **Facility Access:** Secure all physical locations where sensitive data is stored or accessed, using badge readers and activity logging."
        )
        return render_template('mitigation_tool.html', result=result_text)

    # For GET requests, just render the page without results
    return render_template('mitigation_tool.html', result=None)

if __name__ == '__main__':
    # This block is for local development. Render will use the Gunicorn command.
    port = int(os.environ.get('PORT', 5004))
    app.run(host='0.0.0.0', port=10000, debug=True)
